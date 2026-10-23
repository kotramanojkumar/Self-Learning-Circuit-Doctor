"""
classifier.py - Baseline Threshold Detector and Standardized Nearest-Centroid Classifier
Part of 'Self-Learning Circuit Doctor: Voltage-Signature-Based Fault Detection in DC Circuits'
BEEE Project for B.Tech

Methods:
  Method A: Baseline Threshold Detector (Rule-based with engineering tolerances)
  Method B: Voltage-Signature Nearest-Centroid Classifier (Standardized Euclidean Metric)
            + Supervised Self-Learning (Incremental Online Adaptation)
"""

import os
import sys
import numpy as np
from typing import Dict, Any, List, Tuple, Optional

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fault_scenarios import FAULT_CATALOG, FAULT_CLASSES


class BaselineThresholdDetector:
    """
    Method A: Baseline Rule-Based Diagnostic System.
    
    Uses physical circuit rules derived from Kirchhoff's Laws and nominal thresholds.
    Nominal Reference Signatures:
      F0 (Normal):   VA ~ 5.81V, VB ~ 3.87V, Is ~ 4.19mA
      F1 (R1 Open):  VA ~ 0.00V, VB ~ 0.00V, Is ~ 0.00mA (complete disconnect)
      F2 (R2 Open):  VA ~ 8.18V, VB ~ 5.45V, Is ~ 1.82mA
      F3 (R3 Open):  VA ~ 6.67V, VB ~ 0.00V, Is ~ 3.33mA
      F4 (R4 Open):  VA ~ 6.67V, VB ~ 6.67V, Is ~ 3.33mA
      F5 (R1 Short): VA ~ 10.0V, VB ~ 6.67V, Is ~ 7.22mA
      F6 (R2 Short): VA ~ 0.00V, VB ~ 0.00V, Is ~ 10.0mA
      F7 (R3 Short): VA ~ 5.45V, VB ~ 5.45V, Is ~ 4.55mA
      F8 (R4 Short): VA ~ 4.62V, VB ~ 0.00V, Is ~ 5.38mA
      Drift Faults:  F9 (R1+50%), F10 (R2+50%), F11 (R3-50%), F12 (R4-50%)
    
    Decision Rules:
      1. Hard boundary checks for extreme open/short states (e.g. Is < 0.1mA -> R1 Open; Is > 9.0mA -> R2 Short).
      2. Equipotential checks (VA == VB within margin -> R4 Open or R3 Short).
      3. For subtle drift faults, maps to minimum normalized distance relative to nominal references.
    """

    def __init__(self, tolerance_pct: float = 7.5):
        self.tolerance_pct = tolerance_pct
        self.nominal_signatures = {
            k: np.array([v['expected_va'], v['expected_vb'], v['expected_is']], dtype=float)
            for k, v in FAULT_CATALOG.items()
        }
        # Engineering scale weights to balance voltage (Volts) and current (mA)
        self.scale_weights = np.array([1.0 / 10.0, 1.0 / 10.0, 1.0 / 10.0])

    def predict_single(self, va: float, vb: float, is_ma: float) -> Dict[str, Any]:
        """Diagnoses a single measurement vector [VA, VB, Is] using baseline logic."""
        meas = np.array([va, vb, is_ma], dtype=float)

        # Rule 1: No supply current -> R1 Open
        if is_ma < 0.2 and va < 0.2 and vb < 0.2:
            return {
                'predicted_class': 'F1_R1_OPEN',
                'method': 'Baseline Rule (Current Cutoff)',
                'confidence_note': 'High confidence: complete circuit de-energization detected.',
                'distance': 0.0,
                'margin': 5.0
            }

        # Rule 2: Clamped to 0V with high current -> R2 Short
        if va < 0.2 and vb < 0.2 and is_ma > 8.5:
            return {
                'predicted_class': 'F6_R2_SHORT',
                'method': 'Baseline Rule (GND Clamp & Overcurrent)',
                'confidence_note': 'High confidence: Node A shorted to ground causing maximum R1 current.',
                'distance': 0.0,
                'margin': 5.0
            }

        # Rule 3: Node A clamped to 10V -> R1 Short
        if va > 9.5:
            return {
                'predicted_class': 'F5_R1_SHORT',
                'method': 'Baseline Rule (Supply Clamping)',
                'confidence_note': 'High confidence: Node A connected directly to +10V rail.',
                'distance': 0.0,
                'margin': 3.0
            }

        # Rule 4: Node B grounded (0V) with active Node A
        if vb < 0.2 and va > 1.0:
            if va > 6.0:
                return {
                    'predicted_class': 'F3_R3_OPEN',
                    'method': 'Baseline Rule (Bridge Isolation)',
                    'confidence_note': 'High confidence: Node B decoupled from Node A while Node A floats at divider voltage.',
                    'distance': 0.0,
                    'margin': 2.0
                }
            else:
                return {
                    'predicted_class': 'F8_R4_SHORT',
                    'method': 'Baseline Rule (Node B Grounding)',
                    'confidence_note': 'High confidence: Node B clamped to ground with active Node A.',
                    'distance': 0.0,
                    'margin': 2.0
                }

        # Rule 5: Node A and Node B equipotential (VA ~ VB)
        if abs(va - vb) < 0.25:
            if va > 6.0:
                return {
                    'predicted_class': 'F4_R4_OPEN',
                    'method': 'Baseline Rule (Floating Node B)',
                    'confidence_note': 'Node B pull-down lost, floating up to match Node A.',
                    'distance': 0.0,
                    'margin': 1.5
                }
            elif 5.0 <= va <= 5.8:
                return {
                    'predicted_class': 'F7_R3_SHORT',
                    'method': 'Baseline Rule (Bridge Equipotential)',
                    'confidence_note': 'R3 shorted, merging Node A and Node B.',
                    'distance': 0.0,
                    'margin': 1.5
                }

        # Fallback / Drift analysis: Minimum weighted distance to nominal theoretical signatures
        distances = {}
        for cls_name, nom_sig in self.nominal_signatures.items():
            diff = (meas - nom_sig) * self.scale_weights
            distances[cls_name] = float(np.linalg.norm(diff))

        sorted_dist = sorted(distances.items(), key=lambda x: x[1])
        best_cls, best_d = sorted_dist[0]
        second_cls, second_d = sorted_dist[1]
        margin = second_d - best_d

        return {
            'predicted_class': best_cls,
            'method': 'Baseline Minimum Nominal Distance',
            'confidence_note': f"Distance to nominal: {best_d:.4f}, margin to {second_cls}: {margin:.4f}",
            'distance': round(best_d, 4),
            'margin': round(margin, 4)
        }

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Batch prediction over 2D array X of shape (N, 3)."""
        preds = []
        for i in range(len(X)):
            res = self.predict_single(X[i, 0], X[i, 1], X[i, 2])
            preds.append(res['predicted_class'])
        return np.array(preds, dtype=object)


class NearestCentroidClassifier:
    """
    Method B: Standardized Nearest-Centroid Classifier.
    
    Mathematical Formulation:
      1. Feature Standardization:
         mu_j = (1 / N) * sum(X_ij)
         sigma_j = sqrt((1 / N) * sum((X_ij - mu_j)^2))
         Z_ij = (X_ij - mu_j) / sigma_j
         
      2. Centroid Calculation (Training Phase):
         C_c = (1 / N_c) * sum_{i in class c} (Z_i)
         
      3. Query Classification (Inference Phase):
         For test query x = [VA, VB, Is]:
           z = (x - mu) / sigma
           d_c = || z - C_c ||_2 = sqrt( sum_j (z_j - C_cj)^2 )
           y_pred = argmin_c (d_c)
           
      4. Diagnostic Ambiguity & Margin:
         margin = d_second - d_nearest
         If margin < AMBIGUITY_THRESHOLD, flag as diagnostic uncertainty.
         
      5. Incremental Self-Learning Update:
         When a new verified labelled sample (x_new, y_new) is provided:
           z_new = (x_new - mu) / sigma
           N_c <- N_c + 1
           C_c <- C_c + (1 / N_c) * (z_new - C_c)
    """

    AMBIGUITY_THRESHOLD = 0.35  # Standardized distance threshold for borderline predictions

    def __init__(self):
        self.classes_: List[str] = []
        self.class_to_idx: Dict[str, int] = {}
        self.idx_to_class: Dict[int, str] = {}
        self.means_: Optional[np.ndarray] = None          # (3,)
        self.stds_: Optional[np.ndarray] = None           # (3,)
        self.centroids_: Optional[np.ndarray] = None      # (n_classes, 3) in standardized space
        self.raw_centroids_: Optional[np.ndarray] = None  # (n_classes, 3) in physical space
        self.class_counts_: Optional[np.ndarray] = None   # (n_classes,)
        self.is_fitted: bool = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'NearestCentroidClassifier':
        """
        Fits the classifier strictly using training data only.
        
        Args:
            X: Training feature matrix of shape (N, 3) with columns [VA, VB, Is].
            y: Training class labels of shape (N,).
        """
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=object)

        if len(X) != len(y):
            raise ValueError(f"Features and labels count mismatch: {len(X)} != {len(y)}")

        self.classes_ = sorted(list(np.unique(y)))
        n_classes = len(self.classes_)
        self.class_to_idx = {c: i for i, c in enumerate(self.classes_)}
        self.idx_to_class = {i: c for i, c in enumerate(self.classes_)}

        # 1. Compute Standardization Parameters from TRAINING DATA ONLY
        self.means_ = np.mean(X, axis=0)
        self.stds_ = np.std(X, axis=0)
        # Avoid division by zero
        self.stds_[self.stds_ < 1e-8] = 1.0

        # Standardize training features
        Z = (X - self.means_) / self.stds_

        # 2. Compute Centroids for each class
        self.centroids_ = np.zeros((n_classes, 3), dtype=float)
        self.raw_centroids_ = np.zeros((n_classes, 3), dtype=float)
        self.class_counts_ = np.zeros(n_classes, dtype=int)

        for i, c in enumerate(self.classes_):
            mask = (y == c)
            self.class_counts_[i] = np.sum(mask)
            if self.class_counts_[i] == 0:
                raise ValueError(f"Class '{c}' has 0 training samples!")
            self.centroids_[i] = np.mean(Z[mask], axis=0)
            self.raw_centroids_[i] = np.mean(X[mask], axis=0)

        self.is_fitted = True
        return self

    def predict_detailed(self, va: float, vb: float, is_ma: float) -> Dict[str, Any]:
        """
        Performs inference on a single measurement and returns diagnostic telemetry:
          - Predicted class code and descriptive name
          - Distance to nearest centroid
          - Runner-up class and distance
          - Separation margin
          - Ambiguity / uncertainty indicator
          - Ranked candidate list
        """
        if not self.is_fitted:
            raise RuntimeError("Classifier has not been fitted! Call fit(X_train, y_train) first.")

        x = np.array([va, vb, is_ma], dtype=float)
        # Standardize query sample
        z = (x - self.means_) / self.stds_

        # Compute Euclidean distance to all class centroids
        diffs = self.centroids_ - z  # shape (n_classes, 3)
        distances = np.linalg.norm(diffs, axis=1)  # shape (n_classes,)

        # Sort classes by standardized distance
        sorted_indices = np.argsort(distances)
        best_idx = sorted_indices[0]
        second_idx = sorted_indices[1]

        best_class = self.idx_to_class[best_idx]
        best_dist = float(distances[best_idx])
        second_class = self.idx_to_class[second_idx]
        second_dist = float(distances[second_idx])
        margin = second_dist - best_dist

        # Cautious indication of diagnostic uncertainty
        is_uncertain = (margin < self.AMBIGUITY_THRESHOLD)

        # Ranked list of top 3 candidates
        ranked_candidates = []
        for idx in sorted_indices[:3]:
            c_key = self.idx_to_class[idx]
            ranked_candidates.append({
                'class': c_key,
                'code': FAULT_CATALOG[c_key]['code'],
                'name': FAULT_CATALOG[c_key]['name'],
                'distance': round(float(distances[idx]), 4),
                'raw_centroid': self.raw_centroids_[idx].tolist()
            })

        return {
            'predicted_class': best_class,
            'predicted_code': FAULT_CATALOG[best_class]['code'],
            'predicted_name': FAULT_CATALOG[best_class]['name'],
            'description': FAULT_CATALOG[best_class]['description'],
            'nearest_distance': round(best_dist, 4),
            'second_class': second_class,
            'second_name': FAULT_CATALOG[second_class]['name'],
            'second_distance': round(second_dist, 4),
            'margin': round(margin, 4),
            'is_uncertain': is_uncertain,
            'uncertainty_flag': 'CAUTION: Ambiguous / Borderline Diagnosis' if is_uncertain else 'Clear Separation',
            'ranked_candidates': ranked_candidates,
            'measured_values': {'VA': round(va, 4), 'VB': round(vb, 4), 'Is': round(is_ma, 4)},
            'standardized_z': z.tolist()
        }

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Batch prediction over 2D array X of shape (N, 3)."""
        if not self.is_fitted:
            raise RuntimeError("Classifier has not been fitted! Call fit(X_train, y_train) first.")
        X = np.asarray(X, dtype=float)
        Z = (X - self.means_) / self.stds_

        # Vectorized Euclidean distance calculation: shape (N, n_classes)
        # ||Z_i - C_j||^2 = sum((Z_i - C_j)^2)
        # Using broadcasting:
        diff = Z[:, np.newaxis, :] - self.centroids_[np.newaxis, :, :]
        dist_matrix = np.linalg.norm(diff, axis=2)
        best_indices = np.argmin(dist_matrix, axis=1)

        return np.array([self.idx_to_class[i] for i in best_indices], dtype=object)

    def update_with_sample(self, va: float, vb: float, is_ma: float, true_class: str) -> Dict[str, Any]:
        """
        Incremental Supervised Self-Learning:
        Updates the class centroid in real time when a confirmed labelled sample is provided.
        Preserves model integrity and avoids retraining from scratch.
        """
        if not self.is_fitted:
            raise RuntimeError("Classifier must be fitted before incremental updates.")
        if true_class not in self.class_to_idx:
            raise KeyError(f"Unknown class '{true_class}'. Must be one of {self.classes_}")

        cls_idx = self.class_to_idx[true_class]
        x_new = np.array([va, vb, is_ma], dtype=float)
        z_new = (x_new - self.means_) / self.stds_

        old_count = self.class_counts_[cls_idx]
        new_count = old_count + 1
        self.class_counts_[cls_idx] = new_count

        # Incremental moving average formula:
        # C_new = C_old + (1 / N_new) * (z_new - C_old)
        old_centroid = self.centroids_[cls_idx].copy()
        delta = (z_new - old_centroid) / new_count
        self.centroids_[cls_idx] = old_centroid + delta

        # Also update raw centroid
        self.raw_centroids_[cls_idx] = self.raw_centroids_[cls_idx] + (x_new - self.raw_centroids_[cls_idx]) / new_count

        drift_norm = float(np.linalg.norm(delta))

        return {
            'status': 'success',
            'updated_class': true_class,
            'previous_sample_count': int(old_count),
            'new_sample_count': int(new_count),
            'centroid_shift_norm': round(drift_norm, 6),
            'new_standardized_centroid': self.centroids_[cls_idx].tolist(),
            'new_physical_centroid': self.raw_centroids_[cls_idx].tolist()
        }


