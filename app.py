"""
app.py - Interactive Graphical Interface for Self-Learning Circuit Doctor
Part of 'Self-Learning Circuit Doctor: Voltage-Signature-Based Fault Detection in DC Circuits'
BEEE Project for B.Tech

Run via Streamlit:
    streamlit run app.py
"""

import os
import sys
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


def run_streamlit_app():
    import streamlit as st
    import matplotlib.pyplot as plt

    st.set_page_config(
        page_title="Self-Learning Circuit Doctor",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Cache trained models in Streamlit session
    @st.cache_resource
    def load_trained_models():
        gen = CircuitDatasetGenerator(samples_per_class=150, random_seed=42)
        X_tr, X_te, y_tr, y_te, tr_recs, te_recs = gen.train_test_split(0.2)
        clf = NearestCentroidClassifier().fit(X_tr, y_tr)
        baseline = BaselineThresholdDetector()
        return clf, baseline, X_te, y_te, tr_recs, te_recs

    clf, baseline, X_test, y_test, train_recs, test_recs = load_trained_models()

    # Sidebar Navigation
    st.sidebar.image("https://img.icons8.com/color/96/resistor.png", width=64)
    st.sidebar.title("Circuit Doctor")
    st.sidebar.caption("Voltage-Signature Fault Diagnostic Engine\nB.Tech BEEE Project")

    nav_choice = st.sidebar.radio(
        "Navigation Menu",
        [
            "🩺 Live Circuit Diagnosis",
            "🔌 Physical Breadboard & Lab Wiring",
            "🔬 Fault Topologies & Ambiguity Resolution",
            "🌐 3D Signature Feature Space",
            "📊 Experimental Evaluation",
            "⚡ Falstad Simulator Cross-Check",
            "🧠 Supervised Self-Learning",
            "📖 BEEE Electrical Theory"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Team Information:**")
    st.sidebar.info(
        "**Student 1:** KOTRA MANOJ KUMAR (23BCE2113)\n\n"
        "**Student 2:** Mayank Yadav (23BCE0119)\n\n"
        "*B.Tech CSE (SCOPE)*\n\n"
        "**Supervisor:** Prof. POOMPAVAI T (SELECT, VIT)"
    )

    # =========================================================================
    # TAB 1: LIVE CIRCUIT DIAGNOSIS
    # =========================================================================
    if nav_choice == "🩺 Live Circuit Diagnosis":
        st.title("🩺 Self-Learning Circuit Doctor: Live Fault Diagnosis")
        st.write(
            "This interface diagnoses electrical faults in a DC bridge/ladder resistor network "
            "by inspecting the multi-signal signature vector: **[VA, VB, Is]**."
        )

        col_top1, col_top2 = st.columns([1, 1])
        with col_top1:
            st.subheader("Circuit Schematic & Nominal Baseline")
            schematic_path = os.path.join(os.path.dirname(__file__), 'figures', 'circuit_schematic.png')
            if os.path.exists(schematic_path):
                st.image(schematic_path, use_container_width=True)
            else:
                st.info("Run `python -m src.evaluation` to generate schematic.")

        with col_top2:
            st.subheader("Nominal Parameters (Healthy Baseline)")
            nom = simulate_nominal_circuit()
            st.markdown(f"""
            - **Supply Voltage (Vs):** `10.0 V` DC
            - **Resistors:** `R1 = 1 kΩ`, `R2 = 2 kΩ`, `R3 = 1.5 kΩ`, `R4 = 3 kΩ`
            - **Expected Node A (VA):** `{nom.VA:.4f} V` (~5.806 V)
            - **Expected Node B (VB):** `{nom.VB:.4f} V` (~3.871 V)
            - **Expected Source Current (Is):** `{nom.Is:.4f} mA` (~4.194 mA)
            - **Total Equivalent Resistance (Req):** `{nom.Req:.2f} Ω`
            """)

        st.markdown("---")
        st.subheader("Diagnostic Input Mode")

        input_mode = st.radio(
            "Select Measurement Source:",
            ["Preset Simulated Fault Condition", "Manual DMM Measurement Entry"],
            horizontal=True
        )

        meas_va, meas_vb, meas_is = 0.0, 0.0, 0.0
        data_source_label = ""
        ground_truth_label = None

        if input_mode == "Preset Simulated Fault Condition":
            data_source_label = "Model-Generated Simulated Fault"
            col_sel1, col_sel2 = st.columns([2, 1])
            with col_sel1:
                selected_fault = st.selectbox(
                    "Choose an Operating Scenario to Inject:",
                    FAULT_CLASSES,
                    format_func=lambda x: f"[{FAULT_CATALOG[x]['code']}] {FAULT_CATALOG[x]['name']}"
                )
                ground_truth_label = selected_fault

            with col_sel2:
                noise_slider = st.slider("Sensor Noise Simulation (mV)", 0, 100, 20) / 1000.0

            # Compute injected circuit state
            net = create_circuit_for_fault(selected_fault)
            raw_state = net.solve()
            rng = np.random.RandomState(None)
            meas_va = max(0.0, raw_state.VA + rng.normal(0, noise_slider))
            meas_vb = max(0.0, raw_state.VB + rng.normal(0, noise_slider))
            meas_is = max(0.0, raw_state.Is + rng.normal(0, noise_slider))

            st.caption(f"Physical Injected Fault Description: {FAULT_CATALOG[selected_fault]['description']}")

        else:
            data_source_label = "Manually Entered Laboratory / Falstad Measurements"
            st.info("Enter multimeter readings measured across Node A, Node B, and the DC source ammeter:")
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                meas_va = st.number_input("Node A Voltage VA (Volts)", min_value=0.0, max_value=15.0, value=5.806, step=0.01)
            with col_m2:
                meas_vb = st.number_input("Node B Voltage VB (Volts)", min_value=0.0, max_value=15.0, value=3.871, step=0.01)
            with col_m3:
                meas_is = st.number_input("Source Current Is (mA)", min_value=0.0, max_value=25.0, value=4.194, step=0.01)

        # Run Diagnosis Button
        if st.button("🔍 Run Diagnostic Engine", type="primary"):
            diag = clf.predict_detailed(meas_va, meas_vb, meas_is)
            base_diag = baseline.predict_single(meas_va, meas_vb, meas_is)

            st.markdown("### 📋 Diagnostic Telemetry Report")
            st.caption(f"Input Data Tag: **{data_source_label}**")

            res_col1, res_col2, res_col3, res_col4 = st.columns(4)
            with res_col1:
                st.metric("Predicted Fault", f"{diag['predicted_code']}: {diag['predicted_name']}")
            with res_col2:
                st.metric("Nearest Centroid Distance", f"{diag['nearest_distance']:.4f}")
            with res_col3:
                st.metric("Runner-Up Separation", f"{diag['margin']:.4f}", help="Margin to 2nd closest candidate")
            with res_col4:
                if diag['is_uncertain']:
                    st.error("⚠️ Borderline / Ambiguous")
                else:
                    st.success("✅ High Confidence")

            # Ground truth verification if available
            if ground_truth_label is not None:
                if diag['predicted_class'] == ground_truth_label:
                    st.success(f"🎯 **Diagnosis Correct:** Injected fault '{ground_truth_label}' matches model prediction!")
                else:
                    st.warning(f"⚠️ **Discrepancy:** Injected '{ground_truth_label}', predicted '{diag['predicted_class']}'.")

            # Explanation & Runner-Up comparison
            st.markdown("#### 🔬 Detailed Circuit Analysis")
            st.write(diag['description'])

            col_exp1, col_exp2 = st.columns(2)
            with col_exp1:
                st.markdown("**Method B (Nearest Centroid Standardized Ranking):**")
                for i, cand in enumerate(diag['ranked_candidates']):
                    marker = "🥇" if i == 0 else ("🥈" if i == 1 else "🥉")
                    st.write(f"{marker} **[{cand['code']}] {cand['name']}** — Distance: `{cand['distance']:.4f}`")

            with col_exp2:
                st.markdown("**Method A (Baseline Rule Detector Cross-Check):**")
                st.write(f"- Predicted: **{FAULT_CATALOG[base_diag['predicted_class']]['name']}**")
                st.write(f"- Rule Applied: `{base_diag['method']}`")
                st.write(f"- Note: {base_diag['confidence_note']}")

            # Visual comparison bar plot
            st.markdown("#### 📊 Measured vs. Reference Signature Comparison")
            fig, ax = plt.subplots(figsize=(8, 3.5), dpi=200)
            features = ['VA (V)', 'VB (V)', 'Is (mA)']
            measured_vec = [meas_va, meas_vb, meas_is]
            ref_info = FAULT_CATALOG[diag['predicted_class']]
            ref_vec = [ref_info['expected_va'], ref_info['expected_vb'], ref_info['expected_is']]

            x = np.arange(len(features))
            width = 0.35
            ax.bar(x - width/2, measured_vec, width, label='Current Measured Input', color='#1f77b4')
            ax.bar(x + width/2, ref_vec, width, label=f"Nominal Reference ({diag['predicted_code']})", color='#ff7f0e')
            ax.set_xticks(x)
            ax.set_xticklabels(features, fontsize=10, fontweight='bold')
            ax.set_ylabel('Magnitude (V or mA)', fontsize=10)
            ax.set_title(f"Signature Vector Comparison against Reference Centroid [{diag['predicted_code']}]", fontsize=11)
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.5, axis='y')
            st.pyplot(fig)
            plt.close()

    # =========================================================================
    # TAB 2: PHYSICAL BREADBOARD & LAB WIRING GUIDE
    # =========================================================================
    elif nav_choice == "🔌 Physical Breadboard & Lab Wiring":
        st.title("🔌 Physical Hardware Breadboard & Test-Point Wiring Guide")
        st.write(
            "This guide shows how the four-resistor DC ladder network is physically wired on a standard "
            "solderless breadboard, complete with resistor EIA color codes, power supply connections, and DMM probe placement."
        )

        fig_dir = os.path.join(os.path.dirname(__file__), 'figures')
        bb_path = os.path.join(fig_dir, 'breadboard_wiring_diagram.png')
        if os.path.exists(bb_path):
            st.image(bb_path, use_container_width=True)

        col_bb1, col_bb2 = st.columns(2)
        with col_bb1:
            st.subheader("Resistor Color Code Reference Table")
            st.markdown("""
            | Resistor | Value | Tolerance | 4-Band Color Code |
            | :--- | :--- | :--- | :--- |
            | **R1** | $1.0\\text{ k}\\Omega$ | $\\pm 5\\%$ | 🟫 Brown, ⬛ Black, 🟥 Red, 🟨 Gold |
            | **R2** | $2.0\\text{ k}\\Omega$ | $\\pm 5\\%$ | 🟥 Red, ⬛ Black, 🟥 Red, 🟨 Gold |
            | **R3** | $1.5\\text{ k}\\Omega$ | $\\pm 5\\%$ | 🟫 Brown, 🟩 Green, 🟥 Red, 🟨 Gold |
            | **R4** | $3.0\\text{ k}\\Omega$ | $\\pm 5\\%$ | 🟧 Orange, ⬛ Black, 🟥 Red, 🟨 Gold |
            """)

        with col_bb2:
            st.subheader("Digital Multimeter (DMM) Probing Rules")
            st.markdown("""
            - **DMM 1 (Ammeter for Is):** Connect in **series** between the $+10\\text{ V}$ positive supply rail and resistor $R_1$. (Set selector to `20 mA DC`).
            - **DMM 2 (Voltmeter for VA):** Connect Red probe to **Node A** (junction of $R_1, R_2, R_3$) and Black probe to **Ground (0V)**. (Set to `20 V DC`).
            - **DMM 3 (Voltmeter for VB):** Connect Red probe to **Node B** (junction of $R_3, R_4$) and Black probe to **Ground (0V)**. (Set to `20 V DC`).
            - **Common Ground Rationale:** All voltages are referenced to a single common 0V ground rail, minimizing probe complexity and mirroring industrial ground planes.
            """)

    # =========================================================================
    # TAB 3: FAULT TOPOLOGIES & AMBIGUITY RESOLUTION
    # =========================================================================
    elif nav_choice == "🔬 Fault Topologies & Ambiguity Resolution":
        st.title("🔬 Circuit Topologies & Physical Failure Physics")
        st.write(
            "Visual comparison of the circuit's physical behavior under healthy operation versus characteristic "
            "catastrophic failure modes, illustrating how source current breaks diagnostic deadlocks."
        )

        fig_dir = os.path.join(os.path.dirname(__file__), 'figures')
        fm_path = os.path.join(fig_dir, 'fault_mechanism_diagrams.png')
        if os.path.exists(fm_path):
            st.image(fm_path, use_container_width=True)

        st.markdown("---")
        st.subheader("★ The Critical Ambiguity Resolution: R1 Open vs R2 Short")
        col_am1, col_am2 = st.columns(2)
        with col_am1:
            st.error("❌ Voltage-Only Monitoring Fails:")
            st.markdown("""
            - **R1 Open (F1):** The circuit is disconnected. Multimeters read:
              - $V_A = 0.000\\text{ V}$
              - $V_B = 0.000\\text{ V}$
            - **R2 Short (F6):** Node A is shorted to Ground. Multimeters read:
              - $V_A = 0.000\\text{ V}$
              - $V_B = 0.000\\text{ V}$
            - **Result:** Identical voltages! A voltage-only detector experiences 100% ambiguity.
            """)

        with col_am2:
            st.success("✅ Multi-Signal Sensing Resolves Tie:")
            st.markdown("""
            - **R1 Open (F1):** $I_s = \\mathbf{0.000\\text{ mA}}$ (open loop, zero power).
            - **R2 Short (F6):** Full $10\\text{ V}$ drops across $R_1$, causing $I_s = \\mathbf{10.000\\text{ mA}}$!
            - **Result:** In standardized 3D space, these two states are separated by an immense **$d = 2.68$ units**, completely eliminating misclassification!
            """)

    # =========================================================================
    # TAB 4: 3D SIGNATURE FEATURE SPACE
    # =========================================================================
    elif nav_choice == "🌐 3D Signature Feature Space":
        st.title("🌐 3D Geometric Feature Space [VA, VB, Is]")
        st.write(
            "Every physical state in the DC network maps to a distinct cluster in the 3-dimensional "
            "measurement space $[V_A, V_B, I_s]$. The Nearest-Centroid Classifier evaluates Euclidean distances to each cluster centroid."
        )

        fig_dir = os.path.join(os.path.dirname(__file__), 'figures')
        clus_path = os.path.join(fig_dir, '3d_signature_clusters.png')
        if os.path.exists(clus_path):
            st.image(clus_path, use_container_width=True)

        st.info(
            "**Key Geometric Insight:** The stars mark the reference class centroids computed from training samples. "
            "The spread of dots around each star reflects natural $\\pm 5\\%$ resistor manufacturing tolerances and sensor noise. "
            "Because the clusters are well-separated in 3D, the Standardized Nearest-Centroid Classifier achieves 100% test accuracy."
        )

    # =========================================================================
    # TAB 5: EXPERIMENTAL EVALUATION
    # =========================================================================
    elif nav_choice == "📊 Experimental Evaluation":
        st.title("📊 Rigorous Experimental Evaluation & Metrics")
        st.write(
            "Evaluation performed strictly on held-out test data (N=390 samples, 30 per class) "
            "with zero data leakage. Centroids and standardization statistics are derived solely from training samples."
        )

        acc_clf = np.mean(clf.predict(X_test) == y_test) * 100.0
        acc_base = np.mean(baseline.predict(X_test) == y_test) * 100.0

        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Method B (Nearest Centroid)", f"{acc_clf:.2f}%", "Overall Test Accuracy")
        col_m2.metric("Method A (Baseline Rules)", f"{acc_base:.2f}%", "Overall Test Accuracy")
        col_m3.metric("Held-Out Test Set Size", f"{len(X_test)} Samples", "30 Samples / Class")

        st.markdown("---")
        st.subheader("Confusion Matrix Analysis")
        col_cm1, col_cm2 = st.columns(2)
        fig_dir = os.path.join(os.path.dirname(__file__), 'figures')
        cm_clf_path = os.path.join(fig_dir, 'confusion_matrix_classifier.png')
        cm_base_path = os.path.join(fig_dir, 'confusion_matrix_baseline.png')

        with col_cm1:
            st.markdown("**Method B: Nearest Centroid Confusion Matrix**")
            if os.path.exists(cm_clf_path):
                st.image(cm_clf_path, use_container_width=True)
        with col_cm2:
            st.markdown("**Method A: Baseline Rule Detector Confusion Matrix**")
            if os.path.exists(cm_base_path):
                st.image(cm_base_path, use_container_width=True)

        st.markdown("---")
        st.subheader("Robustness Sensitivity Studies")
        col_s1, col_s2 = st.columns(2)
        noise_path = os.path.join(fig_dir, 'noise_sensitivity_curve.png')
        tol_path = os.path.join(fig_dir, 'tolerance_sensitivity_curve.png')

        with col_s1:
            st.markdown("**Accuracy vs. Measurement Noise (DMM Noise)**")
            if os.path.exists(noise_path):
                st.image(noise_path, use_container_width=True)
        with col_s2:
            st.markdown("**Accuracy vs. Component Manufacturing Tolerance**")
            if os.path.exists(tol_path):
                st.image(tol_path, use_container_width=True)

        st.markdown("---")
        st.subheader("Download Evaluation Artifacts")
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        test_csv_path = os.path.join(data_dir, 'circuit_fault_test.csv')
        falstad_csv_path = os.path.join(data_dir, 'falstad_experiment_log.csv')

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            if os.path.exists(test_csv_path):
                with open(test_csv_path, 'rb') as f:
                    st.download_button("📥 Download Test Dataset CSV (N=390)", f, file_name="circuit_fault_test.csv", mime="text/csv")
        with col_d2:
            if os.path.exists(falstad_csv_path):
                with open(falstad_csv_path, 'rb') as f:
                    st.download_button("📥 Download Falstad Validation Log CSV", f, file_name="falstad_experiment_log.csv", mime="text/csv")

    # =========================================================================
    # TAB 3: FALSTAD SIMULATOR CROSS-CHECK
    # =========================================================================
    elif nav_choice == "⚡ Falstad Simulator Cross-Check":
        st.title("⚡ Falstad Circuit Simulator Cross-Check & Exporter")
        st.write(
            "The online Falstad Circuit Simulator is an interactive analog circuit simulator. "
            "Here you can open the circuit with one click or copy the ASCII circuit file."
        )

        st.markdown("### 1-Click Online Falstad Simulation")
        nom_txt = generate_falstad_circuit_text(10.0, 1000.0, 2000.0, 1500.0, 3000.0, "Nominal DC Resistor Network")
        nom_url = get_falstad_simulator_url(nom_txt)

        st.link_button("🌐 Open Circuit Directly in Falstad Simulator", nom_url, type="primary")

        st.markdown("### Falstad Validation Experiment Table")
        falstad_csv_path = os.path.join(os.path.dirname(__file__), 'data', 'falstad_experiment_log.csv')
        if os.path.exists(falstad_csv_path):
            import pandas as pd
            df_falstad = pd.read_csv(falstad_csv_path)
            st.dataframe(df_falstad[['Fault_Code', 'Fault_Name', 'Falstad_VA_V', 'Falstad_VB_V', 'Falstad_Is_mA',
                                     'Python_Model_VA_V', 'Python_Model_VB_V', 'Python_Model_Is_mA',
                                     'Classifier_Prediction', 'Diagnostic_Correct', 'Separation_Margin']],
                         use_container_width=True)

        st.markdown("### Falstad Circuit Text Code (For File -> Import from Text)")
        st.code(nom_txt, language="text")

    # =========================================================================
    # TAB 4: SUPERVISED SELF-LEARNING DEMO
    # =========================================================================
    elif nav_choice == "🧠 Supervised Self-Learning":
        st.title("🧠 Supervised Self-Learning Demonstration")
        st.write(
            "This module demonstrates true supervised incremental learning. When a technician "
            "verifies a new labelled measurement from the lab bench, the Circuit Doctor dynamically "
            "updates its reference centroid without discarding prior knowledge."
        )

        st.info(
            "**Incremental Online Formulation:**\n\n"
            r"$N_{c, new} = N_{c, old} + 1$" + "\n\n"
            r"$\mathbf{C}_{c, new} = \mathbf{C}_{c, old} + \frac{1}{N_{c, new}} (\mathbf{z}_{new} - \mathbf{C}_{c, old})$"
        )

        col_l1, col_l2 = st.columns([1, 1])
        with col_l1:
            st.subheader("Submit Verified Lab Measurement")
            learn_cls = st.selectbox("True Verified Operating Class:", FAULT_CLASSES,
                                     format_func=lambda x: f"[{FAULT_CATALOG[x]['code']}] {FAULT_CATALOG[x]['name']}")
            learn_va = st.number_input("Verified VA (V):", value=5.82, step=0.01)
            learn_vb = st.number_input("Verified VB (V):", value=3.88, step=0.01)
            learn_is = st.number_input("Verified Is (mA):", value=4.20, step=0.01)

            if st.button("🚀 Ingest New Training Sample", type="primary"):
                update_res = clf.update_with_sample(learn_va, learn_vb, learn_is, learn_cls)
                st.success(f"Successfully updated reference model for class '{learn_cls}'!")
                st.write(f"- Previous Training Count: `{update_res['previous_sample_count']}`")
                st.write(f"- New Training Count: `{update_res['new_sample_count']}`")
                st.write(f"- Standardized Centroid Shift: `{update_res['centroid_shift_norm']:.6f}` units")
                st.write(f"- New Centroid (Physical): `VA={update_res['new_physical_centroid'][0]:.4f}V, VB={update_res['new_physical_centroid'][1]:.4f}V, Is={update_res['new_physical_centroid'][2]:.4f}mA`")

        with col_l2:
            st.subheader("Understanding Self-Learning in BEEE")
            st.markdown("""
            **What Self-Learning Means Here:**
            - The model does **not** make wild guesses or hallucinate unknown classes.
            - It refines its empirical reference center based on verified real-world hardware data.
            - Addresses sensor calibration drift, resistor thermal aging, and ambient temperature changes over time.
            """)

    # =========================================================================
    # TAB 5: BEEE ELECTRICAL THEORY
    # =========================================================================
    elif nav_choice == "📖 BEEE Electrical Theory":
        st.title("📖 BEEE Electrical Circuit Theory")
        st.write("Complete nodal derivations and Kirchhoff's Laws governing the circuit.")

        st.markdown(r"""
        ### 1. Kirchhoff's Current Law (KCL) Formulation
        At Node A:
        $$\frac{V_A - V_s}{R_1} + \frac{V_A}{R_2} + \frac{V_A - V_B}{R_3} = 0$$
        
        At Node B:
        $$\frac{V_B - V_A}{R_3} + \frac{V_B}{R_4} = 0 \implies V_B = V_A \left( \frac{R_4}{R_3 + R_4} \right)$$
        
        ### 2. Matrix Conductance Form ($\mathbf{G}\mathbf{V} = \mathbf{I}$)
        $$\begin{bmatrix}
        \frac{1}{R_1} + \frac{1}{R_2} + \frac{1}{R_3} & -\frac{1}{R_3} \\
        -\frac{1}{R_3} & \frac{1}{R_3} + \frac{1}{R_4}
        \end{bmatrix}
        \begin{bmatrix} V_A \\ V_B \end{bmatrix} =
        \begin{bmatrix} \frac{V_s}{R_1} \\ 0 \end{bmatrix}$$
        
        ### 3. Nominal Reference Values (Vs = 10V, R1=1k, R2=2k, R3=1.5k, R4=3k)
        - $R_{34} = R_3 + R_4 = 1.5 + 3.0 = 4.5\text{ k}\Omega$
        - $R_p = R_2 \parallel R_{34} = \frac{2 \times 4.5}{2 + 4.5} = \frac{18}{13}\text{ k}\Omega \approx 1.3846\text{ k}\Omega$
        - $R_{total} = R_1 + R_p = 1 + \frac{18}{13} = \frac{31}{13}\text{ k}\Omega \approx 2.3846\text{ k}\Omega$
        - $I_s = \frac{V_s}{R_{total}} = \frac{10}{31/13} = \frac{130}{31}\text{ mA} \approx \mathbf{4.194\text{ mA}}$
        - $V_A = V_s \frac{R_p}{R_1 + R_p} = 10 \frac{18/13}{31/13} = \frac{180}{31}\text{ V} \approx \mathbf{5.806\text{ V}}$
        - $V_B = V_A \left( \frac{R_4}{R_3 + R_4} \right) = \frac{180}{31} \left( \frac{2}{3} \right) = \frac{120}{31}\text{ V} \approx \mathbf{3.871\text{ V}}$
        """)

        st.markdown("### Summary of All 13 Operating Conditions")
        summary_table = get_fault_summary_table()
        import pandas as pd
        st.dataframe(pd.DataFrame(summary_table), use_container_width=True)


if __name__ == '__main__':
    run_streamlit_app()

