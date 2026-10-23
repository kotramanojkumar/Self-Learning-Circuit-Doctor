"""
test_classifier.py - Unit Tests for Fault Diagnosis Algorithms
Part of 'Self-Learning Circuit Doctor: Voltage-Signature-Based Fault Detection in DC Circuits'
"""

import sys
import os
import pytest
import numpy as np

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fault_scenarios import FAULT_CATALOG, FAULT_CLASSES
from src.dataset_generator import CircuitDatasetGenerator
from src.classifier import NearestCentroidClassifier, BaselineThresholdDetector


@pytest.fixture(scope="module")
def prepared_dataset():
    """Provides a deterministic stratified dataset for testing."""
    gen = CircuitDatasetGenerator(samples_per_class=50, random_seed=42)
    X_train, X_test, y_train, y_test, _, _ = gen.train_test_split(test_ratio=0.2)
    return X_train, X_test, y_train, y_test


class TestBaselineThresholdDetector:
    """Tests for Method A: Baseline Rule-Based Detector."""

    def test_nominal_signature_predictions(self):
        detector = BaselineThresholdDetector()
        for cls_name, info in FAULT_CATALOG.items():
            res = detector.predict_single(info['expected_va'], info['expected_vb'], info['expected_is'])
            assert res['predicted_class'] == cls_name, f"Failed on {cls_name}: got {res['predicted_class']}"

    def test_distinguish_r1_open_vs_r2_short(self):
        """Both have VA=0V, VB=0V, but Is is 0mA vs 10mA."""
        detector = BaselineThresholdDetector()
        r1_open = detector.predict_single(0.0, 0.0, 0.0)
        r2_short = detector.predict_single(0.0, 0.0, 10.0)

        assert r1_open['predicted_class'] == 'F1_R1_OPEN'
        assert r2_short['predicted_class'] == 'F6_R2_SHORT'

    def test_batch_prediction_shape(self, prepared_dataset):
        X_train, X_test, y_train, y_test = prepared_dataset
        detector = BaselineThresholdDetector()
        preds = detector.predict(X_test)
        assert len(preds) == len(X_test)


class TestNearestCentroidClassifier:
    """Tests for Method B: Standardized Nearest Centroid Classifier."""

    def test_fit_and_standardization(self, prepared_dataset):
        X_train, X_test, y_train, y_test = prepared_dataset
        clf = NearestCentroidClassifier()
        clf.fit(X_train, y_train)

        assert clf.is_fitted is True
        assert len(clf.classes_) == 13
        assert clf.means_.shape == (3,)
        assert clf.stds_.shape == (3,)
        assert clf.centroids_.shape == (13, 3)

        # Standardized centroids must have zero mean across columns
        # (approximately zero mean weighted by class sizes)
        assert np.all(clf.stds_ > 0.0)

    def test_predict_detailed_telemetry(self, prepared_dataset):
        X_train, X_test, y_train, y_test = prepared_dataset
        clf = NearestCentroidClassifier().fit(X_train, y_train)

        diag = clf.predict_detailed(5.8065, 3.8710, 4.1935)
        assert diag['predicted_class'] == 'F0_NORMAL'
        assert diag['predicted_code'] == 'F0'
        assert 'nearest_distance' in diag
        assert 'second_class' in diag
        assert 'margin' in diag
        assert diag['margin'] >= 0.0
        assert len(diag['ranked_candidates']) == 3

    def test_incremental_self_learning_update(self, prepared_dataset):
        X_train, X_test, y_train, y_test = prepared_dataset
        clf = NearestCentroidClassifier().fit(X_train, y_train)

        target_cls = 'F0_NORMAL'
        cls_idx = clf.class_to_idx[target_cls]
        old_count = clf.class_counts_[cls_idx]
        old_centroid = clf.centroids_[cls_idx].copy()

        # Submit a new training sample
        update_res = clf.update_with_sample(5.85, 3.90, 4.22, target_cls)

        assert update_res['status'] == 'success'
        assert clf.class_counts_[cls_idx] == old_count + 1
        assert update_res['centroid_shift_norm'] > 0.0
        assert not np.array_equal(clf.centroids_[cls_idx], old_centroid)

    def test_unfitted_model_raises_runtime_error(self):
        clf = NearestCentroidClassifier()
        with pytest.raises(RuntimeError):
            clf.predict_detailed(5.0, 3.0, 4.0)

    def test_high_accuracy_on_held_out_test_set(self, prepared_dataset):
        X_train, X_test, y_train, y_test = prepared_dataset
        clf = NearestCentroidClassifier().fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        acc = np.mean(y_pred == y_test) * 100.0
        assert acc >= 95.0, f"Expected accuracy >= 95%, got {acc:.2f}%"


if __name__ == '__main__':
    pytest.main(['-v', __file__])
