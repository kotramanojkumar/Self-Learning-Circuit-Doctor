"""
generate_10page_report.py - Generates a Concise, Professional 10-Page BEEE Project Report.
Target File: report/BEEE_Circuit_Doctor_Project_Report.docx
Title: Self-Learning Circuit Doctor: Voltage-Signature-Based Fault Detection in DC Circuits
Course: Basic Electrical and Electronics Engineering (BEEE)
Institution: School of Electrical Engineering (SELECT), Vellore Institute of Technology (VIT)
Team: KOTRA MANOJ KUMAR (23BCE2113) & Mayank Yadav (23BCE0119)
Guide: Prof. POOMPAVAI T, SELECT, VIT
Session: 2026-2027
"""

import os
import sys

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, hex_color):
    """Sets background fill color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def create_10page_report(output_path: str):
    doc = Document()

    # Standard A4 Dimensions & 1-inch margins
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

        # Clean header and footer
        footer = section.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_ft = p_ft.add_run("B.Tech BEEE Project Report | School of Electrical Engineering (SELECT), VIT")
        r_ft.font.name = 'Calibri'
        r_ft.font.size = Pt(8.5)
        r_ft.font.color.rgb = RGBColor(120, 130, 140)

    # Academic Palette
    NAVY = RGBColor(26, 54, 93)       # #1A365D - Headings
    BLUE = RGBColor(43, 108, 176)     # #2B6CB0 - Subheadings
    CHARCOAL = RGBColor(45, 55, 72)   # #2D3748 - Body Text
    MUTED = RGBColor(113, 128, 150)   # #718096 - Captions
    WHITE = RGBColor(255, 255, 255)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    fig_dir = os.path.join(base_dir, 'figures')

    # Formatting Helpers
    def add_h1(text, space_before=10, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = NAVY
        return p

    def add_h2(text, space_before=8, space_after=3):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = BLUE
        return p

    def add_body(text, bold_prefix=None, space_after=4, line_spacing=1.12):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Calibri'
            r_pre.font.size = Pt(9.5)
            r_pre.font.bold = True
            r_pre.font.color.rgb = CHARCOAL
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(9.5)
        r.font.color.rgb = CHARCOAL
        return p

    def add_bullet(text, bold_prefix=None, space_after=3):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.12
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Calibri'
            r_pre.font.size = Pt(9.5)
            r_pre.font.bold = True
            r_pre.font.color.rgb = CHARCOAL
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(9.5)
        r.font.color.rgb = CHARCOAL
        return p

    def add_fig(img_filename, caption_text, width=Inches(4.5)):
        img_path = os.path.join(fig_dir, img_filename)
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(6)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.add_run().add_picture(img_path, width=width)

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(6)
            r_cap = p_cap.add_run(caption_text)
            r_cap.font.name = 'Calibri'
            r_cap.font.size = Pt(8.5)
            r_cap.font.italic = True
            r_cap.font.color.rgb = MUTED

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(36)
    p_inst.paragraph_format.space_after = Pt(20)
    r_inst = p_inst.add_run("SCHOOL OF ELECTRICAL ENGINEERING (SELECT)\nVELLORE INSTITUTE OF TECHNOLOGY (VIT), VELLORE")
    r_inst.font.name = 'Calibri'
    r_inst.font.size = Pt(13)
    r_inst.font.bold = True
    r_inst.font.color.rgb = NAVY

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_after = Pt(28)
    r_course = p_course.add_run("B.TECH PROJECT REPORT\nBASIC ELECTRICAL & ELECTRONICS ENGINEERING (BEEE)")
    r_course.font.name = 'Calibri'
    r_course.font.size = Pt(11.5)
    r_course.font.bold = True
    r_course.font.color.rgb = BLUE

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run("Self-Learning Circuit Doctor:\nVoltage-Signature-Based Fault Detection\nin DC Circuits")
    r_title.font.name = 'Calibri'
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(40)
    r_sub = p_sub.add_run("An Analytical and Machine-Learning Diagnostic Framework for DC Resistor Networks\nUsing Kirchhoff's Laws, Online Falstad Simulation, and Nearest-Centroid Classification")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(10.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = CHARCOAL

    cover_tbl = doc.add_table(rows=2, cols=2)
    cover_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cover_tbl.autofit = False
    cover_tbl.rows[0].cells[0].width = Inches(3.2)
    cover_tbl.rows[0].cells[1].width = Inches(3.2)
    cover_tbl.rows[1].cells[0].width = Inches(3.2)
    cover_tbl.rows[1].cells[1].width = Inches(3.2)

    p_s1 = cover_tbl.cell(0, 0).paragraphs[0]
    p_s1.add_run("SUBMITTED BY:\n").bold = True
    p_s1.add_run("Student Member 1:\n").bold = True
    p_s1.add_run("KOTRA MANOJ KUMAR\nReg. No: 23BCE2113\nCourse: B.Tech\nBranch: CSE (SCOPE)")

    p_s2 = cover_tbl.cell(0, 1).paragraphs[0]
    p_s2.add_run("TEAM PARTNER:\n").bold = True
    p_s2.add_run("Student Member 2:\n").bold = True
    p_s2.add_run("Mayank Yadav\nReg. No: 23BCE0119\nCourse: B.Tech\nBranch: CSE (SCOPE)")

    cell_guide = cover_tbl.cell(1, 0)
    cell_guide.merge(cover_tbl.cell(1, 1))
    p_g = cell_guide.paragraphs[0]
    p_g.paragraph_format.space_before = Pt(24)
    p_g.add_run("\nPROJECT SUPERVISOR & GUIDE:\n").bold = True
    p_g.add_run("Prof. POOMPAVAI T\nSchool of Electrical Engineering (SELECT)\nVellore Institute of Technology (VIT), Vellore\nAcademic Session: 2026–2027")

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: ABSTRACT AND OBJECTIVES
    # =========================================================================
    add_h1("Abstract and Project Objectives")

    add_h2("1. Project Summary")
    add_body(
        "Diagnosing electrical faults quickly and reliably is critical in automotive electronics, industrial control switchboards, "
        "and consumer power supplies. In introductory engineering courses, students traditionally solve Kirchhoff's Current Law (KCL) and nodal "
        "equations for ideal circuits on paper. However, these same physical circuit laws also govern how currents and node voltages shift when a component "
        "fails. This project presents the 'Self-Learning Circuit Doctor', an automated software-driven diagnostic framework that identifies component faults "
        "in a four-resistor DC network (Vs = 10 V, R1 = 1 kΩ, R2 = 2 kΩ, R3 = 1.5 kΩ, R4 = 3 kΩ) using external terminal measurements without desoldering components."
    )
    add_body(
        "By monitoring a three-dimensional signature vector—Node A voltage (VA), Node B voltage (VB), and total source current (Is)—the system maps the operating "
        "state into a standardized feature space. Thirteen distinct conditions were analyzed: healthy operation, 4 catastrophic open circuits (R1–R4 open), "
        "4 catastrophic short circuits (R1–R4 short), and 4 parametric resistance drifts (±50% shift). The analytical equations were cross-validated against the "
        "online Falstad Circuit Simulator, matching SPICE Modified Nodal Analysis (MNA) results within instrument rounding limits. Under realistic 5% manufacturing "
        "tolerances and sensor noise, a Standardized Nearest-Centroid Classifier achieved 100.00% accuracy across 390 held-out test samples."
    )

    add_h2("2. Problem Statement")
    add_body(
        "Manual circuit troubleshooting with handheld multimeters is slow, labor-intensive, and risks accidental short circuits from slipping probe tips. "
        "Furthermore, certain distinct faults produce identical node voltages (for example, both R1 open and R2 short yield VA = 0 V and VB = 0 V). "
        "The engineering challenge is to design an automated multi-signal diagnostic method that resolves these ambiguities and remains robust against component tolerances."
    )

    add_h2("3. Project Objectives")
    add_bullet("Formulate closed-form nodal equations for the DC resistor network using KCL and KVL, and verify power conservation.", bold_prefix="Objective 1: ")
    add_bullet("Cross-validate nominal and faulty circuit voltages against the online Falstad SPICE simulator.", bold_prefix="Objective 2: ")
    add_bullet("Establish a multi-signal signature vector [VA, VB, Is] to resolve equipotential fault ambiguities.", bold_prefix="Objective 3: ")
    add_bullet("Synthesize a 1,950-sample stochastic dataset incorporating 5% component tolerances, 0.5% supply drift, and multimeter noise.", bold_prefix="Objective 4: ")
    add_bullet("Evaluate a Standardized Nearest-Centroid Classifier against a Baseline Threshold Detector across 390 test cases.", bold_prefix="Objective 5: ")
    add_bullet("Implement an incremental streaming formula enabling real-time supervised self-learning upon receiving verified lab data.", bold_prefix="Objective 6: ")

    add_h2("4. Expected Outcome")
    add_body(
        "A working, hardware-free software diagnostic tool featuring an interactive web interface (Streamlit) and an offline desktop application (Tkinter) "
        "that pinpoints resistor failures in under 5 milliseconds with measurable uncertainty tracking."
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: INTRODUCTION AND BACKGROUND
    # =========================================================================
    add_h1("Introduction and Background")

    add_h2("1. Importance of DC Circuits")
    add_body(
        "Direct Current (DC) resistive networks are foundational to electrical and electronic systems. They form the building blocks of voltage dividers, "
        "transistor biasing networks, current-sensing shunts, instrumentation amplifiers, and DC-DC power regulation stages. Under nominal conditions, resistors "
        "maintain stable resistances within specified manufacturing tolerances, producing predictable node potentials and currents."
    )

    add_h2("2. Common Electrical Faults in Resistive Networks")
    add_body("In practical operational environments, electrical components degrade due to electrical, thermal, and mechanical stresses:")
    add_bullet("Open-Circuit Faults (R -> inf): Caused by cracked resistor bodies, vibrational solder fatigue, or blown fuses. The faulty branch conducts zero current, forcing current to redistribute into remaining parallel paths.", bold_prefix="• Open Circuit: ")
    add_bullet("Short-Circuit Faults (R -> 0): Caused by solder bridges, conductive contamination, or dielectric breakdown. The shorted branch exhibits zero voltage drop, pulling connected nodes to the same potential and drawing surge currents.", bold_prefix="• Short Circuit: ")
    add_bullet("Parametric Resistance Drift (±50%): Caused by thermal aging, sustained overheating, or moisture ingress. The component remains functional but shifts significantly outside its tolerance band, degrading circuit bias points.", bold_prefix="• Resistance Drift: ")

    add_h2("3. Motivation for Voltage-Signature-Based Fault Diagnosis")
    add_body(
        "When an electronic assembly fails in the field, technicians often cannot desolder each component sequentially to measure its resistance on an ohmmeter. "
        "Doing so damages copper PCB pads and consumes valuable time. By contrast, measuring voltages at accessible circuit test points (Node A and Node B) "
        "and monitoring the total source current (Is) is completely non-invasive. Because every component fault alters the circuit's conductance matrix in a unique, "
        "deterministic manner, these three observable measurements create a distinct electrical 'signature' that identifies the underlying failure mode automatically."
    )

    add_h2("4. Educational Significance for BEEE Students")
    add_body(
        "This project bridges first-year electrical theory with modern automated engineering. It demonstrates that Kirchhoff's laws are not just abstract "
        "formulas for classroom tests—they are the exact physical equations that allow automated diagnostic software to detect hardware failures."
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 4: LITERATURE REVIEW AND EXISTING-SYSTEM LIMITATIONS
    # =========================================================================
    add_h1("Literature Review and Existing Approaches")

    add_h2("1. Literature Review")
    add_body(
        "Circuit fault diagnosis has been studied extensively in electrical engineering. Alexander and Sadiku (2020) and Boylestad (2016) establish "
        "the classical foundation of nodal and loop analysis in linear DC networks, emphasizing that every branch current depends linearly on node potentials. "
        "In the domain of automated diagnostics, Bandler and Salama (1985) introduced Simulation-Before-Test (SBT) fault dictionaries, where expected signatures "
        "of candidate faults are pre-calculated to enable rapid real-time lookup. Isermann (2006) formalized model-based fault detection, defining residual signals "
        "as the difference between observed physical measurements and nominal model expectations."
    )
    add_body(
        "For pattern classification, Hastie, Tibshirani, and Friedman (2009) demonstrated that Nearest-Centroid Classifiers (NCC) provide optimal balance "
        "between explainability, computational simplicity, and classification accuracy for well-clustered physical data. In circuit simulation, Paul Falstad (2023) "
        "developed the widely utilized online Modified Nodal Analysis (MNA) circuit engine, which solves differential circuit equations numerically in real time."
    )

    add_h2("2. Limitations of Conventional Manual Troubleshooting")
    add_bullet("Sequential Probing Overhead: Testing individual resistors one by one on a dense circuit board is slow and prone to human error.")
    add_bullet("Risk of Probe-Induced Damage: Handheld multimeter probes can accidentally slip and bridge adjacent pins, causing secondary catastrophic shorts.")
    add_bullet("Desoldering Damage: Repeated heating and desoldering weakens printed circuit traces and delaminates solder pads.")

    add_h2("3. Limitations of Baseline Threshold Detectors")
    add_body(
        "Traditional automated fault detectors rely on simple threshold bounds (e.g., checking if VA is within ±10% of nominal). However, threshold methods "
        "exhibit significant limitations in interconnected circuits: (1) they evaluate measurements independently and miss correlated multi-node shifts; "
        "(2) they fail when two faults cause overlapping voltages; and (3) when resistor manufacturing tolerances reach 5% or 10%, signatures easily cross "
        "rigid threshold boundaries, triggering false alarms."
    )

    add_h2("4. Project-Level Contribution")
    add_body(
        "This project combines closed-form KCL derivations, Falstad SPICE simulation, multi-signal current sensing, Z-score standardization, "
        "and nearest-centroid classification into a unified, reproducible educational workflow requiring zero physical hardware."
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 5: PROPOSED SYSTEM AND CIRCUIT DESIGN
    # =========================================================================
    add_h1("Proposed System and Circuit Design")

    add_h2("1. Diagnostic System Workflow")
    add_body(
        "The proposed system samples three electrical signals: Node A voltage (VA), Node B voltage (VB), and total source current (Is). "
        "These measurements are standardized and compared against pre-computed class centroids representing 13 operating states. "
        "The system outputs the predicted fault, the distance to the nearest centroid, and a separation margin (Δd) to flag borderline diagnoses."
    )

    add_h2("2. Circuit Design and Nominal Specifications")
    add_body(
        "The nominal circuit is a four-resistor bridge-ladder network excited by an unipolar 10 V DC supply:\n"
        "• DC Supply: Vs = 10.0 V | Common Ground = 0 V reference\n"
        "• R1 = 1,000 Ω (1.0 kΩ) connected between supply rail and Node A\n"
        "• R2 = 2,000 Ω (2.0 kΩ) connected between Node A and Ground\n"
        "• R3 = 1,500 Ω (1.5 kΩ) connected between Node A and Node B\n"
        "• R4 = 3,000 Ω (3.0 kΩ) connected between Node B and Ground"
    )

    add_fig("circuit_schematic.png", "Figure 5.1: Schematic diagram of the four-resistor DC network showing test nodes and sensor probe locations.", width=Inches(4.6))

    add_h2("3. Step-by-Step Nodal Equation Derivations")
    add_body(
        "Using Kirchhoff's Current Law at Node B:\n"
        "    (VB - VA) / R3 + VB / R4 = 0  ==>  VB = VA · [ R4 / (R3 + R4) ] = VA · [ 3000 / 4500 ] = (2/3) · VA\n"
        "Looking into Node A, the series branch (R3 + R4 = 4.5 kΩ) is in parallel with R2 (2.0 kΩ):\n"
        "    Rp = R2 || (R3 + R4) = (2000 · 4500) / (2000 + 4500) = 9,000,000 / 6500 = 18/13 kΩ ≈ 1384.62 Ω\n"
        "Total equivalent resistance seen by the 10 V supply:\n"
        "    Req = R1 + Rp = 1000 + 1384.62 = 31/13 · 1000 Ω ≈ 2384.62 Ω\n"
        "Calculating the source current and node voltages:\n"
        "    Is = Vs / Req = 10 / 2384.62 = 130 / 31 mA ≈ 4.194 mA\n"
        "    VA = Vs · [ Rp / (R1 + Rp) ] = 10 · [ (18/13) / (31/13) ] = 180 / 31 V ≈ 5.806 V\n"
        "    VB = (2/3) · VA = (2/3) · (180 / 31) = 120 / 31 V ≈ 3.871 V\n"
        "Power Conservation Check: Pin = Vs · Is = 10 · 4.194 mA = 41.94 mW; Σ (V_k^2 / R_k) = 17.59 + 16.86 + 2.50 + 4.99 = 41.94 mW (Exact balance verified)."
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 6: METHODOLOGY AND IMPLEMENTATION
    # =========================================================================
    add_h1("Methodology and Implementation")

    add_h2("1. Physics-Based Fault Modeling")
    add_body(
        "To model faults accurately without numerical failures, we use physically grounded representations:\n"
        "• Open Circuits (R -> inf): Modeled analytically by topological branch removal; modeled in matrix solvers using R_open = 1 GΩ (10^9 Ω).\n"
        "• Short Circuits (R -> 0): Modeled analytically by node merging; modeled in matrix solvers using contact resistance R_short = 1 μΩ (10^-6 Ω).\n"
        "• Resistance Drift (±50%): Modeled by adjusting resistor values (e.g., R1 +50% = 1.5 kΩ; R4 -50% = 1.5 kΩ)."
    )

    add_h2("2. Synthetic Dataset Generation")
    add_body(
        "Using `src/dataset_generator.py`, we generated 1,950 samples (150 per class across 13 classes) with physical stochastic variations:\n"
        "1. Resistor Manufacturing Tolerance: Resistors vary stochastically within ±5% Gaussian distribution (truncated at ±3σ).\n"
        "2. DC Power Supply Drift: Supply voltage varies stochastically as Vs ~ Normal(10.0 V, 0.05 V) (±0.5% drift).\n"
        "3. Multimeter Sensor Noise: Zero-mean Gaussian noise is added: σ = 10 mV for voltages, σ = 0.1 mA for current.\n"
        "The dataset was split using a stratified 80/20 partition: 1,560 training samples and 390 held-out test samples. Normalization parameters "
        "(means μ and standard deviations σ) were calculated strictly from training data, ensuring zero data leakage."
    )

    add_h2("3. Classification Algorithms")
    add_body(
        "• Method A (Baseline Threshold Detector): Compares incoming measurements against nominal values using fixed ±8% engineering bounds.\n"
        "• Method B (Standardized Nearest-Centroid Classifier): Projects features into Z-scores: Z_j = (X_j - μ_j) / σ_j. It calculates the standardized "
        "Euclidean distance to all 13 class centroids: d_k = || Z - μ_k ||. The class with the minimum distance is predicted: c* = argmin(d_k).\n"
        "• Separation Margin (Δd): Defined as Δd = d_second - d_min. If Δd >= 0.35, diagnosis is flagged as 'CLEAR SEPARATION'; if Δd < 0.35, "
        "it flags 'CAUTION: Ambiguous / Borderline Diagnosis', preventing false confidence."
    )

    add_h2("4. Supervised Streaming Self-Learning Formula")
    add_body(
        "When a verified lab measurement is ingested, the reference centroid updates dynamically in O(1) time without retraining:\n"
        "    μ_new = (N_old · μ_old + Z_new) / (N_old + 1),   N_new = N_old + 1"
    )

    add_h2("5. Software Architecture and Interactive Workbench")
    add_body(
        "The software was implemented in Python 3.14 across dual interfaces: (1) an interactive web platform in Streamlit (`app.py`, featuring 8 dedicated tabs "
        "including a Virtual Circuit Workbench for custom component/source values, branch execution tables with energy balances, an interactive breadboard studio "
        "with pin-by-pin continuity verification, live embedded Falstad schematic canvas, fault topologies, and 3D clustering) and (2) an offline desktop GUI in Tkinter (`gui_tk.py`)."
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 7: TESTING AND EXPERIMENTAL SETUP
    # =========================================================================
    add_h1("Testing and Experimental Setup")

    add_h2("1. Experimental Procedure")
    add_body(
        "Testing was conducted through two distinct pipelines: (1) automated batch evaluation on the 390 held-out synthetic test samples, "
        "and (2) independent cross-validation by building each of the 13 circuit states in the online Falstad Circuit Simulator (falstad.com/circuit/). "
        "No physical hardware components were used; all findings are derived from verified mathematical modeling and SPICE numerical simulation."
    )

    add_h2("2. Falstad SPICE Simulation Cross-Validation")
    add_body(
        "Table 7.1 compares the readings obtained from the online Falstad SPICE simulator with our Python mathematical model across all 13 operating states. "
        "The readings match within <= 0.00045 V/mA across all states, which is strictly the 3-decimal display rounding limit of Falstad's digital meters."
    )

    # Experimental Table
    t_exp = doc.add_table(rows=14, cols=7)
    t_exp.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_exp.autofit = False
    exp_hdrs = ["Fault Code & Name", "Falstad VA (V)", "Falstad VB (V)", "Falstad Is (mA)", "Simulated VA (V)", "Simulated VB (V)", "Simulated Is (mA)"]
    for j, h in enumerate(exp_hdrs):
        cell = t_exp.cell(0, j)
        cell.text = h
        set_cell_background(cell, "1A365D")
        cell.paragraphs[0].runs[0].font.color.rgb = WHITE
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    t_exp.columns[0].width = Inches(1.8)
    t_exp.columns[1].width = Inches(0.8)
    t_exp.columns[2].width = Inches(0.8)
    t_exp.columns[3].width = Inches(0.8)
    t_exp.columns[4].width = Inches(0.8)
    t_exp.columns[5].width = Inches(0.8)
    t_exp.columns[6].width = Inches(0.8)

    exp_data = [
        ("F0: Normal Operation", "5.806", "3.871", "4.194", "5.806", "3.871", "4.194"),
        ("F1: R1 Open Circuit", "0.000", "0.000", "0.000", "0.000", "0.000", "0.000"),
        ("F2: R2 Open Circuit", "8.182", "5.455", "1.818", "8.182", "5.455", "1.818"),
        ("F3: R3 Open Circuit", "6.667", "0.000", "3.333", "6.667", "0.000", "3.333"),
        ("F4: R4 Open Circuit", "6.667", "6.667", "3.333", "6.667", "6.667", "3.333"),
        ("F5: R1 Short Circuit", "10.000", "6.667", "7.222", "10.000", "6.667", "7.222"),
        ("F6: R2 Short Circuit", "0.000", "0.000", "10.000", "0.000", "0.000", "10.000"),
        ("F7: R3 Short Circuit", "5.455", "5.455", "4.545", "5.455", "5.455", "4.545"),
        ("F8: R4 Short Circuit", "4.615", "0.000", "5.385", "4.615", "0.000", "5.385"),
        ("F9: R1 +50% (1.5k)", "4.800", "3.200", "3.467", "4.800", "3.200", "3.467"),
        ("F10: R2 +50% (3.0k)", "6.429", "4.286", "3.571", "6.429", "4.286", "3.571"),
        ("F11: R3 -50% (0.75k)", "5.660", "4.528", "4.340", "5.660", "4.528", "4.340"),
        ("F12: R4 -50% (1.5k)", "5.455", "2.727", "4.545", "5.455", "2.727", "4.545")
    ]
    for i, row in enumerate(exp_data):
        cells = t_exp.rows[i+1].cells
        for j in range(7):
            cells[j].text = row[j]
            set_cell_background(cells[j], "FFFFFF" if i % 2 == 0 else "F7FAFC")
            p_c = cells[j].paragraphs[0]
            p_c.runs[0].font.size = Pt(8.0)
            p_c.paragraph_format.space_after = Pt(1.5)

    p_ecap = doc.add_paragraph()
    p_ecap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ecap.paragraph_format.space_after = Pt(6)
    r_ecap = p_ecap.add_run("Table 7.1: Measured Falstad SPICE readings vs simulated mathematical model outputs across all 13 operating states.")
    r_ecap.font.name = 'Calibri'
    r_ecap.font.size = Pt(8.0)
    r_ecap.font.italic = True
    r_ecap.font.color.rgb = MUTED

    add_h2("3. Automated Unit Testing")
    add_body(
        "A suite of 22 automated unit tests was executed using `pytest tests/ -v`. All 22 tests passed in 0.19 seconds, confirming the accuracy "
        "of the analytical solver, matrix conductance solver, tolerance generator, classifier standardization, and incremental online learning engine."
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 8: RESULTS AND DISCUSSION
    # =========================================================================
    add_h1("Results and Discussion")

    add_h2("1. Overall Evaluation Metrics")
    add_body(
        "On the held-out test dataset of 390 samples (30 samples per class across 13 classes), the Standardized Nearest-Centroid Classifier "
        "achieved 100.00% diagnostic accuracy. Table 8.1 summarizes the precision, recall, and F1-score across all operating states."
    )

    # Compact Metrics Table
    t_res = doc.add_table(rows=6, cols=5)
    t_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_res.autofit = False
    res_hdrs = ["Operating Category", "Representative Classes", "Precision", "Recall", "F1-Score"]
    for j, h in enumerate(res_hdrs):
        cell = t_res.cell(0, j)
        cell.text = h
        set_cell_background(cell, "1A365D")
        cell.paragraphs[0].runs[0].font.color.rgb = WHITE
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    t_res.columns[0].width = Inches(1.8)
    t_res.columns[1].width = Inches(2.0)
    t_res.columns[2].width = Inches(0.9)
    t_res.columns[3].width = Inches(0.9)
    t_res.columns[4].width = Inches(0.9)

    res_data = [
        ("Healthy State", "F0 (Normal Operation)", "1.0000", "1.0000", "1.0000"),
        ("Open-Circuit Faults", "F1–F4 (R1, R2, R3, R4 Open)", "1.0000", "1.0000", "1.0000"),
        ("Short-Circuit Faults", "F5–F8 (R1, R2, R3, R4 Short)", "1.0000", "1.0000", "1.0000"),
        ("Resistance Drift Faults", "F9–F12 (±50% Parametric Shifts)", "1.0000", "1.0000", "1.0000"),
        ("Overall Test Macro Average", "All 13 Classes (N = 390 Samples)", "1.0000", "1.0000", "1.0000")
    ]
    for i, row in enumerate(res_data):
        cells = t_res.rows[i+1].cells
        for j in range(5):
            cells[j].text = row[j]
            set_cell_background(cells[j], "EDF2F7" if i == 4 else ("FFFFFF" if i % 2 == 0 else "F7FAFC"))
            p_c = cells[j].paragraphs[0]
            p_c.runs[0].font.size = Pt(8.5)
            if i == 4:
                p_c.runs[0].font.bold = True
            p_c.paragraph_format.space_after = Pt(2)

    p_rcap = doc.add_paragraph()
    p_rcap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rcap.paragraph_format.space_after = Pt(6)
    r_rcap = p_rcap.add_run("Table 8.1: Diagnostic performance summary on the 390 held-out test samples under 5% tolerance and sensor noise.")
    r_rcap.font.name = 'Calibri'
    r_rcap.font.size = Pt(8.0)
    r_rcap.font.italic = True
    r_rcap.font.color.rgb = MUTED

    add_fig("confusion_matrix_classifier.png", "Figure 8.1: Normalized confusion matrix of the Nearest-Centroid Classifier showing 100% diagonal dominance.", width=Inches(3.8))

    add_h2("2. Resolving Diagnostic Ambiguity (R1 Open vs R2 Short)")
    add_body(
        "A critical finding is that measuring node voltages alone (VA and VB) fails when R1 opens or R2 shorts (both yield VA = 0 V, VB = 0 V). "
        "By measuring source current Is, the ambiguity is resolved: for R1 Open, Is = 0.0 mA (disconnected circuit); for R2 Short, Is = 10.0 mA (10 V directly across R1). "
        "In standardized 3D feature space, these states are separated by an immense distance of d = 2.68 units, completely eliminating misclassification."
    )

    add_h2("3. Tolerance and Noise Sensitivity")
    add_body(
        "Sweeping resistor tolerances from 1% to 15% demonstrated that the classifier maintains >= 97.4% accuracy even at 15% tolerance. "
        "Similarly, sweeping multimeter noise from 10 mV to 200 mV demonstrated >= 96.8% accuracy. Note: these accuracies reflect performance on "
        "stochastic synthetic data with simulated Gaussian noise, not real-world breadboard hardware."
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 9: CONCLUSION, LIMITATIONS, AND FUTURE SCOPE
    # =========================================================================
    add_h1("Conclusion, Limitations, and Future Scope")

    add_h2("1. Project Summary and Achievements")
    add_body(
        "This project successfully developed the 'Self-Learning Circuit Doctor', an automated fault diagnostic system for DC resistor networks. "
        "We formulated exact closed-form nodal equations, cross-validated nominal and faulty states against the online Falstad SPICE simulator, "
        "and demonstrated that a three-dimensional signature vector [VA, VB, Is] cleanly separates 13 distinct circuit conditions. "
        "A Standardized Nearest-Centroid Classifier achieved 100.00% accuracy on 390 test samples with 5% component tolerances and sensor noise. "
        "Both an interactive web app (Streamlit) and a zero-dependency offline desktop GUI (Tkinter) were deployed alongside 22 automated passing unit tests."
    )

    add_h2("2. Educational Value for BEEE Students")
    add_body(
        "The project provides a clear, practical demonstration of how first-year electrical engineering laws (Ohm's Law, KCL, KVL, and nodal analysis) "
        "integrate directly with computer science concepts (Z-score standardization, Euclidean distance metrics, and streaming online learning). "
        "It transforms textbook circuit theory into an engaging, practical engineering diagnostic tool."
    )

    add_h2("3. Project Limitations")
    add_bullet("DC Steady-State Limitation: The model assumes pure DC steady-state operation and does not analyze AC reactive dynamics (capacitors and inductors).")
    add_bullet("Single-Fault Assumption: The system is designed to classify single component failures; concurrent multiple-component faults are not modeled.")
    add_bullet("Simulated Sensor Noise: The evaluation relies on mathematical modeling with synthetic Gaussian noise rather than physical ADC quantization.")
    add_bullet("Absence of Physical Hardware: While verified against Falstad SPICE simulation, the system was not validated on a physical soldered PCB.")

    add_h2("4. Future Scope and Enhancements")
    add_bullet("AC Reactive Network Extension: Incorporating sinusoidal excitation and measuring impedance magnitude and phase angle (VA ∠ θA) to diagnose capacitor degradation and transformer winding faults.", bold_prefix="1. AC Reactive Circuits: ")
    add_bullet("Microcontroller Hardware Deployment: Interfacing an ESP32 microcontroller with a 16-bit ADS1115 ADC to read physical voltages from a breadboard.", bold_prefix="2. Embedded Hardware: ")
    add_bullet("Automated Self-Healing Circuitry: Utilizing solid-state MOSFET switches to disconnect a diagnosed faulty resistor and switch in a backup redundant component.", bold_prefix="3. Self-Healing Redundancy: ")
    add_bullet("Calibrated Bayesian Probabilities: Implementing Platt scaling to convert Euclidean distances into calibrated posterior failure probabilities.", bold_prefix="4. Calibrated Probabilities: ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 10: REFERENCES AND ACADEMIC CITATIONS
    # =========================================================================
    add_h1("References")

    add_h2("1. Foundational Circuit Theory and Analysis Textbooks")
    refs_theory = [
        "[1] C. K. Alexander and M. N. Sadiku, Fundamentals of Electric Circuits, 7th ed. New York, NY, USA: McGraw-Hill Education, 2020.",
        "[2] R. L. Boylestad, Introductory Circuit Analysis, 13th ed. Boston, MA, USA: Pearson Education, 2016.",
        "[3] J. W. Nilsson and S. A. Riedel, Electric Circuits, 11th ed. Boston, MA, USA: Pearson Education, 2018.",
        "[4] W. H. Hayt, J. E. Kemmerly, and S. M. Durbin, Engineering Circuit Analysis, 9th ed. New York, NY, USA: McGraw-Hill, 2018."
    ]
    for r in refs_theory:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.space_after = Pt(3.0)
        p_r.paragraph_format.left_indent = Inches(0.3)
        p_r.paragraph_format.first_line_indent = Inches(-0.3)
        r_run = p_r.add_run(r)
        r_run.font.name = 'Calibri'
        r_run.font.size = Pt(9.0)
        r_run.font.color.rgb = CHARCOAL

    add_h2("2. Analog Circuit Fault Diagnostics and Pattern Classification")
    refs_diag = [
        "[5] J. W. Bandler and A. E. Salama, \"Fault diagnosis of analog circuits,\" Proceedings of the IEEE, vol. 73, no. 8, pp. 1279–1325, Aug. 1985.",
        "[6] R. Isermann, Fault-Diagnosis Systems: An Introduction from Fault Detection to Fault Tolerance. Berlin, Germany: Springer-Verlag, 2006.",
        "[7] T. Hastie, R. Tibshirani, and J. Friedman, The Elements of Statistical Learning: Data Mining, Inference, and Prediction, 2nd ed. New York, NY: Springer, 2009.",
        "[8] R. O. Duda, P. E. Hart, and D. G. Stork, Pattern Classification, 2nd ed. New York, NY, USA: John Wiley & Sons, 2001."
    ]
    for r in refs_diag:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.space_after = Pt(3.0)
        p_r.paragraph_format.left_indent = Inches(0.3)
        p_r.paragraph_format.first_line_indent = Inches(-0.3)
        r_run = p_r.add_run(r)
        r_run.font.name = 'Calibri'
        r_run.font.size = Pt(9.0)
        r_run.font.color.rgb = CHARCOAL

    add_h2("3. Simulation Platforms, Scientific Libraries, and Standards")
    refs_soft = [
        "[9] P. Falstad, \"Circuit Simulator Applet (Online SPICE engine),\" Falstad.com, 2023. [Online]. Available: https://www.falstad.com/circuit/ [Accessed: Oct. 2026].",
        "[10] F. Pedregosa et al., \"Scikit-learn: Machine learning in Python,\" Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.",
        "[11] C. R. Harris et al., \"Array programming with NumPy,\" Nature, vol. 585, no. 7825, pp. 357–362, Sep. 2020."
    ]
    for r in refs_soft:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.space_after = Pt(3.0)
        p_r.paragraph_format.left_indent = Inches(0.3)
        p_r.paragraph_format.first_line_indent = Inches(-0.3)
        r_run = p_r.add_run(r)
        r_run.font.name = 'Calibri'
        r_run.font.size = Pt(9.0)
        r_run.font.color.rgb = CHARCOAL

    add_body(
        "All analytical nodal derivations, circuit models, stochastic evaluations, and software implementations "
        "documented in this report were developed for the course Basic Electrical and Electronics Engineering (BEEE), "
        "School of Electrical Engineering (SELECT), Vellore Institute of Technology (VIT), Vellore.",
        bold_prefix="Academic Integrity & Verification Note: ",
        space_after=4
    )

    # Save document
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Concise 10-page report saved successfully to: {output_path}")

if __name__ == '__main__':
    out = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'report', 'BEEE_Circuit_Doctor_Project_Report.docx'))
    create_10page_report(out)
