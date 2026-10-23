"""
dataset_generator.py - Synthetic Dataset Generator with Physical Stochastic Variations
Part of 'Self-Learning Circuit Doctor: Voltage-Signature-Based Fault Detection in DC Circuits'
BEEE Project for B.Tech

Models:
  1. Component Tolerances: Standard 5% resistor manufacturing tolerances (Gaussian distribution 3-sigma truncated).
  2. Supply Voltage Regulation: DC supply drift around 10.0 V nominal (Gaussian std = 0.1 V, ~1%).
  3. Sensor Measurement Noise: Digital Multimeter (DMM) / ADC quantization & thermal noise on VA, VB, and Is.
"""

import os
import sys
import numpy as np
from typing import Tuple, Dict, Any, Optional

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.circuit_model import (
    DCResistorNetwork, NUMERICAL_OPEN_RESISTANCE, NUMERICAL_SHORT_RESISTANCE
)
from src.fault_scenarios import FAULT_CATALOG, FAULT_CLASSES


class CircuitDatasetGenerator:
    """
    Generates synthetic datasets reflecting physical DC resistor network behavior under
    realistic lab conditions (tolerances, supply variations, sensor noise).
    """

    def __init__(self,
                 samples_per_class: int = 150,
                 resistor_tolerance_pct: float = 5.0,
                 supply_noise_std: float = 0.05,
                 voltage_meas_noise_std: float = 0.02,
                 current_meas_noise_std: float = 0.02,
                 random_seed: int = 42):
        """
        Args:
            samples_per_class: Number of observations per fault class.
            resistor_tolerance_pct: Resistor tolerance standard percentage (default: 5%).
            supply_noise_std: Standard deviation of supply voltage (default: 0.05 V).
            voltage_meas_noise_std: DMM voltage sensor noise std (default: 0.02 V).
            current_meas_noise_std: DMM current sensor noise std (default: 0.02 mA).
            random_seed: Seed for reproducible data generation.
        """
        self.samples_per_class = samples_per_class
        self.resistor_tolerance_pct = resistor_tolerance_pct
        self.supply_noise_std = supply_noise_std
        self.voltage_meas_noise_std = voltage_meas_noise_std
        self.current_meas_noise_std = current_meas_noise_std
        self.random_seed = random_seed
        self.rng = np.random.RandomState(random_seed)

    def generate_sample(self, fault_key: str) -> Dict[str, Any]:
        """
        Generates a single synthetic circuit sample for the specified fault class
        with perturbed component values and sensor noise.
        """
        info = FAULT_CATALOG[fault_key]

        # 1. Supply Voltage Variation
        Vs = max(1.0, float(self.rng.normal(loc=10.0, scale=self.supply_noise_std)))

        # 2. Resistor Tolerance Perturbations
        # 5% tolerance typically corresponds to 3-sigma = 5% => sigma = 5% / 3 = 1.67%
        tol_sigma = (self.resistor_tolerance_pct / 100.0) / 3.0

        def sample_resistor(nominal_val: float, factor: Optional[float], is_open: bool, is_short: bool) -> float:
            if is_open:
                # Open circuit: very high resistance with random air-gap leakage variation
                return NUMERICAL_OPEN_RESISTANCE * self.rng.uniform(0.9, 1.1)
            if is_short:
                # Short circuit: contact resistance variation in micro-ohms
                return NUMERICAL_SHORT_RESISTANCE * self.rng.uniform(0.5, 2.0)
            target_val = nominal_val * (factor if factor is not None else 1.0)
            noise_factor = 1.0 + self.rng.normal(0.0, tol_sigma)
            return max(1.0, target_val * noise_factor)

        r1 = sample_resistor(1000.0, info['r1_factor'], info['is_open'] == 'R1', info['is_short'] == 'R1')
        r2 = sample_resistor(2000.0, info['r2_factor'], info['is_open'] == 'R2', info['is_short'] == 'R2')
        r3 = sample_resistor(1500.0, info['r3_factor'], info['is_open'] == 'R3', info['is_short'] == 'R3')
        r4 = sample_resistor(3000.0, info['r4_factor'], info['is_open'] == 'R4', info['is_short'] == 'R4')

        # 3. Electrical Solution
        net = DCResistorNetwork(Vs=Vs, R1=r1, R2=r2, R3=r3, R4=r4)
        true_state = net.solve()

        # 4. Sensor Measurement Noise
        # DMM voltage noise
        meas_va = max(0.0, true_state.VA + self.rng.normal(0.0, self.voltage_meas_noise_std))
        meas_vb = max(0.0, true_state.VB + self.rng.normal(0.0, self.voltage_meas_noise_std))
        # DMM current noise
        meas_is = max(0.0, true_state.Is + self.rng.normal(0.0, self.current_meas_noise_std))

        # Clamp open circuit currents physically to zero if effectively open
        if info['is_open'] == 'R1':
            meas_va = max(0.0, abs(self.rng.normal(0.0, 0.005)))
            meas_vb = max(0.0, abs(self.rng.normal(0.0, 0.005)))
            meas_is = max(0.0, abs(self.rng.normal(0.0, 0.002)))

        return {
            'fault_class': fault_key,
            'fault_code': info['code'],
            'fault_name': info['name'],
            'Vs_actual': round(Vs, 3),
            'R1_actual': round(r1, 1),
            'R2_actual': round(r2, 1),
            'R3_actual': round(r3, 1),
            'R4_actual': round(r4, 1),
            'VA_true': round(true_state.VA, 4),
            'VB_true': round(true_state.VB, 4),
            'Is_true': round(true_state.Is, 4),
            'VA': round(meas_va, 4),
            'VB': round(meas_vb, 4),
            'Is': round(meas_is, 4)
        }

    def generate_full_dataset(self) -> Dict[str, Any]:
        """
        Generates full dataset across all 13 classes with stratified train/test partitioning.
        """
        records = []
        for fault_key in FAULT_CLASSES:
            for _ in range(self.samples_per_class):
                rec = self.generate_sample(fault_key)
                records.append(rec)

        # Feature matrix X: [VA, VB, Is]
        X = np.array([[r['VA'], r['VB'], r['Is']] for r in records], dtype=float)
        # Class labels y
        y = np.array([r['fault_class'] for r in records], dtype=object)

        return {
            'records': records,
            'X': X,
            'y': y,
            'feature_names': ['VA', 'VB', 'Is'],
            'classes': FAULT_CLASSES
        }

    def train_test_split(self, test_ratio: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list, list]:
        """
        Stratified train/test split ensuring balanced representation for every fault class.
        
        Returns:
            X_train, X_test, y_train, y_test, train_records, test_records
        """
        dataset = self.generate_full_dataset()
        records = dataset['records']

        train_records = []
        test_records = []

        # Stratify by fault_class
        for cls in FAULT_CLASSES:
            cls_recs = [r for r in records if r['fault_class'] == cls]
            n_total = len(cls_recs)
            n_test = int(round(n_total * test_ratio))
            
            # Shuffle indices for this class
            indices = self.rng.permutation(n_total)
            test_idx = indices[:n_test]
            train_idx = indices[n_test:]

            for i in train_idx:
                train_records.append(cls_recs[i])
            for i in test_idx:
                test_records.append(cls_recs[i])

        X_train = np.array([[r['VA'], r['VB'], r['Is']] for r in train_records], dtype=float)
        y_train = np.array([r['fault_class'] for r in train_records], dtype=object)

        X_test = np.array([[r['VA'], r['VB'], r['Is']] for r in test_records], dtype=float)
        y_test = np.array([r['fault_class'] for r in test_records], dtype=object)

        return X_train, X_test, y_train, y_test, train_records, test_records


