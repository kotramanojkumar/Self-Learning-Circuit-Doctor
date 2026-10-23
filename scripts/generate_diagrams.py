"""
generate_diagrams.py - Generates System Architecture and Diagnostic Flowchart diagrams.
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_system_architecture(output_path):
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    # Background color
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    # Color Palette
    c_navy = '#1A365D'
    c_blue = '#2B6CB0'
    c_light_blue = '#EBF8FF'
    c_teal = '#2C7A7B'
    c_light_teal = '#E6FFFA'
    c_amber = '#C05621'
    c_light_amber = '#FFFAF0'
    c_purple = '#553C9A'
    c_light_purple = '#FAF5FF'

    # Title
    ax.text(5.0, 5.15, "Self-Learning Circuit Doctor: System Architecture", 
            ha='center', va='center', fontsize=14, fontweight='bold', color=c_navy)

    # Box 1: Circuit Simulation & Physical Modeling
    box1 = patches.FancyBboxPatch((0.4, 1.2), 2.0, 3.4, boxstyle="round,pad=0.15", 
                                  fc=c_light_blue, ec=c_blue, lw=1.8)
    ax.add_patch(box1)
    ax.text(1.4, 4.3, "1. Circuit Engine", ha='center', va='center', fontsize=11, fontweight='bold', color=c_navy)
    ax.text(1.4, 3.4, "• DC Resistor Ladder\n  (Vs=10V, R1-R4)\n• Falstad SPICE (MNA)\n• Python Closed-Form\n• 13 Fault Scenarios\n  (Opens, Shorts, Drifts)\n• Tolerances (5%)", 
            ha='center', va='center', fontsize=8.5, color='#2D3748', linespacing=1.4)

    # Arrow 1 -> 2
    ax.annotate('', xy=(2.7, 2.9), xytext=(2.4, 2.9),
                arrowprops=dict(arrowstyle="-|>", color=c_blue, lw=2.2, mutation_scale=15))

    # Box 2: Multi-Signal Sensing & Feature Extraction
    box2 = patches.FancyBboxPatch((2.7, 1.2), 2.0, 3.4, boxstyle="round,pad=0.15", 
                                  fc=c_light_teal, ec=c_teal, lw=1.8)
    ax.add_patch(box2)
    ax.text(3.7, 4.3, "2. Signature Sensing", ha='center', va='center', fontsize=11, fontweight='bold', color=c_teal)
    ax.text(3.7, 3.4, "• Node A Voltage (VA)\n• Node B Voltage (VB)\n• Source Current (Is)\n• Sensor Noise Injection\n  (Gaussian 10mV/0.1mA)\n• 3D Feature Vector:\n  X = [VA, VB, Is]", 
            ha='center', va='center', fontsize=8.5, color='#2D3748', linespacing=1.4)

    # Arrow 2 -> 3
    ax.annotate('', xy=(5.0, 2.9), xytext=(4.7, 2.9),
                arrowprops=dict(arrowstyle="-|>", color=c_teal, lw=2.2, mutation_scale=15))

    # Box 3: Machine Learning Diagnostic Core
    box3 = patches.FancyBboxPatch((5.0, 1.2), 2.3, 3.4, boxstyle="round,pad=0.15", 
                                  fc=c_light_amber, ec=c_amber, lw=1.8)
    ax.add_patch(box3)
    ax.text(6.15, 4.3, "3. Diagnostic Core", ha='center', va='center', fontsize=11, fontweight='bold', color=c_amber)
    ax.text(6.15, 3.4, "• Z-Score Standardization\n  (mu, sigma from train)\n• Nearest-Centroid Model\n• Minimum Distance d_min\n• Margin: Delta_d = d2 - d1\n• Uncertainty Flagging\n• Supervised Online\n  Centroid Adaptation", 
            ha='center', va='center', fontsize=8.5, color='#2D3748', linespacing=1.4)

    # Arrow 3 -> 4
    ax.annotate('', xy=(7.6, 2.9), xytext=(7.3, 2.9),
                arrowprops=dict(arrowstyle="-|>", color=c_amber, lw=2.2, mutation_scale=15))

    # Box 4: Interactive Deployment & Human Interface
    box4 = patches.FancyBboxPatch((7.6, 1.2), 2.0, 3.4, boxstyle="round,pad=0.15", 
                                  fc=c_light_purple, ec=c_purple, lw=1.8)
    ax.add_patch(box4)
    ax.text(8.6, 4.3, "4. Deployment & UI", ha='center', va='center', fontsize=11, fontweight='bold', color=c_purple)
    ax.text(8.6, 3.4, "• Streamlit Web App\n• Tkinter Desktop GUI\n• Live Telemetry Display\n• Fault State Prediction\n• Confidence Indicator\n• 1-Click Falstad Link\n• Streaming Lab Sample\n  Ingestion Form", 
            ha='center', va='center', fontsize=8.5, color='#2D3748', linespacing=1.4)

    # Feedback loop for online self-learning
    ax.annotate('', xy=(6.15, 1.2), xytext=(8.6, 1.2),
                arrowprops=dict(arrowstyle="-|>", color='#718096', lw=1.5, ls='--',
                                connectionstyle="arc3,rad=-0.3", mutation_scale=12))
    ax.text(7.35, 0.45, "Supervised Streaming Self-Learning Feedback Loop", 
            ha='center', va='center', fontsize=8, fontstyle='italic', color='#4A5568')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"System architecture saved to: {output_path}")

def generate_diagnostic_flowchart(output_path):
    fig, ax = plt.subplots(figsize=(8, 7.5), dpi=300)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 10)
    ax.axis('off')

    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    c_navy = '#1A365D'
    c_blue = '#2B6CB0'
    c_green = '#276749'
    c_amber = '#C05621'
    c_box_bg = '#FFFFFF'

    ax.text(4.0, 9.6, "Fault Diagnosis & Classification Flowchart", 
            ha='center', va='center', fontsize=13, fontweight='bold', color=c_navy)

    # Node 1: Start
    start_box = patches.FancyBboxPatch((2.8, 8.8), 2.4, 0.5, boxstyle="round,pad=0.1", fc='#E2E8F0', ec='#718096', lw=1.5)
    ax.add_patch(start_box)
    ax.text(4.0, 9.05, "START: Circuit State Ingestion", ha='center', va='center', fontsize=9, fontweight='bold', color='#1A202C')

    # Arrow 1
    ax.annotate('', xy=(4.0, 8.2), xytext=(4.0, 8.8), arrowprops=dict(arrowstyle="-|>", color='#4A5568', lw=1.5))

    # Node 2: Acquire Measurements
    p2 = patches.FancyBboxPatch((2.0, 7.5), 4.0, 0.7, boxstyle="round,pad=0.1", fc='#EBF8FF', ec=c_blue, lw=1.5)
    ax.add_patch(p2)
    ax.text(4.0, 7.85, "Measure Signature Vector:\nX = [VA (V), VB (V), Is (mA)]", ha='center', va='center', fontsize=9, fontweight='bold', color=c_navy)

    # Arrow 2
    ax.annotate('', xy=(4.0, 6.9), xytext=(4.0, 7.5), arrowprops=dict(arrowstyle="-|>", color='#4A5568', lw=1.5))

    # Node 3: Feature Standardization
    p3 = patches.FancyBboxPatch((2.2, 6.2), 3.6, 0.7, boxstyle="round,pad=0.1", fc='#FEFCBF', ec='#B7791F', lw=1.5)
    ax.add_patch(p3)
    ax.text(4.0, 6.55, "Standardize Features:\nZ_j = (X_j - mu_j) / sigma_j", ha='center', va='center', fontsize=9, fontweight='bold', color='#744210')

    # Arrow 3
    ax.annotate('', xy=(4.0, 5.6), xytext=(4.0, 6.2), arrowprops=dict(arrowstyle="-|>", color='#4A5568', lw=1.5))

    # Node 4: Compute Euclidean Distances
    p4 = patches.FancyBboxPatch((2.0, 4.9), 4.0, 0.7, boxstyle="round,pad=0.1", fc='#E6FFFA', ec='#319795', lw=1.5)
    ax.add_patch(p4)
    ax.text(4.0, 5.25, "Compute Standardized Euclidean Distances:\nd_k = || Z - mu_k || for all 13 Classes", ha='center', va='center', fontsize=9, fontweight='bold', color='#234E52')

    # Arrow 4
    ax.annotate('', xy=(4.0, 4.3), xytext=(4.0, 4.9), arrowprops=dict(arrowstyle="-|>", color='#4A5568', lw=1.5))

    # Node 5: Sort Distances & Margin
    p5 = patches.FancyBboxPatch((1.8, 3.6), 4.4, 0.7, boxstyle="round,pad=0.1", fc='#FAF5FF', ec='#805AD5', lw=1.5)
    ax.add_patch(p5)
    ax.text(4.0, 3.95, "Find Best Class: c* = argmin(d_k)\nSeparation Margin: Delta_d = d_second - d_min", ha='center', va='center', fontsize=9, fontweight='bold', color='#44337A')

    # Arrow 5
    ax.annotate('', xy=(4.0, 3.0), xytext=(4.0, 3.6), arrowprops=dict(arrowstyle="-|>", color='#4A5568', lw=1.5))

    # Decision Diamond: Margin Check
    diamond = patches.Polygon([[4.0, 3.0], [5.6, 2.3], [4.0, 1.6], [2.4, 2.3]], closed=True, 
                              fc='#FFF5F5', ec='#E53E3E', lw=1.5)
    ax.add_patch(diamond)
    ax.text(4.0, 2.3, "Is Delta_d >= 0.35\n(Margin Check)?", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#9B2C2C')

    # Decision Arrows: Yes -> Confident, No -> Caution
    ax.annotate('', xy=(6.5, 2.3), xytext=(5.6, 2.3), arrowprops=dict(arrowstyle="-|>", color=c_green, lw=1.5))
    ax.text(6.0, 2.5, "YES", ha='center', va='center', fontsize=8, fontweight='bold', color=c_green)

    ax.annotate('', xy=(1.5, 2.3), xytext=(2.4, 2.3), arrowprops=dict(arrowstyle="-|>", color=c_amber, lw=1.5))
    ax.text(2.0, 2.5, "NO", ha='center', va='center', fontsize=8, fontweight='bold', color=c_amber)

    # Box Confident
    b_conf = patches.FancyBboxPatch((6.2, 0.8), 1.6, 1.1, boxstyle="round,pad=0.1", fc='#F0FFF4', ec=c_green, lw=1.5)
    ax.add_patch(b_conf)
    ax.text(7.0, 1.35, "Output Prediction:\nCLEAR\nSEPARATION\nConfidence: High", ha='center', va='center', fontsize=7.5, fontweight='bold', color=c_green)

    # Box Caution
    b_caut = patches.FancyBboxPatch((0.2, 0.8), 1.6, 1.1, boxstyle="round,pad=0.1", fc='#FFFAF0', ec=c_amber, lw=1.5)
    ax.add_patch(b_caut)
    ax.text(1.0, 1.35, "Output Prediction:\nBORDERLINE /\nAMBIGUOUS\nFlag Uncertainty", ha='center', va='center', fontsize=7.5, fontweight='bold', color=c_amber)

    # Arrows to Final Display
    ax.annotate('', xy=(4.0, 0.8), xytext=(6.2, 1.35), arrowprops=dict(arrowstyle="-|>", color='#718096', lw=1.2))
    ax.annotate('', xy=(4.0, 0.8), xytext=(1.8, 1.35), arrowprops=dict(arrowstyle="-|>", color='#718096', lw=1.2))

    # Node End: Display in UI
    p_end = patches.FancyBboxPatch((2.2, 0.2), 3.6, 0.6, boxstyle="round,pad=0.1", fc='#EDF2F7', ec='#4A5568', lw=1.5)
    ax.add_patch(p_end)
    ax.text(4.0, 0.5, "Display Telemetry in Web/Desktop GUI\nEnable Incremental Ingestion Form", ha='center', va='center', fontsize=8, fontweight='bold', color='#2D3748')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Flowchart saved to: {output_path}")

if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    fig_dir = os.path.join(base_dir, 'figures')
    os.makedirs(fig_dir, exist_ok=True)
    generate_system_architecture(os.path.join(fig_dir, 'system_architecture.png'))
    generate_diagnostic_flowchart(os.path.join(fig_dir, 'diagnostic_flowchart.png'))
