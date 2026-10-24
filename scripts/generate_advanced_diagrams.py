"""
generate_advanced_diagrams.py - Generates:
1. Breadboard & Hardware Wiring Diagram (figures/breadboard_wiring_diagram.png)
2. Side-by-Side Fault Mechanism Comparison Diagram (figures/fault_mechanism_diagrams.png)
3. 3D Feature Space Cluster Scatter Plot (figures/3d_signature_clusters.png)
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.fault_scenarios import FAULT_CATALOG, FAULT_CLASSES
from src.dataset_generator import CircuitDatasetGenerator

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
fig_dir = os.path.join(base_dir, 'figures')
os.makedirs(fig_dir, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. BREADBOARD & HARDWARE WIRING DIAGRAM
# -----------------------------------------------------------------------------
def generate_breadboard_diagram(output_path):
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    c_navy = '#1A365D'
    c_blue = '#2B6CB0'

    # Title Banner
    ax.text(8.0, 9.6, "Physical Hardware Breadboard & Test-Point Wiring Layout", 
            ha='center', va='center', fontsize=15, fontweight='bold', color=c_navy)
    ax.text(8.0, 9.2, "Standard 830-Point Solderless Breadboard with DC Supply & DMM Multimeter Probes", 
            ha='center', va='center', fontsize=10, fontstyle='italic', color='#4A5568')

    # Breadboard Base Plate
    bb_bg = patches.FancyBboxPatch((1.0, 2.0), 14.0, 6.8, boxstyle="round,pad=0.2", 
                                  fc='#E2E8F0', ec='#A0AEC0', lw=2.5)
    ax.add_patch(bb_bg)

    # Breadboard White Top
    bb_body = patches.Rectangle((1.3, 2.3), 13.4, 6.2, fc='#FFFFFF', ec='#CBD5E1', lw=1.5)
    ax.add_patch(bb_body)

    # Power Rails (Top: Red +10V, Blue GND)
    ax.plot([1.8, 14.2], [8.1, 8.1], color='#E53E3E', lw=3, label='+10V Supply Rail')
    ax.plot([1.8, 14.2], [7.7, 7.7], color='#3182CE', lw=3, label='0V Ground Rail')
    ax.text(1.5, 8.1, "+", ha='center', va='center', fontsize=12, fontweight='bold', color='#E53E3E')
    ax.text(1.5, 7.7, "-", ha='center', va='center', fontsize=14, fontweight='bold', color='#3182CE')

    # Bottom Power Rails
    ax.plot([1.8, 14.2], [2.9, 2.9], color='#3182CE', lw=3)
    ax.plot([1.8, 14.2], [2.5, 2.5], color='#E53E3E', lw=3)
    ax.text(1.5, 2.9, "-", ha='center', va='center', fontsize=14, fontweight='bold', color='#3182CE')
    ax.text(1.5, 2.5, "+", ha='center', va='center', fontsize=12, fontweight='bold', color='#E53E3E')

    # Central Divider Trough
    trough = patches.Rectangle((1.8, 5.1), 12.4, 0.4, fc='#CBD5E1', ec='none')
    ax.add_patch(trough)

    # Draw Tie-Point Grids (subtle dots)
    for x_pos in np.linspace(2.2, 13.8, 25):
        for y_pos in [7.3, 6.9, 6.5, 6.1, 5.7]:
            ax.plot(x_pos, y_pos, marker='o', markersize=2.2, color='#A0AEC0')
        for y_pos in [4.7, 4.3, 3.9, 3.5, 3.1]:
            ax.plot(x_pos, y_pos, marker='o', markersize=2.2, color='#A0AEC0')

    # Helper function to draw a realistic 4-band resistor
    def draw_resistor(x1, y1, x2, y2, color_bands, label_text, value_text):
        # Lead wires
        ax.plot([x1, (x1+x2)/2 - 0.7], [y1, (y1+y2)/2], color='#718096', lw=2.5)
        ax.plot([(x1+x2)/2 + 0.7, x2], [(y1+y2)/2, y2], color='#718096', lw=2.5)
        # Resistor Body (Beige/Tan)
        cx, cy = (x1+x2)/2, (y1+y2)/2
        body = patches.FancyBboxPatch((cx - 0.7, cy - 0.25), 1.4, 0.5, boxstyle="round,pad=0.05",
                                      fc='#ECC94B', ec='#B7791F', lw=1.2)
        ax.add_patch(body)
        # 4 Color Bands
        band_xs = [cx - 0.45, cx - 0.15, cx + 0.15, cx + 0.45]
        for bx, bcolor in zip(band_xs, color_bands):
            band = patches.Rectangle((bx - 0.06, cy - 0.25), 0.12, 0.5, fc=bcolor, ec='none')
            ax.add_patch(band)
        # Label & Text
        ax.text(cx, cy + 0.45, label_text, ha='center', va='center', fontsize=9.5, fontweight='bold', color=c_navy)
        ax.text(cx, cy - 0.45, value_text, ha='center', va='center', fontsize=8.0, fontweight='bold', color='#744210')

    # 1. Resistor R1 (1k: Brown-Black-Red-Gold)
    draw_resistor(3.2, 8.1, 5.0, 6.5, ['#7B3F00', '#000000', '#E53E3E', '#D4AF37'], "R1", "1 kΩ (±5%)")

    # 2. Resistor R2 (2k: Red-Black-Red-Gold)
    draw_resistor(5.0, 6.5, 5.0, 2.9, ['#E53E3E', '#000000', '#E53E3E', '#D4AF37'], "R2", "2 kΩ (±5%)")

    # 3. Resistor R3 (1.5k: Brown-Green-Red-Gold)
    draw_resistor(5.0, 6.5, 9.5, 4.3, ['#7B3F00', '#38A169', '#E53E3E', '#D4AF37'], "R3", "1.5 kΩ (±5%)")

    # 4. Resistor R4 (3k: Orange-Black-Red-Gold)
    draw_resistor(9.5, 4.3, 9.5, 2.9, ['#DD6B20', '#000000', '#E53E3E', '#D4AF37'], "R4", "3 kΩ (±5%)")

    # Test Nodes Highlights
    # Node A
    node_a = patches.Circle((5.0, 6.5), 0.22, fc='#3182CE', ec='#1A365D', lw=2, zorder=5)
    ax.add_patch(node_a)
    ax.text(4.2, 6.5, "NODE A", ha='right', va='center', fontsize=9.5, fontweight='bold', color='#2B6CB0')

    # Node B
    node_b = patches.Circle((9.5, 4.3), 0.22, fc='#38A169', ec='#1C4532', lw=2, zorder=5)
    ax.add_patch(node_b)
    ax.text(10.3, 4.3, "NODE B", ha='left', va='center', fontsize=9.5, fontweight='bold', color='#276749')

    # Ground Return
    ax.plot([5.0, 5.0], [2.9, 2.9], marker='o', markersize=6, color='#3182CE')
    ax.plot([9.5, 9.5], [2.9, 2.9], marker='o', markersize=6, color='#3182CE')

    # Helper function to draw Digital Multimeters (DMMs)
    def draw_dmm(x, y, label, reading_str, unit, ec_color, probe_target):
        # DMM Body (Yellow Industrial Multimeter Style)
        dmm = patches.FancyBboxPatch((x-1.0, y-1.0), 2.0, 2.0, boxstyle="round,pad=0.1", 
                                     fc='#FEFCBF', ec=ec_color, lw=2.2)
        ax.add_patch(dmm)
        # LCD Screen (Dark grey-green)
        lcd = patches.Rectangle((x-0.8, y+0.2), 1.6, 0.6, fc='#2D3748', ec='#1A202C')
        ax.add_patch(lcd)
        ax.text(x, y+0.5, reading_str, ha='center', va='center', fontsize=11, fontweight='bold', color='#48BB78', family='monospace')
        # Labels
        ax.text(x, y-0.1, label, ha='center', va='center', fontsize=8.5, fontweight='bold', color=c_navy)
        ax.text(x, y-0.45, f"Range: {unit}", ha='center', va='center', fontsize=7.5, color='#718096')
        # Probe Jumper Wire
        ax.annotate('', xy=probe_target, xytext=(x, y-1.0),
                    arrowprops=dict(arrowstyle="-|>", color=ec_color, lw=2.0, connectionstyle="arc3,rad=-0.2"))

    # DMM 1: Ammeter (Is)
    draw_dmm(2.5, 0.9, "DMM 1: DC AMMETER", "4.194 mA", "20 mA DC", "#C53030", (3.2, 8.1))

    # DMM 2: Voltmeter Node A (VA)
    draw_dmm(6.8, 0.9, "DMM 2: VOLTMETER", "5.806 V", "20 V DC", "#2B6CB0", (5.0, 6.5))

    # DMM 3: Voltmeter Node B (VB)
    draw_dmm(11.5, 0.9, "DMM 3: VOLTMETER", "3.871 V", "20 V DC", "#276749", (9.5, 4.3))

    # DC Power Supply Graphic
    psu = patches.FancyBboxPatch((12.5, 7.2), 2.5, 1.8, boxstyle="round,pad=0.1", fc='#2D3748', ec='#1A202C', lw=1.5)
    ax.add_patch(psu)
    ax.text(13.75, 8.6, "DC REGULATED PSU", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#FFFFFF')
    ax.text(13.75, 8.1, "10.00 V", ha='center', va='center', fontsize=12, fontweight='bold', color='#ECC94B', family='monospace')
    ax.text(13.0, 7.5, "(+) Red", ha='center', va='center', fontsize=7.0, fontweight='bold', color='#FC8181')
    ax.text(14.5, 7.5, "(-) Black", ha='center', va='center', fontsize=7.0, fontweight='bold', color='#90CDF4')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Breadboard diagram saved to: {output_path}")


# -----------------------------------------------------------------------------
# 2. SIDE-BY-SIDE FAULT MECHANISM COMPARISON DIAGRAM
# -----------------------------------------------------------------------------
def generate_fault_mechanism_diagram(output_path):
    fig, axes = plt.subplots(2, 2, figsize=(13, 9.5), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')

    c_navy = '#1A365D'
    c_blue = '#2B6CB0'
    c_red = '#E53E3E'
    c_green = '#276749'
    c_amber = '#D69E2E'

    fig.suptitle("Physical Circuit Topologies under Characteristic Failure Modes", 
                 fontsize=15, fontweight='bold', color=c_navy, y=0.98)

    # Helper function to draw mini schematic
    def draw_mini_circuit(ax, title, r1_mode, r2_mode, r3_mode, r4_mode, va_val, vb_val, is_val, note_str, highlight_color):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 7)
        ax.axis('off')
        ax.set_facecolor('#FFFFFF')
        
        # Border box
        box = patches.FancyBboxPatch((0.2, 0.2), 9.6, 6.4, boxstyle="round,pad=0.1", fc='#FFFFFF', ec='#CBD5E1', lw=1.5)
        ax.add_patch(box)

        # Header Banner
        head_box = patches.Rectangle((0.2, 5.8), 9.6, 0.8, fc=highlight_color, ec='none')
        ax.add_patch(head_box)
        ax.text(5.0, 6.2, title, ha='center', va='center', fontsize=11, fontweight='bold', color='#FFFFFF')

        # Rails
        ax.plot([1.0, 9.0], [5.0, 5.0], color='#CBD5E1', lw=1.5, ls=':')
        ax.plot([1.0, 9.0], [1.2, 1.2], color='#3182CE', lw=2) # GND
        ax.text(9.2, 1.2, "GND (0V)", ha='left', va='center', fontsize=7.5, color='#3182CE')

        # Supply +10V
        ax.plot([1.2, 2.2], [5.0, 5.0], color='#E53E3E', lw=2.5)
        ax.text(1.2, 5.3, "+10V (Vs)", ha='left', va='center', fontsize=8.5, fontweight='bold', color='#E53E3E')

        # Component R1
        if r1_mode == 'OPEN':
            ax.plot([2.2, 2.7], [5.0, 5.0], color='#E53E3E', lw=2)
            ax.plot([3.5, 4.0], [5.0, 5.0], color='#718096', lw=2)
            ax.text(3.1, 5.3, "✕ OPEN GAP", ha='center', va='center', fontsize=8, fontweight='bold', color=c_red)
        elif r1_mode == 'SHORT':
            ax.plot([2.2, 4.0], [5.0, 5.0], color=c_red, lw=3.5)
            ax.text(3.1, 5.3, "══ SOLDER BRIDGE (0Ω)", ha='center', va='center', fontsize=7.5, fontweight='bold', color=c_red)
        else:
            r1_box = patches.Rectangle((2.5, 4.7), 1.2, 0.6, fc='#ECC94B', ec='#B7791F', lw=1.2)
            ax.add_patch(r1_box)
            ax.plot([2.2, 2.5], [5.0, 5.0], color='#718096', lw=2)
            ax.plot([3.7, 4.0], [5.0, 5.0], color='#718096', lw=2)
            ax.text(3.1, 5.0, "R1: 1k", ha='center', va='center', fontsize=8, fontweight='bold')

        # Node A
        ax.plot(4.0, 5.0, marker='o', markersize=6, color='#1A365D')
        ax.text(4.0, 5.4, f"Node A\n{va_val}", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=c_navy)

        # Component R2
        ax.plot([4.0, 4.0], [5.0, 4.3], color='#718096', lw=2)
        ax.plot([4.0, 4.0], [2.1, 1.2], color='#718096', lw=2)
        if r2_mode == 'SHORT':
            ax.plot([4.0, 4.0], [4.3, 2.1], color=c_red, lw=4)
            ax.text(4.3, 3.2, "SHORT TO GND\n(R2=0Ω)", ha='left', va='center', fontsize=8, fontweight='bold', color=c_red)
        elif r2_mode == 'OPEN':
            ax.text(4.3, 3.2, "✕ OPEN (R2=∞)", ha='left', va='center', fontsize=8, fontweight='bold', color=c_red)
        else:
            r2_box = patches.Rectangle((3.6, 2.7), 0.8, 1.2, fc='#ECC94B', ec='#B7791F', lw=1.2)
            ax.add_patch(r2_box)
            ax.text(4.0, 3.3, "R2\n2k", ha='center', va='center', fontsize=8, fontweight='bold')

        # Component R3
        if r3_mode == 'SHORT':
            ax.plot([4.0, 7.5], [5.0, 5.0], color=c_red, lw=3.5)
            ax.text(5.75, 5.3, "R3 SHORT (0Ω)", ha='center', va='center', fontsize=8, fontweight='bold', color=c_red)
        elif r3_mode == 'OPEN':
            ax.plot([4.0, 5.0], [5.0, 5.0], color='#718096', lw=2)
            ax.plot([6.5, 7.5], [5.0, 5.0], color='#718096', lw=2)
            ax.text(5.75, 5.3, "✕ R3 OPEN", ha='center', va='center', fontsize=8, fontweight='bold', color=c_red)
        else:
            ax.plot([4.0, 5.0], [5.0, 5.0], color='#718096', lw=2)
            ax.plot([6.5, 7.5], [5.0, 5.0], color='#718096', lw=2)
            r3_box = patches.Rectangle((5.0, 4.7), 1.5, 0.6, fc='#ECC94B', ec='#B7791F', lw=1.2)
            ax.add_patch(r3_box)
            ax.text(5.75, 5.0, "R3: 1.5k", ha='center', va='center', fontsize=8, fontweight='bold')

        # Node B
        ax.plot(7.5, 5.0, marker='o', markersize=6, color='#276749')
        ax.text(7.5, 5.4, f"Node B\n{vb_val}", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#276749')

        # Component R4
        ax.plot([7.5, 7.5], [5.0, 4.3], color='#718096', lw=2)
        ax.plot([7.5, 7.5], [2.1, 1.2], color='#718096', lw=2)
        if r4_mode == 'OPEN':
            ax.text(7.8, 3.2, "✕ OPEN (R4=∞)\n(Floats to VA)", ha='left', va='center', fontsize=8, fontweight='bold', color=c_red)
        elif r4_mode == 'SHORT':
            ax.plot([7.5, 7.5], [4.3, 2.1], color=c_red, lw=4)
            ax.text(7.8, 3.2, "SHORT TO GND\n(VB = 0V)", ha='left', va='center', fontsize=8, fontweight='bold', color=c_red)
        else:
            r4_box = patches.Rectangle((7.1, 2.7), 0.8, 1.2, fc='#ECC94B', ec='#B7791F', lw=1.2)
            ax.add_patch(r4_box)
            ax.text(7.5, 3.3, "R4\n3k", ha='center', va='center', fontsize=8, fontweight='bold')

        # Bottom Telemetry Bar
        t_box = patches.Rectangle((0.4, 0.4), 9.2, 0.65, fc='#F7FAFC', ec='#E2E8F0')
        ax.add_patch(t_box)
        ax.text(0.6, 0.72, f"Telemetry: VA = {va_val}  |  VB = {vb_val}  |  Is = {is_val}", 
                ha='left', va='center', fontsize=8.5, fontweight='bold', color=c_navy)
        ax.text(9.4, 0.72, note_str, ha='right', va='center', fontsize=7.5, fontstyle='italic', color='#718096')

    # Panel 1: Healthy Circuit
    draw_mini_circuit(axes[0, 0], "State F0: Nominal Healthy Operation", 
                      'NORM', 'NORM', 'NORM', 'NORM', 
                      "5.806 V", "3.871 V", "4.194 mA", "Balanced Divider Loop", '#2B6CB0')

    # Panel 2: R1 Open (Ambiguity Case 1)
    draw_mini_circuit(axes[0, 1], "State F1: R1 Open Circuit (Catastrophic Break)", 
                      'OPEN', 'NORM', 'NORM', 'NORM', 
                      "0.000 V", "0.000 V", "0.000 mA", "Supply Fully Disconnected", '#E53E3E')

    # Panel 3: R2 Short (Ambiguity Case 2 - Notice Is = 10mA!)
    draw_mini_circuit(axes[1, 0], "State F6: R2 Short Circuit (Solder Bridge)", 
                      'NORM', 'SHORT', 'NORM', 'NORM', 
                      "0.000 V", "0.000 V", "10.000 mA", "★ SURGE CURRENT BREAKS TIE!", '#DD6B20')

    # Panel 4: R4 Open (Equipotential Case VA = VB)
    draw_mini_circuit(axes[1, 1], "State F4: R4 Open Circuit (Equipotential Nodes)", 
                      'NORM', 'NORM', 'NORM', 'OPEN', 
                      "6.667 V", "6.667 V", "3.333 mA", "No Current in R3 -> VA = VB", '#805AD5')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Fault mechanism diagram saved to: {output_path}")


# -----------------------------------------------------------------------------
# 3. 3D FEATURE SPACE CLUSTER SCATTER PLOT
# -----------------------------------------------------------------------------
def generate_3d_cluster_plot(output_path):
    gen = CircuitDatasetGenerator(samples_per_class=100, random_seed=42)
    full_data = gen.generate_full_dataset()
    import pandas as pd
    df = pd.DataFrame(full_data['records'])

    fig = plt.figure(figsize=(11, 8.5), dpi=300)
    ax = fig.add_subplot(111, projection='3d')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    c_navy = '#1A365D'

    colors = [
        '#2B6CB0', '#E53E3E', '#38A169', '#D69E2E', '#805AD5', 
        '#DD6B20', '#319795', '#D53F8C', '#4A5568', '#4299E1', 
        '#48BB78', '#ED8936', '#9F7AEA'
    ]

    for idx, f_class in enumerate(FAULT_CLASSES):
        cls_df = df[df['fault_class'] == f_class]
        ax.scatter(cls_df['VA'], cls_df['VB'], cls_df['Is'], 
                   c=colors[idx], label=f"{FAULT_CATALOG[f_class]['code']}: {FAULT_CATALOG[f_class]['name']}",
                   alpha=0.45, s=18, edgecolors='none')

        # Centroid
        c_va = cls_df['VA'].mean()
        c_vb = cls_df['VB'].mean()
        c_is = cls_df['Is'].mean()
        ax.scatter(c_va, c_vb, c_is, color=colors[idx], marker='*', s=140, edgecolors='#1A202C', lw=1.2)

    # Highlight Ambiguity Resolution: Line between F1 (R1 Open) and F6 (R2 Short)
    f1_df = df[df['fault_class'] == 'F1_R1_OPEN']
    f6_df = df[df['fault_class'] == 'F6_R2_SHORT']
    ax.plot([f1_df['VA'].mean(), f6_df['VA'].mean()],
            [f1_df['VB'].mean(), f6_df['VB'].mean()],
            [f1_df['Is'].mean(), f6_df['Is'].mean()],
            color='#E53E3E', lw=2.5, ls='--', label='Ambiguity Vector (Is Separation = 10mA)')

    ax.set_xlabel('Node A Voltage, VA (V)', fontsize=10, fontweight='bold', labelpad=8, color=c_navy)
    ax.set_ylabel('Node B Voltage, VB (V)', fontsize=10, fontweight='bold', labelpad=8, color=c_navy)
    ax.set_zlabel('Source Current, Is (mA)', fontsize=10, fontweight='bold', labelpad=8, color=c_navy)
    ax.set_title('3D Geometric Feature Space [VA, VB, Is] across 13 Circuit Operating Clusters\n(Stars denote class centroids; Ellipsoids denote 5% tolerance spreads)', 
                 fontsize=11.5, fontweight='bold', color=c_navy, pad=14)

    ax.view_init(elev=24, azim=125)
    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1.0), fontsize=7.5, frameon=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"3D cluster plot saved to: {output_path}")

if __name__ == '__main__':
    generate_breadboard_diagram(os.path.join(fig_dir, 'breadboard_wiring_diagram.png'))
    generate_fault_mechanism_diagram(os.path.join(fig_dir, 'fault_mechanism_diagrams.png'))
    generate_3d_cluster_plot(os.path.join(fig_dir, '3d_signature_clusters.png'))
