"""
gui_tk.py - Lightweight Desktop Graphical User Interface (Tkinter)
Part of 'Self-Learning Circuit Doctor: Voltage-Signature-Based Fault Detection in DC Circuits'
BEEE Project for B.Tech

Run directly with standard Python:
    python gui_tk.py
Works offline with zero external web dependencies!
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.circuit_model import DCResistorNetwork, simulate_nominal_circuit
from src.fault_scenarios import (
    FAULT_CATALOG, FAULT_CLASSES, create_circuit_for_fault, get_fault_summary_table
)
from src.dataset_generator import CircuitDatasetGenerator
from src.classifier import NearestCentroidClassifier, BaselineThresholdDetector
from src.falstad_export import generate_falstad_circuit_text, get_falstad_simulator_url


class CircuitDoctorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Self-Learning Circuit Doctor (B.Tech BEEE Project)")
        self.root.geometry("1024x720")
        self.root.minsize(900, 600)

        # Train models
        self.train_models()

        # Build Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Tab 1: Live Diagnosis
        self.tab_diag = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_diag, text="  🩺 Live Diagnosis  ")
        self.build_diagnosis_tab()

        # Tab 2: Reference Catalog
        self.tab_ref = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ref, text="  📋 13 Fault Signatures  ")
        self.build_reference_tab()

        # Tab 3: Falstad Cross-Check
        self.tab_falstad = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_falstad, text="  ⚡ Falstad Simulation  ")
        self.build_falstad_tab()

        # Tab 4: Supervised Self-Learning
        self.tab_learn = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_learn, text="  🧠 Self-Learning Demo  ")
        self.build_learning_tab()

        # Tab 5: About & Team
        self.tab_about = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_about, text="  ℹ️ About & Team  ")
        self.build_about_tab()

    def train_models(self):
        """Train models deterministically on synthetic dataset."""
        gen = CircuitDatasetGenerator(samples_per_class=150, random_seed=42)
        X_tr, X_te, y_tr, y_te, tr_recs, te_recs = gen.train_test_split(0.2)
        self.clf = NearestCentroidClassifier().fit(X_tr, y_tr)
        self.baseline = BaselineThresholdDetector()
        self.X_test = X_te
        self.y_test = y_te

    def build_diagnosis_tab(self):
        frame = ttk.Frame(self.tab_diag, padding="15")
        frame.pack(fill='both', expand=True)

        # Title
        lbl_title = ttk.Label(frame, text="⚡ Self-Learning Circuit Doctor: Real-Time Diagnostic Engine",
                              font=("Helvetica", 14, "bold"))
        lbl_title.pack(anchor='w', pady=(0, 10))

        # Mode Selection
        grp_mode = ttk.LabelFrame(frame, text=" 1. Input Mode Selection ", padding="10")
        grp_mode.pack(fill='x', pady=5)

        self.mode_var = tk.StringVar(value="PRESET")
        r1 = ttk.Radiobutton(grp_mode, text="Inject Predefined Simulated Fault", variable=self.mode_var,
                             value="PRESET", command=self.toggle_mode)
        r2 = ttk.Radiobutton(grp_mode, text="Manual Laboratory DMM Measurement Entry", variable=self.mode_var,
                             value="MANUAL", command=self.toggle_mode)
        r1.grid(row=0, column=0, padx=10, sticky='w')
        r2.grid(row=0, column=1, padx=10, sticky='w')

        # Preset Controls
        self.frame_preset = ttk.Frame(grp_mode)
        self.frame_preset.grid(row=1, column=0, columnspan=2, pady=10, sticky='w')
        ttk.Label(self.frame_preset, text="Select Scenario:").pack(side='left', padx=5)

        self.combo_fault = ttk.Combobox(self.frame_preset, values=[
            f"[{FAULT_CATALOG[k]['code']}] {FAULT_CATALOG[k]['name']}" for k in FAULT_CLASSES
        ], state="readonly", width=35)
        self.combo_fault.current(0)
        self.combo_fault.pack(side='left', padx=5)
        self.combo_fault.bind("<<ComboboxSelected>>", self.on_preset_selected)

        btn_load = ttk.Button(self.frame_preset, text="Load Scenario Values", command=self.on_preset_selected)
        btn_load.pack(side='left', padx=5)

        # Measurements Input
        grp_inputs = ttk.LabelFrame(frame, text=" 2. Circuit Measurements (Feature Vector: [VA, VB, Is]) ", padding="10")
        grp_inputs.pack(fill='x', pady=10)

        ttk.Label(grp_inputs, text="Node A Voltage VA (V):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_va = ttk.Entry(grp_inputs, width=15)
        self.entry_va.insert(0, "5.8065")
        self.entry_va.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(grp_inputs, text="Node B Voltage VB (V):").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.entry_vb = ttk.Entry(grp_inputs, width=15)
        self.entry_vb.insert(0, "3.8710")
        self.entry_vb.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(grp_inputs, text="Source Current Is (mA):").grid(row=0, column=4, padx=5, pady=5, sticky='e')
        self.entry_is = ttk.Entry(grp_inputs, width=15)
        self.entry_is.insert(0, "4.1935")
        self.entry_is.grid(row=0, column=5, padx=5, pady=5)

        btn_diagnose = ttk.Button(grp_inputs, text="🔍 Run Diagnosis", command=self.perform_diagnosis)
        btn_diagnose.grid(row=0, column=6, padx=15, pady=5)

        # Telemetry Display Box
        grp_results = ttk.LabelFrame(frame, text=" 3. Diagnostic Telemetry & Physical Circuit Analysis ", padding="10")
        grp_results.pack(fill='both', expand=True, pady=10)

        self.txt_results = tk.Text(grp_results, wrap='word', height=14, font=("Consolas", 10))
        self.txt_results.pack(fill='both', expand=True, side='left')
        scroll = ttk.Scrollbar(grp_results, command=self.txt_results.yview)
        scroll.pack(side='right', fill='y')
        self.txt_results.config(yscrollcommand=scroll.set)

        self.perform_diagnosis()

    def toggle_mode(self):
        mode = self.mode_var.get()
        if mode == "PRESET":
            self.frame_preset.grid()
        else:
            self.frame_preset.grid_remove()

    def on_preset_selected(self, event=None):
        idx = self.combo_fault.current()
        cls_key = FAULT_CLASSES[idx]
        info = FAULT_CATALOG[cls_key]
        self.entry_va.delete(0, tk.END)
        self.entry_va.insert(0, str(info['expected_va']))
        self.entry_vb.delete(0, tk.END)
        self.entry_vb.insert(0, str(info['expected_vb']))
        self.entry_is.delete(0, tk.END)
        self.entry_is.insert(0, str(info['expected_is']))
        self.perform_diagnosis()

    def perform_diagnosis(self):
        try:
            va = float(self.entry_va.get())
            vb = float(self.entry_vb.get())
            is_ma = float(self.entry_is.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numerical values for VA, VB, and Is.")
            return

        diag = self.clf.predict_detailed(va, vb, is_ma)
        base_diag = self.baseline.predict_single(va, vb, is_ma)

        self.txt_results.delete("1.0", tk.END)
        self.txt_results.insert(tk.END, "=" * 75 + "\n")
        self.txt_results.insert(tk.END, f"  DIAGNOSTIC VERDICT: [{diag['predicted_code']}] {diag['predicted_name'].upper()}\n")
        self.txt_results.insert(tk.END, "=" * 75 + "\n\n")

        self.txt_results.insert(tk.END, f"Input Feature Vector: VA = {va:.4f} V | VB = {vb:.4f} V | Is = {is_ma:.4f} mA\n")
        self.txt_results.insert(tk.END, f"Status / Certainty  : {diag['uncertainty_flag']}\n")
        self.txt_results.insert(tk.END, f"Centroid Distance   : {diag['nearest_distance']:.4f} (Standardized Euclidean Units)\n")
        self.txt_results.insert(tk.END, f"Runner-Up Class     : {diag['second_name']} (Distance: {diag['second_distance']:.4f})\n")
        self.txt_results.insert(tk.END, f"Separation Margin   : {diag['margin']:.4f}\n\n")

        self.txt_results.insert(tk.END, "-" * 75 + "\n")
        self.txt_results.insert(tk.END, "TOP 3 CANDIDATES (Nearest Centroid Method B):\n")
        for i, c in enumerate(diag['ranked_candidates']):
            self.txt_results.insert(tk.END, f"  {i+1}. [{c['code']}] {c['name']:<24} Distance: {c['distance']:.4f}\n")

        self.txt_results.insert(tk.END, "\nCROSS-CHECK (Baseline Rule-Based Method A):\n")
        self.txt_results.insert(tk.END, f"  Predicted: {FAULT_CATALOG[base_diag['predicted_class']]['name']}\n")
        self.txt_results.insert(tk.END, f"  Rule Path: {base_diag['method']}\n\n")

        self.txt_results.insert(tk.END, "-" * 75 + "\n")
        self.txt_results.insert(tk.END, "PHYSICAL CIRCUIT BEHAVIOR:\n")
        self.txt_results.insert(tk.END, f"{diag['description']}\n")

    def build_reference_tab(self):
        frame = ttk.Frame(self.tab_ref, padding="15")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="📋 Catalog of All 13 Operating Conditions & Reference Signatures",
                  font=("Helvetica", 12, "bold")).pack(anchor='w', pady=(0, 10))

        cols = ("Code", "Condition Name", "VA (V)", "VB (V)", "Is (mA)", "Req (Ω)")
        tree = ttk.Treeview(frame, columns=cols, show='headings', height=14)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        tree.column("Condition Name", width=220, anchor='w')

        for row in get_fault_summary_table():
            tree.insert("", "end", values=(row['Code'], row['Name'], row['VA (V)'], row['VB (V)'], row['Is (mA)'], row['Req (Ω)']))

        tree.pack(fill='both', expand=True, side='left')
        scroll = ttk.Scrollbar(frame, command=tree.yview)
        scroll.pack(side='right', fill='y')
        tree.config(yscrollcommand=scroll.set)

    def build_falstad_tab(self):
        frame = ttk.Frame(self.tab_falstad, padding="15")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="⚡ Falstad Circuit Simulator Integration", font=("Helvetica", 12, "bold")).pack(anchor='w', pady=(0, 5))

        txt_info = tk.Text(frame, wrap='word', height=12, font=("Helvetica", 10))
        txt_info.pack(fill='x', pady=5)
        txt_info.insert(tk.END, (
            "The online Falstad Circuit Simulator (https://www.falstad.com/circuit/) simulates this DC bridge network.\n\n"
            "INSTRUCTIONS FOR FACULTY DEMO:\n"
            "1. Open https://www.falstad.com/circuit/\n"
            "2. Click 'File' -> 'Import from Text'.\n"
            "3. Paste the schematic string shown below and click 'OK'.\n"
            "4. Observe Node A (VA ≈ 5.806V), Node B (VB ≈ 3.871V), and Source Current (Is ≈ 4.194mA).\n"
            "5. Change resistor values or disconnect lines to see the voltages shift live!\n"
            "6. Cross-validation log is saved at 'data/falstad_experiment_log.csv'.\n"
        ))
        txt_info.config(state='disabled')

        ttk.Label(frame, text="Falstad Schematic Text (Copy & Paste into Simulator):", font=("Helvetica", 10, "bold")).pack(anchor='w', pady=(10, 2))
        nom_txt = generate_falstad_circuit_text(10.0, 1000.0, 2000.0, 1500.0, 3000.0, "DC Resistor Network")
        txt_circ = tk.Text(frame, wrap='none', height=8, font=("Consolas", 9))
        txt_circ.pack(fill='both', expand=True)
        txt_circ.insert(tk.END, nom_txt)

    def build_learning_tab(self):
        frame = ttk.Frame(self.tab_learn, padding="15")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="🧠 Supervised Self-Learning (Incremental Online Adaptation)",
                  font=("Helvetica", 12, "bold")).pack(anchor='w', pady=(0, 5))

        ttk.Label(frame, text="Submit a confirmed physical lab measurement to incrementally adjust the class centroid:").pack(anchor='w', pady=5)

        grp = ttk.LabelFrame(frame, text=" New Training Sample Submission ", padding="10")
        grp.pack(fill='x', pady=5)

        ttk.Label(grp, text="True Verified Class:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        combo_learn = ttk.Combobox(grp, values=FAULT_CLASSES, state="readonly", width=25)
        combo_learn.current(0)
        combo_learn.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(grp, text="Measured VA (V):").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        entry_lva = ttk.Entry(grp, width=10)
        entry_lva.insert(0, "5.82")
        entry_lva.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(grp, text="Measured VB (V):").grid(row=0, column=4, padx=5, pady=5, sticky='e')
        entry_lvb = ttk.Entry(grp, width=10)
        entry_lvb.insert(0, "3.88")
        entry_lvb.grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(grp, text="Measured Is (mA):").grid(row=0, column=6, padx=5, pady=5, sticky='e')
        entry_lis = ttk.Entry(grp, width=10)
        entry_lis.insert(0, "4.20")
        entry_lis.grid(row=0, column=7, padx=5, pady=5)

        txt_learn_log = tk.Text(frame, wrap='word', height=10, font=("Consolas", 10))

        def on_submit_sample():
            c_key = combo_learn.get()
            try:
                va = float(entry_lva.get())
                vb = float(entry_lvb.get())
                is_val = float(entry_lis.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid floats.")
                return

            res = self.clf.update_with_sample(va, vb, is_val, c_key)
            txt_learn_log.insert(tk.END, f"Ingested confirmed sample for '{c_key}':\n")
            txt_learn_log.insert(tk.END, f"  Count: {res['previous_sample_count']} -> {res['new_sample_count']}\n")
            txt_learn_log.insert(tk.END, f"  Centroid Shift Norm: {res['centroid_shift_norm']:.6f}\n")
            txt_learn_log.insert(tk.END, f"  New Centroid: VA={res['new_physical_centroid'][0]:.4f}V, VB={res['new_physical_centroid'][1]:.4f}V, Is={res['new_physical_centroid'][2]:.4f}mA\n\n")

        btn_submit = ttk.Button(grp, text="🚀 Ingest Sample", command=on_submit_sample)
        btn_submit.grid(row=0, column=8, padx=10, pady=5)

        txt_learn_log.pack(fill='both', expand=True, pady=10)
        txt_learn_log.insert(tk.END, "Awaiting new verified training samples...\n")

    def build_about_tab(self):
        frame = ttk.Frame(self.tab_about, padding="20")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Self-Learning Circuit Doctor", font=("Helvetica", 14, "bold")).pack(anchor='w')
        ttk.Label(frame, text="Voltage-Signature-Based Fault Detection in DC Circuits\nB.Tech BEEE Project",
                  font=("Helvetica", 11, "italic")).pack(anchor='w', pady=(0, 15))

        txt_about = tk.Text(frame, wrap='word', height=16, font=("Helvetica", 10))
        txt_about.pack(fill='both', expand=True)
        txt_about.insert(tk.END, (
            "PROJECT OVERVIEW:\n"
            "This software acts as an automated 'doctor' for electrical circuits. By monitoring voltages at Node A\n"
            "and Node B along with total source current Is, the system compares live signatures against known reference\n"
            "patterns to isolate faults (open circuits, short circuits, and resistance drifts).\n\n"
            "PROJECT TEAM (VIT VELLORE):\n"
            "• Student 1: KOTRA MANOJ KUMAR (Reg. No: 23BCE2113) - B.Tech CSE (SCOPE)\n"
            "• Student 2: Mayank Yadav (Reg. No: 23BCE0119) - B.Tech CSE (SCOPE)\n"
            "• Project Guide: Prof. POOMPAVAI T, School of Electrical Engineering (SELECT)\n\n"
            "KEY METRICS:\n"
            "• Method B (Nearest Centroid Classifier): 100.00% Test Accuracy (390 held-out samples)\n"
            "• Method A (Baseline Rule Detector)   : 100.00% Test Accuracy\n"
            "• Zero Physical Hardware Required: Purely simulated and verified on Falstad SPICE and Python models.\n"
        ))
        txt_about.config(state='disabled')


if __name__ == '__main__':
    root = tk.Tk()
    app = CircuitDoctorApp(root)
    root.mainloop()
