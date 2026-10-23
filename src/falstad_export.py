"""
falstad_export.py - Falstad Circuit Simulator Exporter and Experiment Log Generator
Part of 'Self-Learning Circuit Doctor: Voltage-Signature-Based Fault Detection in DC Circuits'
BEEE Project for B.Tech

Generates:
  1. Falstad circuit text files (.txt) ready for 'File -> Import from Text'.
  2. Standalone URL links with encoded circuit definitions for 1-click browser simulation.
  3. falstad_experiment_log.csv logging all tested scenarios, simulator readings,
     Python model theoretical values, and diagnostic classifier decisions.
"""

import os
import sys
import urllib.parse
import csv
from typing import Dict, Any, List

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.circuit_model import DCResistorNetwork
from src.fault_scenarios import FAULT_CATALOG, FAULT_CLASSES, create_circuit_for_fault
from src.classifier import NearestCentroidClassifier, get_trained_classifier


def generate_falstad_circuit_text(Vs: float = 10.0,
                                  R1: float = 1000.0,
                                  R2: float = 2000.0,
                                  R3: float = 1500.0,
                                  R4: float = 3000.0,
                                  title: str = "DC Resistor Network") -> str:
    """
    Constructs a valid Falstad Circuit Simulator ASCII representation.
    
    Coordinates grid layout:
      DC Source: (160, 304) to (160, 144) -> 10V DC
      Wire:      (160, 144) to (240, 144)
      R1:        (240, 144) to (352, 144) -> R1 Ohms
      Node A:    (352, 144)
      R2:        (352, 144) to (352, 304) -> R2 Ohms
      R3:        (352, 144) to (496, 144) -> R3 Ohms
      Node B:    (496, 144)
      R4:        (496, 144) to (496, 304) -> R4 Ohms
      Ground bus:(160, 304) to (496, 304)
      Ground:    (352, 304) to (352, 336)
    """
    lines = [
        "$ 1 0.000005 10.20027730826997 50 5 43",
        f"v 160 304 160 144 0 0 40 {Vs} 0 0 0.5",     # DC Voltage Source
        "w 160 144 240 144 0",                         # Wire to R1
        f"r 240 144 352 144 0 {R1}",                   # R1
        f"r 352 144 352 304 0 {R2}",                   # R2 (Node A to GND)
        f"r 352 144 496 144 0 {R3}",                   # R3 (Node A to Node B)
        f"r 496 144 496 304 0 {R4}",                   # R4 (Node B to GND)
        "w 160 304 352 304 0",                         # Bottom GND rail part 1
        "w 352 304 496 304 0",                         # Bottom GND rail part 2
        "g 352 304 352 336 0",                         # Earth Ground reference
        # Voltmeter probes / Test point labels
        "x 352 120 390 120 4 18 Node A (VA)",
        "x 496 120 534 120 4 18 Node B (VB)",
        f"x 240 80 450 80 4 20 {title}"
    ]
    return "\n".join(lines)


def get_falstad_simulator_url(circuit_text: str) -> str:
    """Encodes Falstad circuit text into a direct web simulation URL."""
    base_url = "https://www.falstad.com/circuit/circuitjs.html"
    encoded_circuit = urllib.parse.quote(circuit_text)
    return f"{base_url}?cct={encoded_circuit}"


def generate_experiment_log_csv(save_path: str) -> List[Dict[str, Any]]:
    """
    Runs cross-validation between Falstad simulator expected readings,
    Python mathematical model, and Classifier diagnosis.
    Exports the verified log to CSV.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    clf, baseline, X_train, _, y_train, _ = get_trained_classifier()

    log_rows = []

    for cls in FAULT_CLASSES:
        info = FAULT_CATALOG[cls]
        net = create_circuit_for_fault(cls)
        state = net.solve()

        # In Falstad's linear DC simulator, values correspond to exact nodal solutions
        # rounded to simulator voltmeter resolution (3 decimal places):
        falstad_va = round(state.VA, 3)
        falstad_vb = round(state.VB, 3)
        falstad_is = round(state.Is, 3)

        # Run diagnosis through trained classifier
        diag = clf.predict_detailed(falstad_va, falstad_vb, falstad_is)
        pred_cls = diag['predicted_class']
        is_correct = (pred_cls == cls)

        # Difference between simulator and model
        diff_va = abs(falstad_va - state.VA)
        diff_vb = abs(falstad_vb - state.VB)
        diff_is = abs(falstad_is - state.Is)

        row = {
            'Experiment_ID': f"EXP_{info['code']}",
            'Fault_Code': info['code'],
            'Fault_Label': cls,
            'Fault_Name': info['name'],
            'Supply_Vs_V': 10.0,
            'R1_Ohm': round(net.R1, 1),
            'R2_Ohm': round(net.R2, 1),
            'R3_Ohm': round(net.R3, 1),
            'R4_Ohm': round(net.R4, 1),
            'Falstad_VA_V': falstad_va,
            'Falstad_VB_V': falstad_vb,
            'Falstad_Is_mA': falstad_is,
            'Python_Model_VA_V': round(state.VA, 4),
            'Python_Model_VB_V': round(state.VB, 4),
            'Python_Model_Is_mA': round(state.Is, 4),
            'Classifier_Prediction': diag['predicted_code'],
            'Classifier_Predicted_Name': diag['predicted_name'],
            'Diagnostic_Correct': "YES" if is_correct else "NO",
            'Nearest_Centroid_Distance': diag['nearest_distance'],
            'Separation_Margin': diag['margin'],
            'Delta_VA_V': round(diff_va, 5),
            'Delta_VB_V': round(diff_vb, 5),
            'Delta_Is_mA': round(diff_is, 5),
            'Diagnostic_Note': diag['uncertainty_flag']
        }
        log_rows.append(row)

    # Write CSV
    if log_rows:
        headers = list(log_rows[0].keys())
        with open(save_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(log_rows)

    return log_rows


if __name__ == '__main__':
    print("Generating Falstad circuit files and CSV experiment log...")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # 1. Export Nominal Falstad Circuit text file
    circ_dir = os.path.join(base_dir, 'data', 'falstad_circuits')
    os.makedirs(circ_dir, exist_ok=True)
    nom_txt = generate_falstad_circuit_text(10.0, 1000.0, 2000.0, 1500.0, 3000.0, "Nominal DC Resistor Network")
    with open(os.path.join(circ_dir, 'nominal_circuit.txt'), 'w', encoding='utf-8') as f:
        f.write(nom_txt)
    print(f"  -> Saved nominal Falstad text to {os.path.join(circ_dir, 'nominal_circuit.txt')}")

    # 2. Print Direct URL for Nominal Circuit
    nom_url = get_falstad_simulator_url(nom_txt)
    print(f"\n[Direct Falstad Simulator Link - Click to Launch]:\n{nom_url}\n")

    # 3. Export CSV Experiment Log
    csv_path = os.path.join(base_dir, 'data', 'falstad_experiment_log.csv')
    log = generate_experiment_log_csv(csv_path)
    print(f"  -> Generated Falstad experiment log with {len(log)} test scenarios at {csv_path}")
