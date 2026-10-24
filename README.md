# Self-Learning Circuit Doctor: Voltage-Signature-Based Fault Detection in DC Circuits
**B.Tech Project | Basic Electrical & Electronics Engineering (BEEE)**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests Passing](https://img.shields.io/badge/pytest-22%20passed-success.svg)](file:///d:/BEEE%20PROJECT/tests/)
[![Accuracy](https://img.shields.io/badge/Test%20Accuracy-100%25-brightgreen.svg)](file:///d:/BEEE%20PROJECT/results/evaluation_summary.txt)
[![SPICE Validated](https://img.shields.io/badge/Falstad%20SPICE-Validated-blueviolet.svg)](https://www.falstad.com/circuit/)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=kotramanojkumar/Self-Learning-Circuit-Doctor&branch=main&mainModule=app.py)

---

## ⚡ Project Overview

The **Self-Learning Circuit Doctor** is an automated, software-driven diagnostic engine designed to detect, diagnose, and localize component failures in a four-resistor DC bridge/ladder network. By sampling a 3-dimensional multi-signal signature vector comprising:
- **Node A Voltage ($V_A$)** in Volts
- **Node B Voltage ($V_B$)** in Volts
- **Total Source Current ($I_s$)** in milliamperes

the system maps the electrical operating state into a standardized feature space and applies a **Standardized Nearest-Centroid Classifier** to isolate faults in under 5 milliseconds.

### 🌟 Key Highlights
- **100.00% Test Accuracy:** Evaluated across 390 held-out test samples under 5% component manufacturing tolerances and DMM sensor noise.
- **Zero Hardware Required:** Fully simulated and cross-validated against the online [Falstad Circuit Simulator](https://www.falstad.com/circuit/) (SPICE Modified Nodal Analysis engine) and an exact Python mathematical model.
- **Ambiguity Resolution:** Demonstrates how measuring source current $I_s$ definitively resolves classic diagnostic deadlocks (e.g. distinguishing $R_1$ Open from $R_2$ Short, where both node voltages are $0.0\text{ V}$).
- **Supervised Self-Learning:** Online incremental centroid updates ($O(1)$ complexity) adapt reference models when new verified laboratory observations are submitted.
- **Dual GUI Support:** Includes both a modern **Streamlit web dashboard** (`app.py`) and a lightweight, 100% offline **Tkinter desktop GUI** (`gui_tk.py`).

---

## 👥 Project Team & Work Allocation (VIT Vellore)

**Institution:** Vellore Institute of Technology (VIT)  
**School:** School of Computer Science and Engineering (SCOPE) & School of Electrical Engineering (SELECT)  
**Course:** Basic Electrical & Electronics Engineering (BEEE) | Academic Year 2026–2027  
**Project Supervisor & Guide:** Prof. POOMPAVAI T, School of Electrical Engineering (SELECT)

| Student Member | Primary Technical Responsibilities | BEEE Theory & Software Focus |
| :--- | :--- | :--- |
| **KOTRA MANOJ KUMAR**<br>Reg. No: `23BCE2113`<br>B.Tech CSE (SCOPE) | • Electrical Circuit Design & BEEE Theory<br>• Kirchhoff's Laws (KCL/KVL) & Hand Derivations<br>• Falstad Simulation & SPICE Cross-Validation<br>• Fault Injection & Experiment Logging | Electrical Design Lead, Circuit Simulation Specialist |
| **Mayank Yadav**<br>Reg. No: `23BCE0119`<br>B.Tech CSE (SCOPE) | • Python Mathematical Model & Unit Testing<br>• Stochastic Dataset Generator & Standardization<br>• Nearest-Centroid Classifier & Self-Learning<br>• Streamlit Web App & Tkinter Desktop GUI | Python Architecture Lead, Diagnostic Software Engineer |
| **Both Members** | • Literature Review & References<br>• 10-Page & Master Comprehensive Project Reports<br>• PowerPoint Presentation & Speaker Notes<br>• Viva Voce Preparation & Live Demonstration | Comprehensive Cross-Validation & Defense |

---

## 📐 Circuit Topology & Nominal Reference Values

```text
  Vs (+10V DC) ----[ R1: 1.0 kΩ ]----+---- Node A ----[ R3: 1.5 kΩ ]----+---- Node B
                                     |                                  |
                                 [ R2: 2.0 kΩ ]                     [ R4: 3.0 kΩ ]
                                     |                                  |
  GND (0V) --------------------------+----------------------------------+
```

### Theoretical Equations (KCL):
At Node A:
$$\frac{V_A - V_s}{R_1} + \frac{V_A}{R_2} + \frac{V_A - V_B}{R_3} = 0$$

At Node B:
$$\frac{V_B - V_A}{R_3} + \frac{V_B}{R_4} = 0 \implies V_B = V_A \left( \frac{R_4}{R_3 + R_4} \right) = \frac{2}{3} V_A$$

### Nominal Healthy Operating Point ($V_s = 10\text{ V}$):
- $R_p = R_2 \parallel (R_3 + R_4) = 2 \parallel 4.5 = \frac{18}{13}\text{ k}\Omega \approx 1.385\text{ k}\Omega$
- $R_{total} = R_1 + R_p = 1 + \frac{18}{13} = \frac{31}{13}\text{ k}\Omega \approx 2.385\text{ k}\Omega$
- $\mathbf{V_A} = \frac{180}{31}\text{ V} \approx \mathbf{5.806\text{ V}}$
- $\mathbf{V_B} = \frac{120}{31}\text{ V} \approx \mathbf{3.871\text{ V}}$
- $\mathbf{I_s} = \frac{130}{31}\text{ mA} \approx \mathbf{4.194\text{ mA}}$
- **Power Conservation Verified:** $P_{in} = V_s \cdot I_s = 41.935\text{ mW} \equiv \sum I_k^2 R_k = 41.935\text{ mW}$

---

## 🔬 13 Tested Operating Scenarios

| Code | Condition | Fault Description | Theoretical $[V_A, V_B, I_s]$ | Falstad SPICE Benchmark |
| :---: | :--- | :--- | :--- | :--- |
| **F0** | `F0_NORMAL` | Healthy Baseline Operation | $5.806\text{ V}, 3.871\text{ V}, 4.194\text{ mA}$ | $5.806\text{ V}, 3.871\text{ V}, 4.194\text{ mA}$ |
| **F1** | `F1_R1_OPEN` | Resistor $R_1$ Open ($R_1 \to \infty$) | $0.000\text{ V}, 0.000\text{ V}, 0.000\text{ mA}$ | $0.000\text{ V}, 0.000\text{ V}, 0.000\text{ mA}$ |
| **F2** | `F2_R2_OPEN` | Resistor $R_2$ Open ($R_2 \to \infty$) | $8.182\text{ V}, 5.455\text{ V}, 1.818\text{ mA}$ | $8.182\text{ V}, 5.455\text{ V}, 1.818\text{ mA}$ |
| **F3** | `F3_R3_OPEN` | Resistor $R_3$ Open ($R_3 \to \infty$) | $6.667\text{ V}, 0.000\text{ V}, 3.333\text{ mA}$ | $6.667\text{ V}, 0.000\text{ V}, 3.333\text{ mA}$ |
| **F4** | `F4_R4_OPEN` | Resistor $R_4$ Open ($R_4 \to \infty$) | $6.667\text{ V}, 6.667\text{ V}, 3.333\text{ mA}$ | $6.667\text{ V}, 6.667\text{ V}, 3.333\text{ mA}$ |
| **F5** | `F5_R1_SHORT` | Resistor $R_1$ Short ($R_1 \to 0$) | $10.000\text{ V}, 6.667\text{ V}, 7.222\text{ mA}$ | $10.000\text{ V}, 6.667\text{ V}, 7.222\text{ mA}$ |
| **F6** | `F6_R2_SHORT` | Resistor $R_2$ Short ($R_2 \to 0$) | $0.000\text{ V}, 0.000\text{ V}, 10.000\text{ mA}$ | $0.000\text{ V}, 0.000\text{ V}, 10.000\text{ mA}$ |
| **F7** | `F7_R3_SHORT` | Resistor $R_3$ Short ($R_3 \to 0$) | $5.455\text{ V}, 5.455\text{ V}, 4.545\text{ mA}$ | $5.455\text{ V}, 5.455\text{ V}, 4.545\text{ mA}$ |
| **F8** | `F8_R4_SHORT` | Resistor $R_4$ Short ($R_4 \to 0$) | $4.615\text{ V}, 0.000\text{ V}, 5.385\text{ mA}$ | $4.615\text{ V}, 0.000\text{ V}, 5.385\text{ mA}$ |
| **F9** | `F9_R1_INC50` | $R_1 +50\%$ Drift ($1.5\text{ k}\Omega$) | $4.800\text{ V}, 3.200\text{ V}, 3.467\text{ mA}$ | $4.800\text{ V}, 3.200\text{ V}, 3.467\text{ mA}$ |
| **F10** | `F10_R2_INC50` | $R_2 +50\%$ Drift ($3.0\text{ k}\Omega$) | $6.429\text{ V}, 4.286\text{ V}, 3.571\text{ mA}$ | $6.429\text{ V}, 4.286\text{ V}, 3.571\text{ mA}$ |
| **F11** | `F11_R3_DEC50` | $R_3 -50\%$ Drift ($0.75\text{ k}\Omega$) | $5.660\text{ V}, 4.528\text{ V}, 4.340\text{ mA}$ | $5.660\text{ V}, 4.528\text{ V}, 4.340\text{ mA}$ |
| **F12** | `F12_R4_DEC50` | $R_4 -50\%$ Drift ($1.5\text{ k}\Omega$) | $5.455\text{ V}, 2.727\text{ V}, 4.545\text{ mA}$ | $5.455\text{ V}, 2.727\text{ V}, 4.545\text{ mA}$ |

---

## 📁 Repository Structure

```text
├── README.md                  # Complete project guide and documentation
├── app.py                     # Streamlit web graphical user interface
├── gui_tk.py                  # Offline desktop Tkinter graphical user interface
├── requirements.txt           # Python scientific library dependencies
├── viva_preparation.md        # Top 20 Viva Q&As, elevator pitch, and faculty demo script
├── Circuit_Doctor_BEEE_Project.zip # Standalone standalone project archive
├── src/
│   ├── __init__.py
│   ├── circuit_model.py       # DC Resistor Network nodal and analytical solver
│   ├── fault_scenarios.py     # 13 operating classes catalog and circuit factory
│   ├── dataset_generator.py   # Stochastic data generator (tolerances, noise, splits)
│   ├── classifier.py          # Baseline rule detector & Nearest-Centroid engine
│   ├── evaluation.py          # Metrics, confusion matrices, and sensitivity curves
│   └── falstad_export.py      # Falstad ASCII exporter, 1-click URLs, and CSV logger
├── tests/
│   ├── __init__.py
│   ├── test_circuit_model.py  # 14 unit tests for KCL/KVL, nominals, and fault physics
│   └── test_classifier.py     # 8 unit tests for standardizer, margins, and learning
├── scripts/
│   ├── generate_10page_report.py    # Builds concise 10-page Word report
│   ├── generate_complete_report.py  # Builds comprehensive 23-section master report
│   ├── generate_diagrams.py         # Generates architecture & flowchart diagrams
│   ├── generate_advanced_diagrams.py # Builds breadboard wiring, fault physics & 3D cluster visuals
│   ├── generate_presentation.py     # Builds 16-slide widescreen PowerPoint presentation
│   └── export_pdf.ps1               # Word/PPT COM PDF automated export script
├── data/                      # Synthetic CSV datasets & Falstad experiment log
│   ├── circuit_fault_train.csv
│   ├── circuit_fault_test.csv
│   ├── circuit_fault_full.csv
│   └── falstad_experiment_log.csv
├── results/                   # Exported performance metrics summary
│   └── evaluation_summary.txt
├── figures/                   # High-resolution 300 DPI figures
│   ├── circuit_schematic.png
│   ├── breadboard_wiring_diagram.png     # Solderless breadboard layout with EIA color bands & DMMs
│   ├── fault_mechanism_diagrams.png      # 4 physical topologies (Normal, R1 Open, R2 Short, R4 Open)
│   ├── 3d_signature_clusters.png         # 3D scatter plot of 13 classes & tolerance ellipsoids
│   ├── system_architecture.png
│   ├── diagnostic_flowchart.png
│   ├── voltage_signatures_comparison.png
│   ├── confusion_matrix_classifier.png
│   ├── confusion_matrix_baseline.png
│   ├── noise_sensitivity_curve.png
│   └── tolerance_sensitivity_curve.png
├── presentation/              # Editable PPTX and native PDF slide deck
│   ├── Circuit_Doctor_Presentation.pptx
│   └── Circuit_Doctor_Presentation.pdf
└── report/                    # Formal editable DOCX and native PDF reports
    ├── BEEE_Circuit_Doctor_Project_Report.docx      # Exactly 10 pages concise
    ├── BEEE_Circuit_Doctor_Project_Report.pdf       # Exactly 10 pages concise PDF
    ├── Self_Learning_Circuit_Doctor_Report.docx     # Comprehensive master report
    └── Self_Learning_Circuit_Doctor_Report.pdf      # Comprehensive master PDF
```

---

## 🚀 Setup & Execution Guide

### 1. Requirements & Dependencies
The project runs on standard Python (>= 3.9). Install required packages:
```bash
pip install -r requirements.txt
```

### 2. Run All Automated Unit Tests (22 Tests)
Run pytest to verify the mathematical model and diagnostic engine:
```bash
python -m pytest tests/ -v
```
*Expected: 22 passed in < 0.3 seconds.*

### 3. Launch Interactive Web Dashboard (Streamlit)
```bash
streamlit run app.py
```
*Features interactive telemetry, live fault injection, DMM measurement entry, Falstad 1-click links, and supervised online self-learning.*

### 4. Launch 100% Offline Desktop GUI (Tkinter)
```bash
python gui_tk.py
```
*Runs completely offline with zero web dependencies using standard Python Tkinter.*

---

## ☁️ Live Cloud Deployment (Streamlit Community Cloud)

To deploy the interactive web dashboard live on the internet for faculty evaluation:

1. Click the deployment badge below:  
   [![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=kotramanojkumar/Self-Learning-Circuit-Doctor&branch=main&mainModule=app.py)
2. Sign in with GitHub account (`kotramanojkumar`).
3. Set the following settings:
   - **Repository:** `kotramanojkumar/Self-Learning-Circuit-Doctor`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Deploy!**

---

*Developed for B.Tech BEEE Coursework. Academic Year 2026–2027. Vellore Institute of Technology (VIT).*
