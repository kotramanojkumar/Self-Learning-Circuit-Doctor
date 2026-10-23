"""
evaluation.py - Comprehensive Diagnostic Evaluation, Metrics, and Figure Generation
Part of 'Self-Learning Circuit Doctor: Voltage-Signature-Based Fault Detection in DC Circuits'
BEEE Project for B.Tech

Generates:
  1. Performance metrics: Accuracy, Precision, Recall, F1-Score, Confusion Matrix.
  2. Baseline vs. Standardized Nearest Centroid comparison.
  3. Sensitivity studies: Noise variation & Resistor tolerance variation.
  4. Publication-grade figures saved to figures/
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Headless backend for robust image generation
import matplotlib.pyplot as plt

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fault_scenarios import FAULT_CATALOG, FAULT_CLASSES
from src.dataset_generator import CircuitDatasetGenerator
from src.classifier import NearestCentroidClassifier, BaselineThresholdDetector


def compute_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, classes: list) -> np.ndarray:
    """Computes an N x N confusion matrix where rows are True and columns are Predicted."""
    n_classes = len(classes)
    cls_map = {c: i for i, c in enumerate(classes)}
    cm = np.zeros((n_classes, n_classes), dtype=int)
    for t, p in zip(y_true, y_pred):
        if t in cls_map and p in cls_map:
            cm[cls_map[t], cls_map[p]] += 1
    return cm


def compute_classification_report(y_true: np.ndarray, y_pred: np.ndarray, classes: list) -> dict:
    """Computes per-class precision, recall, f1-score, and support without sklearn dependency."""
    cm = compute_confusion_matrix(y_true, y_pred, classes)
    report = {}
    total_samples = len(y_true)
    correct_samples = np.sum(np.diag(cm))
    overall_accuracy = correct_samples / total_samples if total_samples > 0 else 0.0

    for i, cls in enumerate(classes):
        tp = cm[i, i]
        fp = np.sum(cm[:, i]) - tp
        fn = np.sum(cm[i, :]) - tp
        support = int(np.sum(cm[i, :]))

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        report[cls] = {
            'code': FAULT_CATALOG[cls]['code'],
            'name': FAULT_CATALOG[cls]['name'],
            'precision': round(float(precision), 4),
            'recall': round(float(recall), 4),
            'f1_score': round(float(f1), 4),
            'support': support
        }

    report['overall'] = {
        'accuracy': round(float(overall_accuracy), 4),
        'total_support': total_samples
    }
    return report


def plot_confusion_matrix(cm: np.ndarray, classes: list, title: str, save_path: str) -> None:
    """Generates and saves a publication-quality confusion matrix heatmap."""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)

    # Use fault codes for compact, clear axis labels
    labels = [FAULT_CATALOG[c]['code'] for c in classes]

    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=labels, yticklabels=labels,
           title=title,
           ylabel='True Physical Operating Class',
           xlabel='Predicted Operating Class')

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor", fontsize=9)
    plt.setp(ax.get_yticklabels(), fontsize=9)

    # Annotate counts in cells
    thresh = cm.max() / 2.0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            val = cm[i, j]
            ax.text(j, i, format(val, 'd'),
                    ha="center", va="center",
                    color="white" if val > thresh else "black",
                    fontsize=8, fontweight='bold' if val > 0 else 'normal')

    fig.tight_layout()
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()


def plot_voltage_signatures(save_path: str) -> None:
    """Plots comparative 3-signal signatures [VA, VB, Is] across all 13 operating classes."""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    codes = [FAULT_CATALOG[c]['code'] for c in FAULT_CLASSES]
    va_vals = [FAULT_CATALOG[c]['expected_va'] for c in FAULT_CLASSES]
    vb_vals = [FAULT_CATALOG[c]['expected_vb'] for c in FAULT_CLASSES]
    is_vals = [FAULT_CATALOG[c]['expected_is'] for c in FAULT_CLASSES]

    x = np.arange(len(codes))
    width = 0.26

    fig, ax1 = plt.subplots(figsize=(12, 5.5), dpi=300)

    # Voltages on left axis
    rects1 = ax1.bar(x - width, va_vals, width, label='Node A Voltage (VA)', color='#1f77b4')
    rects2 = ax1.bar(x, vb_vals, width, label='Node B Voltage (VB)', color='#2ca02c')
    ax1.set_ylabel('Voltage (Volts)', color='#1f77b4', fontsize=11, fontweight='bold')
    ax1.set_ylim(0, 11.5)
    ax1.tick_params(axis='y', labelcolor='#1f77b4')
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"{c}\n({FAULT_CATALOG[k]['name'][:10]}..)" for c, k in zip(codes, FAULT_CLASSES)],
                        rotation=30, ha='right', fontsize=8)

    # Current on right axis
    ax2 = ax1.twinx()
    rects3 = ax2.bar(x + width, is_vals, width, label='Source Current (Is)', color='#d62728', alpha=0.9)
    ax2.set_ylabel('Current (mA)', color='#d62728', fontsize=11, fontweight='bold')
    ax2.set_ylim(0, 11.5)
    ax2.tick_params(axis='y', labelcolor='#d62728')

    plt.title('Theoretical Multi-Signal Voltage & Current Signatures Across All 13 Fault Classes',
              fontsize=12, fontweight='bold', pad=15)
    
    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=0.9)
    ax1.grid(True, linestyle='--', alpha=0.4, axis='y')

    fig.tight_layout()
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()


def plot_sensitivity_studies(save_noise_path: str, save_tol_path: str) -> dict:
    """
    Evaluates classifier robustness against varying noise and component tolerance levels.
    """
    os.makedirs(os.path.dirname(save_noise_path), exist_ok=True)
    os.makedirs(os.path.dirname(save_tol_path), exist_ok=True)

    # 1. Measurement Noise Sensitivity Study
    # Test noise std from 0.01V to 0.20V
    noise_levels = [0.01, 0.02, 0.05, 0.08, 0.10, 0.15, 0.20]
    acc_clf_noise = []
    acc_base_noise = []

    for n in noise_levels:
        gen = CircuitDatasetGenerator(samples_per_class=100,
                                      resistor_tolerance_pct=5.0,
                                      voltage_meas_noise_std=n,
                                      current_meas_noise_std=n,
                                      random_seed=42)
        X_tr, X_te, y_tr, y_te, _, _ = gen.train_test_split(0.2)
        
        clf = NearestCentroidClassifier().fit(X_tr, y_tr)
        base = BaselineThresholdDetector()

        acc_c = np.mean(clf.predict(X_te) == y_te) * 100.0
        acc_b = np.mean(base.predict(X_te) == y_te) * 100.0
        acc_clf_noise.append(acc_c)
        acc_base_noise.append(acc_b)

    # Plot Noise Sensitivity
    plt.figure(figsize=(8, 5), dpi=300)
    plt.plot(noise_levels, acc_clf_noise, marker='o', linewidth=2.2, color='#1f77b4', label='Method B: Nearest Centroid')
    plt.plot(noise_levels, acc_base_noise, marker='s', linewidth=2.0, linestyle='--', color='#ff7f0e', label='Method A: Baseline Threshold')
    plt.title('Diagnostic Accuracy vs. Measurement Sensor Noise (DMM Noise)', fontsize=11, fontweight='bold')
    plt.xlabel('Sensor Measurement Noise Std Dev (Volts / mA)', fontsize=10)
    plt.ylabel('Diagnostic Accuracy (%)', fontsize=10)
    plt.ylim(70, 102)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='lower left')
    plt.tight_layout()
    plt.savefig(save_noise_path, bbox_inches='tight')
    plt.close()

    # 2. Resistor Tolerance Sensitivity Study
    # Test tolerances: 1%, 2%, 5%, 8%, 10%, 15%
    tol_levels = [1.0, 2.0, 5.0, 8.0, 10.0, 15.0]
    acc_clf_tol = []
    acc_base_tol = []

    for t in tol_levels:
        gen = CircuitDatasetGenerator(samples_per_class=100,
                                      resistor_tolerance_pct=t,
                                      voltage_meas_noise_std=0.02,
                                      current_meas_noise_std=0.02,
                                      random_seed=42)
        X_tr, X_te, y_tr, y_te, _, _ = gen.train_test_split(0.2)

        clf = NearestCentroidClassifier().fit(X_tr, y_tr)
        base = BaselineThresholdDetector()

        acc_c = np.mean(clf.predict(X_te) == y_te) * 100.0
        acc_b = np.mean(base.predict(X_te) == y_te) * 100.0
        acc_clf_tol.append(acc_c)
        acc_base_tol.append(acc_b)

    # Plot Tolerance Sensitivity
    plt.figure(figsize=(8, 5), dpi=300)
    plt.plot(tol_levels, acc_clf_tol, marker='^', linewidth=2.2, color='#2ca02c', label='Method B: Nearest Centroid')
    plt.plot(tol_levels, acc_base_tol, marker='d', linewidth=2.0, linestyle='--', color='#d62728', label='Method A: Baseline Threshold')
    plt.title('Diagnostic Accuracy vs. Component Manufacturing Tolerance', fontsize=11, fontweight='bold')
    plt.xlabel('Resistor Manufacturing Tolerance (%)', fontsize=10)
    plt.ylabel('Diagnostic Accuracy (%)', fontsize=10)
    plt.ylim(70, 102)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='lower left')
    plt.tight_layout()
    plt.savefig(save_tol_path, bbox_inches='tight')
    plt.close()

    return {
        'noise_study': {'levels': noise_levels, 'clf_acc': acc_clf_noise, 'base_acc': acc_base_noise},
        'tolerance_study': {'levels': tol_levels, 'clf_acc': acc_clf_tol, 'base_acc': acc_base_tol}
    }


def plot_circuit_schematic(save_path: str) -> None:
    """Draws a clean schematic diagram of the DC resistor network using matplotlib."""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 5.5)
    ax.axis('off')

    # Draw nodes and wires
    # DC Source at x=1.0, y=2.5
    ax.text(0.8, 3.8, "Vs = +10V\n(DC Source)", fontsize=10, fontweight='bold', color='#b22222', ha='center')
    ax.plot([1.0, 1.0], [0.5, 3.2], color='black', lw=2)  # Source line
    ax.plot([1.0, 2.2], [3.2, 3.2], color='black', lw=2)  # to R1

    # R1 (horizontal resistor) between (2.2, 3.2) and (3.8, 3.2)
    ax.plot([2.2, 3.8], [3.2, 3.2], color='#1f77b4', lw=6)
    ax.text(3.0, 3.6, "R1 = 1 kΩ", fontsize=10, fontweight='bold', ha='center', color='#1f77b4')

    # Node A at (4.5, 3.2)
    ax.plot([3.8, 5.2], [3.2, 3.2], color='black', lw=2)
    ax.plot(4.5, 3.2, 'ro', markersize=8)
    ax.text(4.5, 3.6, "Node A\n(VA)", fontsize=10, fontweight='bold', ha='center', color='red')

    # R2 (vertical resistor from Node A to GND)
    ax.plot([4.5, 4.5], [3.2, 2.4], color='black', lw=2)
    ax.plot([4.5, 4.5], [2.4, 1.2], color='#1f77b4', lw=6)
    ax.plot([4.5, 4.5], [1.2, 0.5], color='black', lw=2)
    ax.text(5.3, 1.8, "R2 = 2 kΩ", fontsize=10, fontweight='bold', ha='center', color='#1f77b4')

    # Wire from Node A to R3
    ax.plot([4.5, 5.8], [3.2, 3.2], color='black', lw=2)

    # R3 (horizontal resistor between Node A and Node B)
    ax.plot([5.8, 7.2], [3.2, 3.2], color='#1f77b4', lw=6)
    ax.text(6.5, 3.6, "R3 = 1.5 kΩ", fontsize=10, fontweight='bold', ha='center', color='#1f77b4')

    # Node B at (7.8, 3.2)
    ax.plot([7.2, 7.8], [3.2, 3.2], color='black', lw=2)
    ax.plot(7.8, 3.2, 'mo', markersize=8)
    ax.text(7.8, 3.6, "Node B\n(VB)", fontsize=10, fontweight='bold', ha='center', color='purple')

    # R4 (vertical resistor from Node B to GND)
    ax.plot([7.8, 7.8], [3.2, 2.4], color='black', lw=2)
    ax.plot([7.8, 7.8], [2.4, 1.2], color='#1f77b4', lw=6)
    ax.plot([7.8, 7.8], [1.2, 0.5], color='black', lw=2)
    ax.text(8.6, 1.8, "R4 = 3 kΩ", fontsize=10, fontweight='bold', ha='center', color='#1f77b4')

    # Common Ground rail at y=0.5
    ax.plot([0.5, 8.5], [0.5, 0.5], color='black', lw=2.5)
    ax.text(4.5, 0.05, "Common Reference Ground (0 V)", fontsize=10, fontweight='bold', ha='center', color='#333333')

    # Source Current Arrow
    ax.annotate("", xy=(2.0, 3.2), xytext=(1.2, 3.2),
                arrowprops=dict(arrowstyle="->", color="red", lw=2.5))
    ax.text(1.6, 2.7, "Is (mA)", fontsize=9, fontweight='bold', color="red", ha='center')

    # Title box
    ax.text(4.5, 5.0, "Circuit Schematic: Bridge/Ladder DC Resistor Network",
            fontsize=12, fontweight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.3", fc="#eef2f7", ec="#99aab5", lw=1.5))

    fig.tight_layout()
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()


def run_full_evaluation_pipeline() -> dict:
    """Executes the complete experimental evaluation pipeline and generates all result artifacts."""
    print("=" * 75)
    print("RUNNING FULL EXPERIMENTAL EVALUATION PIPELINE")
    print("=" * 75)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    fig_dir = os.path.join(base_dir, 'figures')
    results_dir = os.path.join(base_dir, 'results')
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    # 1. Generate Dataset
    print("\n[Stage 1/5] Generating reproducible synthetic dataset (N=1950, 150/class)...")
    gen = CircuitDatasetGenerator(samples_per_class=150, random_seed=42)
    X_train, X_test, y_train, y_test, train_recs, test_recs = gen.train_test_split(test_ratio=0.2)

    # 2. Train Models
    print("[Stage 2/5] Fitting Nearest-Centroid Classifier and Baseline Detector...")
    clf = NearestCentroidClassifier().fit(X_train, y_train)
    baseline = BaselineThresholdDetector()

    # 3. Test & Compute Metrics
    print("[Stage 3/5] Evaluating models on held-out test set (N=390, 30/class)...")
    y_pred_clf = clf.predict(X_test)
    y_pred_base = baseline.predict(X_test)

    cm_clf = compute_confusion_matrix(y_test, y_pred_clf, FAULT_CLASSES)
    cm_base = compute_confusion_matrix(y_test, y_pred_base, FAULT_CLASSES)

    rep_clf = compute_classification_report(y_test, y_pred_clf, FAULT_CLASSES)
    rep_base = compute_classification_report(y_test, y_pred_base, FAULT_CLASSES)

    acc_clf = rep_clf['overall']['accuracy'] * 100.0
    acc_base = rep_base['overall']['accuracy'] * 100.0

    print(f"  Method A (Baseline Detector) Accuracy : {acc_base:.2f}%")
    print(f"  Method B (Nearest Centroid) Accuracy : {acc_clf:.2f}%")

    # 4. Generate Figures
    print("\n[Stage 4/5] Generating publication-quality figures...")
    plot_circuit_schematic(os.path.join(fig_dir, 'circuit_schematic.png'))
    print("  -> Saved figures/circuit_schematic.png")

    plot_confusion_matrix(cm_clf, FAULT_CLASSES,
                          'Method B: Standardized Nearest Centroid Confusion Matrix',
                          os.path.join(fig_dir, 'confusion_matrix_classifier.png'))
    print("  -> Saved figures/confusion_matrix_classifier.png")

    plot_confusion_matrix(cm_base, FAULT_CLASSES,
                          'Method A: Baseline Threshold Detector Confusion Matrix',
                          os.path.join(fig_dir, 'confusion_matrix_baseline.png'))
    print("  -> Saved figures/confusion_matrix_baseline.png")

    plot_voltage_signatures(os.path.join(fig_dir, 'voltage_signatures_comparison.png'))
    print("  -> Saved figures/voltage_signatures_comparison.png")

    sensitivity_res = plot_sensitivity_studies(
        os.path.join(fig_dir, 'noise_sensitivity_curve.png'),
        os.path.join(fig_dir, 'tolerance_sensitivity_curve.png')
    )
    print("  -> Saved figures/noise_sensitivity_curve.png")
    print("  -> Saved figures/tolerance_sensitivity_curve.png")

    # 5. Export Metrics Summary to CSV/Text
    print("\n[Stage 5/5] Exporting evaluation results and tables...")
    metrics_path = os.path.join(results_dir, 'evaluation_summary.txt')
    with open(metrics_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("SELF-LEARNING CIRCUIT DOCTOR - COMPREHENSIVE EXPERIMENTAL RESULTS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total Dataset Size: {len(train_recs) + len(test_recs)} samples (13 classes, 150 samples/class)\n")
        f.write(f"Training Set Size : {len(train_recs)} samples (120 per class, 80%)\n")
        f.write(f"Testing Set Size  : {len(test_recs)} samples (30 per class, 20%)\n\n")
        f.write(f"OVERALL PERFORMANCE:\n")
        f.write(f"  Method A (Baseline Rule-Based Threshold Detector): {acc_base:.2f}% Accuracy\n")
        f.write(f"  Method B (Standardized Nearest Centroid Classifier): {acc_clf:.2f}% Accuracy\n\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Code':<6} {'Operating Condition':<24} {'Precision':<10} {'Recall':<10} {'F1-Score':<10} {'Support'}\n")
        f.write("-" * 80 + "\n")
        for cls in FAULT_CLASSES:
            info = rep_clf[cls]
            f.write(f"{info['code']:<6} {info['name']:<24} {info['precision']:<10.4f} {info['recall']:<10.4f} {info['f1_score']:<10.4f} {info['support']}\n")
        f.write("-" * 80 + "\n")
    print(f"  -> Saved results to {metrics_path}")

    return {
        'rep_clf': rep_clf,
        'rep_base': rep_base,
        'cm_clf': cm_clf,
        'cm_base': cm_base,
        'sensitivity': sensitivity_res,
        'acc_clf': acc_clf,
        'acc_base': acc_base
    }


if __name__ == '__main__':
    run_full_evaluation_pipeline()