def save_dataset_to_csv(filepath: str, records: list) -> None:
    """Exports dataset records to standard CSV without requiring external libraries."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not records:
        return
    headers = list(records[0].keys())
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(','.join(headers) + '\n')
        for r in records:
            row_str = ','.join(str(r[h]) for h in headers)
            f.write(row_str + '\n')


if __name__ == '__main__':
    print("Generating synthetic DC circuit fault dataset...")
    gen = CircuitDatasetGenerator(samples_per_class=150, random_seed=42)
    X_train, X_test, y_train, y_test, train_recs, test_recs = gen.train_test_split(test_ratio=0.2)
    print(f"Generated Total Samples: {len(train_recs) + len(test_recs)}")
    print(f"Training Set Samples  : {len(train_recs)} ({len(train_recs)//len(FAULT_CLASSES)} per class)")
    print(f"Testing Set Samples   : {len(test_recs)} ({len(test_recs)//len(FAULT_CLASSES)} per class)")

    # Save to data/
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    save_dataset_to_csv(os.path.join(out_dir, 'circuit_fault_train.csv'), train_recs)
    save_dataset_to_csv(os.path.join(out_dir, 'circuit_fault_test.csv'), test_recs)
    save_dataset_to_csv(os.path.join(out_dir, 'circuit_fault_full.csv'), train_recs + test_recs)
    print(f"Saved datasets to {out_dir}")