def get_trained_classifier(data_dir: Optional[str] = None) -> Tuple[NearestCentroidClassifier, BaselineThresholdDetector, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Helper factory to load data and return trained models ready for evaluation/app use."""
    from src.dataset_generator import CircuitDatasetGenerator
    gen = CircuitDatasetGenerator(samples_per_class=150, random_seed=42)
    X_train, X_test, y_train, y_test, _, _ = gen.train_test_split(test_ratio=0.2)

    clf = NearestCentroidClassifier()
    clf.fit(X_train, y_train)

    baseline = BaselineThresholdDetector()

    return clf, baseline, X_train, X_test, y_train, y_test


if __name__ == '__main__':
    print("=" * 70)
    print("EVALUATING CLASSIFIER MODULE")
    print("=" * 70)
    clf, baseline, X_train, X_test, y_train, y_test = get_trained_classifier()
    print(f"NearestCentroidClassifier successfully trained on {len(X_train)} samples across {len(clf.classes_)} classes.")
    
    # Test on nominal point
    diag = clf.predict_detailed(5.8065, 3.8710, 4.1935)
    print("\n--- Diagnostic Test on Nominal Circuit [5.81V, 3.87V, 4.19mA] ---")
    print(f"Prediction: {diag['predicted_code']} ({diag['predicted_name']})")
    print(f"Nearest Centroid Distance: {diag['nearest_distance']}")
    print(f"Runner-up: {diag['second_name']} (Distance: {diag['second_distance']})")
    print(f"Margin: {diag['margin']} | Status: {diag['uncertainty_flag']}")

    # Quick test on test set
    y_pred_clf = clf.predict(X_test)
    acc_clf = np.mean(y_pred_clf == y_test) * 100.0

    y_pred_base = baseline.predict(X_test)
    acc_base = np.mean(y_pred_base == y_test) * 100.0

    print(f"\nTest Set Performance (N={len(X_test)}):")
    print(f"  Method A (Baseline Threshold Detector)      : {acc_base:.2f}% Accuracy")
    print(f"  Method B (Standardized Nearest Centroid)   : {acc_clf:.2f}% Accuracy")
    print("=" * 70)
