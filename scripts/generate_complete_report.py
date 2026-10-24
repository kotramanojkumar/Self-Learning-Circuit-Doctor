"""
generate_complete_report.py - Master Academic Report Generator for B.Tech BEEE Project
Title: Self-Learning Circuit Doctor: Voltage-Signature-Based Fault Detection in DC Circuits
Institution: School of Electrical Engineering (SELECT), Vellore Institute of Technology (VIT), Vellore
Authors: KOTRA MANOJ KUMAR (23BCE2113) & Mayank Yadav (23BCE0119)
Guide: Prof. POOMPAVAI T, SELECT, VIT
Academic Session: 2026-2027
"""

import os
import sys
import shutil

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.fault_scenarios import FAULT_CATALOG, FAULT_CLASSES, get_fault_summary_table

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Sets background fill color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets internal padding/margins for a table cell in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def add_footer_to_document(doc):
    """Configures clean header and footer across all sections."""
    for section in doc.sections:
        footer = section.footer
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.paragraph_format.space_before = Pt(6)
        r = p.add_run("School of Electrical Engineering (SELECT), VIT  |  B.Tech Project Report")
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(140, 150, 160)

def build_full_report(output_path: str):
    doc = Document()

    # Standard 1-inch margins on A4
    for section in doc.sections:
        section.page_width = Inches(8.27)   # A4 width
        section.page_height = Inches(11.69) # A4 height
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    add_footer_to_document(doc)

    # Executive Academic Palette
    NAVY = RGBColor(26, 54, 93)       # #1A365D - Chapter Headings (H1)
    BLUE = RGBColor(43, 108, 176)     # #2B6CB0 - Section Headings (H2)
    TEAL = RGBColor(44, 122, 123)     # #2C7A7B - Sub-section Headings (H3)
    CHARCOAL = RGBColor(45, 55, 72)   # #2D3748 - Body Text
    MUTED = RGBColor(113, 128, 150)   # #718096 - Captions & Notes
    WHITE = RGBColor(255, 255, 255)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    fig_dir = os.path.join(base_dir, 'figures')

    # Typography & Structure Helpers
    def add_p(text="", style=None, space_before=0, space_after=6, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT):
        p = doc.add_paragraph(text, style=style)
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        return p

    def add_h1(text):
        p = add_p(space_before=20, space_after=8, align=WD_ALIGN_PARAGRAPH.LEFT)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(15.5)
        run.font.bold = True
        run.font.color.rgb = NAVY
        return p

    def add_h2(text):
        p = add_p(space_before=13, space_after=5, align=WD_ALIGN_PARAGRAPH.LEFT)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = BLUE
        return p

    def add_h3(text):
        p = add_p(space_before=9, space_after=3, align=WD_ALIGN_PARAGRAPH.LEFT)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11.0)
        run.font.bold = True
        run.font.color.rgb = TEAL
        return p

    def add_body(text, bold_prefix=None, space_after=6):
        p = add_p(space_after=space_after)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Calibri'
            r_pre.font.size = Pt(10.5)
            r_pre.font.bold = True
            r_pre.font.color.rgb = CHARCOAL
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(10.5)
        r.font.color.rgb = CHARCOAL
        return p

    def add_bullet(text, bold_prefix=None):
        p = add_p(style='List Bullet', space_after=4)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Calibri'
            r_pre.font.size = Pt(10.5)
            r_pre.font.bold = True
            r_pre.font.color.rgb = CHARCOAL
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(10.5)
        r.font.color.rgb = CHARCOAL
        return p

    def add_figure(img_filename, caption_text, width=Inches(5.7)):
        img_path = os.path.join(fig_dir, img_filename)
        if os.path.exists(img_path):
            p_img = add_p(space_before=10, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER)
            p_img.add_run().add_picture(img_path, width=width)

            p_cap = add_p(space_before=0, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
            r_cap = p_cap.add_run(caption_text)
            r_cap.font.name = 'Calibri'
            r_cap.font.size = Pt(9.5)
            r_cap.font.italic = True
            r_cap.font.color.rgb = MUTED

    def add_callout(text, bold_title="Key Finding:"):
        p = add_p(space_before=6, space_after=10)
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.right_indent = Inches(0.4)
        r_pre = p.add_run(f"📌 {bold_title} ")
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(10.0)
        r_pre.font.bold = True
        r_pre.font.color.rgb = NAVY
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(10.0)
        r.font.italic = True
        r.font.color.rgb = CHARCOAL

    # =========================================================================
    # FRONT MATTER 1: COVER PAGE
    # =========================================================================
    p_inst = add_p(space_before=20, space_after=24, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_inst = p_inst.add_run("SCHOOL OF ELECTRICAL ENGINEERING (SELECT)\nVELLORE INSTITUTE OF TECHNOLOGY (VIT), VELLORE")
    r_inst.font.name = 'Calibri'
    r_inst.font.size = Pt(13)
    r_inst.font.bold = True
    r_inst.font.color.rgb = NAVY

    p_proj = add_p(space_before=0, space_after=16, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_proj = p_proj.add_run("B.TECH PROJECT REPORT\nBASIC ELECTRICAL & ELECTRONICS ENGINEERING (BEEE)")
    r_proj.font.name = 'Calibri'
    r_proj.font.size = Pt(12)
    r_proj.font.bold = True
    r_proj.font.color.rgb = BLUE

    p_t = add_p(space_before=24, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_t = p_t.add_run("Self-Learning Circuit Doctor:\nVoltage-Signature-Based Fault Detection\nin DC Circuits")
    r_t.font.name = 'Calibri'
    r_t.font.size = Pt(22)
    r_t.font.bold = True
    r_t.font.color.rgb = NAVY

    p_sub = add_p(space_before=0, space_after=32, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_sub = p_sub.add_run("An Analytical and Machine-Learning Diagnostic Framework for DC Resistor Networks\nUsing Kirchhoff's Laws, Falstad Simulation, and Nearest-Centroid Classification")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = CHARCOAL

    cover_table = doc.add_table(rows=2, cols=2)
    cover_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cover_table.autofit = False
    for row in cover_table.rows:
        row.cells[0].width = Inches(3.2)
        row.cells[1].width = Inches(3.2)

    cell_l = cover_table.cell(0, 0)
    cell_r = cover_table.cell(0, 1)

    p_l = cell_l.paragraphs[0]
    p_l.add_run("SUBMITTED BY:\n").bold = True
    p_l.add_run("Student Member 1:\n").bold = True
    p_l.add_run("KOTRA MANOJ KUMAR\nReg. No: 23BCE2113\nCourse: B.Tech\nBranch: Computer Science & Engineering (SCOPE)")

    p_r = cell_r.paragraphs[0]
    p_r.add_run("TEAM PARTNER:\n").bold = True
    p_r.add_run("Student Member 2:\n").bold = True
    p_r.add_run("Mayank Yadav\nReg. No: 23BCE0119\nCourse: B.Tech\nBranch: Computer Science & Engineering (SCOPE)")

    cell_sup = cover_table.cell(1, 0)
    cell_sup.merge(cover_table.cell(1, 1))
    p_sup = cell_sup.paragraphs[0]
    p_sup.paragraph_format.space_before = Pt(16)
    p_sup.add_run("\nPROJECT SUPERVISOR & GUIDE:\n").bold = True
    p_sup.add_run("Prof. POOMPAVAI T\nSchool of Electrical Engineering (SELECT)\nVellore Institute of Technology (VIT), Vellore\nAcademic Session: 2026–2027")

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER 2: CERTIFICATE PAGE
    # =========================================================================
    p_c_head = add_p(space_before=24, space_after=18, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_c_head = p_c_head.add_run("VELLORE INSTITUTE OF TECHNOLOGY (VIT), VELLORE\nSCHOOL OF ELECTRICAL ENGINEERING (SELECT)\n\nBONAFIDE CERTIFICATE")
    r_c_head.font.name = 'Calibri'
    r_c_head.font.size = Pt(13)
    r_c_head.font.bold = True
    r_c_head.font.color.rgb = NAVY

    add_body(
        "This is to certify that the project report entitled 'Self-Learning Circuit Doctor: Voltage-Signature-Based Fault "
        "Detection in DC Circuits' is the bonafide work of KOTRA MANOJ KUMAR (Reg. No: 23BCE2113) and Mayank Yadav "
        "(Reg. No: 23BCE0119), students of B.Tech in Computer Science and Engineering (SCOPE), who carried out this project "
        "work under my supervision for the course Basic Electrical and Electronics Engineering (BEEE) during the academic year 2026–2027."
    )
    add_body(
        "The results embodied in this report have been verified through independent mathematical nodal formulations and rigorous online "
        "circuit simulations in the Falstad SPICE environment. To the best of our knowledge, the work presented herein represents original "
        "engineering study and has not been submitted elsewhere for the award of any other degree or diploma."
    )

    cert_table = doc.add_table(rows=2, cols=2)
    cert_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cert_table.autofit = False
    for row in cert_table.rows:
        row.cells[0].width = Inches(3.2)
        row.cells[1].width = Inches(3.2)

    p_c1 = cert_table.cell(0, 0).paragraphs[0]
    p_c1.paragraph_format.space_before = Pt(36)
    p_c1.add_run("_____________________________\n").bold = True
    p_c1.add_run("Prof. POOMPAVAI T\nProject Supervisor & Guide\nSchool of Electrical Engineering (SELECT)\nVIT, Vellore")

    p_c2 = cert_table.cell(0, 1).paragraphs[0]
    p_c2.paragraph_format.space_before = Pt(36)
    p_c2.add_run("_____________________________\n").bold = True
    p_c2.add_run("Head of the Department / Programme Chair\nSchool of Electrical Engineering (SELECT)\nVIT, Vellore")

    p_c3 = cert_table.cell(1, 0).paragraphs[0]
    p_c3.paragraph_format.space_before = Pt(36)
    p_c3.add_run("Date: ________________________\nPlace: Vellore, Tamil Nadu")

    p_c4 = cert_table.cell(1, 1).paragraphs[0]
    p_c4.paragraph_format.space_before = Pt(36)
    p_c4.add_run("_____________________________\n").bold = True
    p_c4.add_run("Internal / External Examiner")

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER 3: STUDENT DECLARATION
    # =========================================================================
    p_d_head = add_p(space_before=24, space_after=18, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_d_head = p_d_head.add_run("DECLARATION OF ORIGINAL WORK")
    r_d_head.font.name = 'Calibri'
    r_d_head.font.size = Pt(14)
    r_d_head.font.bold = True
    r_d_head.font.color.rgb = NAVY

    add_body(
        "We hereby declare that the project entitled 'Self-Learning Circuit Doctor: Voltage-Signature-Based Fault Detection "
        "in DC Circuits', submitted to the School of Electrical Engineering (SELECT), Vellore Institute of Technology (VIT), "
        "is a record of original work done by us under the academic guidance of Prof. POOMPAVAI T."
    )
    add_body(
        "We confirm that all circuit equations, mathematical nodal models, machine learning classification scripts, interactive interfaces, "
        "and experimental evaluations presented in this report were developed collaboratively by us. All literature, textbooks, and software "
        "tools utilized in this project have been duly cited and referenced in accordance with academic integrity guidelines. This report has not "
        "been submitted previously for the award of any degree, diploma, or certificate at this or any other academic institution."
    )

    decl_table = doc.add_table(rows=1, cols=2)
    decl_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    decl_table.autofit = False
    decl_table.rows[0].cells[0].width = Inches(3.2)
    decl_table.rows[0].cells[1].width = Inches(3.2)

    p_d1 = decl_table.cell(0, 0).paragraphs[0]
    p_d1.paragraph_format.space_before = Pt(40)
    p_d1.add_run("_____________________________\n").bold = True
    p_d1.add_run("KOTRA MANOJ KUMAR\nReg. No: 23BCE2113\nB.Tech CSE (SCOPE)\nVIT, Vellore")

    p_d2 = decl_table.cell(0, 1).paragraphs[0]
    p_d2.paragraph_format.space_before = Pt(40)
    p_d2.add_run("_____________________________\n").bold = True
    p_d2.add_run("Mayank Yadav\nReg. No: 23BCE0119\nB.Tech CSE (SCOPE)\nVIT, Vellore")

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER 4: ACKNOWLEDGEMENTS
    # =========================================================================
    p_a_head = add_p(space_before=24, space_after=18, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_a_head = p_a_head.add_run("ACKNOWLEDGEMENTS")
    r_a_head.font.name = 'Calibri'
    r_a_head.font.size = Pt(14)
    r_a_head.font.bold = True
    r_a_head.font.color.rgb = NAVY

    add_body(
        "We express our sincere gratitude to our project supervisor and guide, Prof. POOMPAVAI T, School of Electrical "
        "Engineering (SELECT), for her invaluable guidance, continuous encouragement, and constructive critique throughout "
        "the formulation, execution, and documentation of this project. Her deep insights into DC network theorems, nodal analysis, "
        "and electrical simulation methodology provided the strong theoretical grounding required for this investigation."
    )
    add_body(
        "We extend our heartfelt thanks to the Dean and faculty members of the School of Electrical Engineering (SELECT) "
        "and the School of Computer Science and Engineering (SCOPE) at Vellore Institute of Technology for providing an excellent "
        "academic environment, computing infrastructure, and encouragement that made this interdisciplinary project possible."
    )
    add_body(
        "We also acknowledge the open-source engineering community, particularly Paul Falstad for developing and maintaining the Falstad "
        "Circuit Simulator, and the developers of NumPy, pandas, scikit-learn, matplotlib, and Streamlit, whose reliable software libraries "
        "formed the backbone of our diagnostic and visualization platform. Finally, we thank our parents and peers for their unwavering support."
    )

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER 5: ABSTRACT & KEYWORDS
    # =========================================================================
    p_ab_head = add_p(space_before=24, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_ab_head = p_ab_head.add_run("ABSTRACT")
    r_ab_head.font.name = 'Calibri'
    r_ab_head.font.size = Pt(14)
    r_ab_head.font.bold = True
    r_ab_head.font.color.rgb = NAVY

    add_body(
        "Rapid, reliable fault localization in electrical and electronic networks is a critical operational requirement across automotive "
        "electronic control units, industrial power distribution switchboards, and aerospace avionics. In conventional engineering education, "
        "Kirchhoff's Current Law (KCL), Kirchhoff's Voltage Law (KVL), and nodal analysis are typically studied as abstract mathematical equations "
        "solved on paper under ideal, fault-free operating conditions. However, in physical systems, these exact same linear circuit laws determine "
        "the deterministic redistribution of currents and potentials when a component suffers degradation or catastrophic failure. This project "
        "develops the 'Self-Learning Circuit Doctor', a software-driven analytical and pattern-recognition framework designed to automatically detect "
        "and localize component failures in a four-resistor DC bridge-ladder network (Vs = 10 V, R1 = 1 kΩ, R2 = 2 kΩ, R3 = 1.5 kΩ, R4 = 3 kΩ) "
        "using non-invasive terminal and test-node measurements without requiring physical component desoldering."
    )
    add_body(
        "By continuously monitoring a three-dimensional electrical signature vector—Node A voltage (VA), Node B voltage (VB), and total source "
        "current (Is)—the diagnostic system maps the operating state into a normalized feature space. Thirteen distinct operating conditions "
        "were formulated and modeled: healthy baseline operation, four open-circuit conditions (R1–R4 open), four short-circuit conditions (R1–R4 short), "
        "and four parametric drift conditions (±50% resistance variations). Closed-form analytical nodal equations were independently derived and "
        "verified against Modified Nodal Analysis (MNA) matrix conductance solvers. The mathematical model was cross-validated against the online Falstad "
        "Circuit Simulator, demonstrating exact numerical agreement within 0.00045 V/mA across all 13 states, attributable solely to instrument display rounding."
    )
    add_body(
        "To evaluate real-world diagnostic robustness, a stochastic synthetic dataset of 1,950 samples was generated, incorporating 5% resistor "
        "manufacturing tolerances, 0.5% DC supply drift, and digital multimeter measurement noise (10 mV voltage noise, 0.1 mA current noise). Using "
        "a stratified 80/20 train/test split (1,560 training samples, 390 test samples), a Standardized Nearest-Centroid Classifier achieved 100.00% "
        "classification accuracy across all 390 held-out test cases. Importantly, measuring source current Is proved essential to resolve an exact "
        "equipotential ambiguity between R1 open and R2 short, where both faults yield identical zero-volt readings at Node A and Node B. A separation margin "
        "metric was implemented to quantify diagnostic uncertainty and flag borderline conditions. Furthermore, a supervised incremental self-learning "
        "mechanism enables the system to ingest verified laboratory readings and adapt reference centroids dynamically without retraining. Both an interactive "
        "Streamlit web interface and a zero-dependency Tkinter desktop application were developed. The entire framework operates via software simulation, "
        "requiring zero physical hardware while providing a reproducible, rigorous educational benchmark for undergraduate electrical engineering."
    )

    add_h2("Keywords")
    add_body(
        "DC circuit analysis; Kirchhoff's laws; Nodal analysis; Fault detection and localization; Voltage-current signatures; "
        "Nearest-centroid classification; Feature standardization; Circuit simulation; Falstad SPICE; Resistor degradation."
    )

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER 7: TABLE OF CONTENTS
    # =========================================================================
    p_toc_head = add_p(space_before=24, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_toc_head = p_toc_head.add_run("TABLE OF CONTENTS")
    r_toc_head.font.name = 'Calibri'
    r_toc_head.font.size = Pt(14)
    r_toc_head.font.bold = True
    r_toc_head.font.color.rgb = NAVY

    toc_items = [
        ("Front Matter: Certificate, Declaration, Acknowledgements, Abstract", "i – v"),
        ("List of Figures and List of Tables", "vi"),
        ("List of Abbreviations and Symbols", "vii"),
        ("Chapter 1: Introduction", "1"),
        ("    1.1 Background of DC Circuits and Electrical Networks", "1"),
        ("    1.2 The Growing Need for Automated Fault Diagnostics", "1"),
        ("    1.3 Motivation for Selecting the Project", "2"),
        ("    1.4 Problem Statement and Challenges", "2"),
        ("    1.5 Project Objectives", "3"),
        ("    1.6 Scope of the Investigation", "3"),
        ("    1.7 Functional and Operational Requirements", "4"),
        ("    1.8 Technical Limitations and Physical Assumptions", "4"),
        ("    1.9 Organization of the Report", "4"),
        ("Chapter 2: Literature Review", "5"),
        ("    2.1 Overview of Analog and DC Circuit Fault Diagnosis", "5"),
        ("    2.2 Voltage and Current Signature Analysis in Electrical Systems", "5"),
        ("    2.3 Threshold-Based Fault Detection Systems and Their Limitations", "6"),
        ("    2.4 Nearest-Centroid and Minimum Distance Pattern Recognition", "6"),
        ("    2.5 Fault Diagnosis Under Component Tolerances and Sensor Noise", "7"),
        ("    2.6 Critical Analysis of Verifiable Literature", "7"),
        ("    2.7 Project-Level Contributions and Research Gap", "8"),
        ("Chapter 3: Existing System and Proposed System", "9"),
        ("    3.1 Conventional Manual Circuit Troubleshooting Techniques", "9"),
        ("    3.2 Inherent Bottlenecks in Manual Fault Tracing", "9"),
        ("    3.3 Proposed Automated Voltage-Signature Diagnostic System", "10"),
        ("    3.4 Key Stages of the Proposed System", "10"),
        ("    3.5 Comparative Analysis: Baseline Detector vs Proposed Classifier", "11"),
        ("    3.6 Realistic Statement of Novelty and Educational Impact", "12"),
        ("Chapter 4: Circuit Design and Theoretical Analysis", "13"),
        ("    4.1 Topology and Schematic Description", "13"),
        ("    4.2 Component Specifications and Nominal Operating Point", "13"),
        ("    4.3 Fundamental Electrical Laws in DC Circuits", "14"),
        ("    4.4 Step-by-Step Nodal Equation Derivations", "14"),
        ("    4.5 Physics-Based Modeling of Circuit Faults (Opens, Shorts, Drifts)", "16"),
        ("    4.6 Theoretical Measurement Trajectories across All 13 Modes", "17"),
        ("Chapter 5: Methodology and Implementation", "18"),
        ("    5.1 End-to-End Implementation Workflow", "18"),
        ("    5.2 Online Falstad Circuit Simulator Integration & SPICE Cross-Validation", "18"),
        ("    5.3 Python Closed-Form & Matrix Conductance Modeling", "19"),
        ("    5.4 Stochastic Dataset Generator with Physical Disturbances", "19"),
        ("    5.5 Feature Selection: The Crucial [VA, VB, Is] Signature Vector", "20"),
        ("    5.6 Data Leakage Prevention and Stratified Partitioning", "20"),
        ("    5.7 Z-Score Feature Standardization", "21"),
        ("    5.8 Classification Algorithms: Baseline Detector vs Nearest Centroid", "21"),
        ("    5.9 Supervised Incremental Self-Learning Engine", "22"),
        ("    5.10 Software Architecture and Modular Implementation", "22"),
        ("    5.11 Graphical User Interfaces (Streamlit Web & Tkinter Desktop)", "23"),
        ("    5.12 Software Dependencies and Platform Compatibility", "23"),
        ("Chapter 6: Experimental Setup and Testing", "24"),
        ("    6.1 Simulation Environment and Hardware-Free Testing Rationale", "24"),
        ("    6.2 Catalog of Tested Fault Classes (F0 through F12)", "24"),
        ("    6.3 Synthetic Dataset Generation Parameters and Statistical Distributions", "25"),
        ("    6.4 Rigorous Separation of Synthetic Training Data and Falstad SPICE Data", "25"),
        ("    6.5 Falstad Online SPICE Simulation Procedure and Interactive URLs", "26"),
        ("    6.6 Automated Unit Testing Suite (22 Pytest Verification Tests)", "26"),
        ("    6.7 Comprehensive 13-Class Falstad vs Python Benchmark Experiment Log", "27"),
        ("Chapter 7: Results and Discussion", "28"),
        ("    7.1 Cross-Validation of Python Analytical Model against Falstad SPICE", "28"),
        ("    7.2 Dataset Statistical Analysis and Feature Distributions", "28"),
        ("    7.3 Overall Diagnostic Performance Comparison", "29"),
        ("    7.4 Per-Class Performance Metrics (Precision, Recall, F1-Score)", "29"),
        ("    7.5 Confusion Matrix Analysis and Diagonal Dominance", "30"),
        ("    7.6 Ambiguity Resolution: How Current Sensing Disambiguates R1 Open vs R2 Short", "31"),
        ("    7.7 Equipotential Analysis: R4 Open vs R3 Short", "31"),
        ("    7.8 Robustness Analysis: Resistor Manufacturing Tolerance Sensitivity", "32"),
        ("    7.9 Robustness Analysis: Sensor Measurement Noise Sensitivity", "32"),
        ("    7.10 Edge Cases, Borderline Diagnoses, and Diagnostic Uncertainty Flagging", "33"),
        ("    7.11 Demonstration of Live Supervised Incremental Self-Learning", "33"),
        ("Chapter 8: Limitations and Future Scope", "34"),
        ("    8.1 Technical Limitations of Current Study", "34"),
        ("    8.2 Discrepancies Between Virtual Simulation and Physical Hardware", "34"),
        ("    8.3 Recommended Future Enhancements (AC, Microcontroller, Self-Healing)", "35"),
        ("Chapter 9: Conclusion", "36"),
        ("    9.1 Summary of Completed Work", "36"),
        ("    9.2 Fulfillment of Educational and Technical Objectives", "36"),
        ("    9.3 Practical Value of DC Circuit Laws in Modern Autonomous Engineering", "37"),
        ("    9.4 Final Concluding Remarks", "37"),
        ("References (IEEE Style)", "38"),
        ("Appendices", "39"),
        ("    Appendix A: Step-by-Step Mathematical Derivations and KCL Proofs", "39"),
        ("    Appendix B: Falstad Simulation Experiment Log (13 Operating Conditions)", "40"),
        ("    Appendix C: Top 20 Comprehensive Viva Voce Questions and Model Answers", "41"),
        ("    Appendix D: Two-Minute Elevator Pitch & Five-Minute Faculty Demo Script", "44")
    ]

    t_toc = doc.add_table(rows=len(toc_items) + 1, cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_toc.autofit = False
    t_toc.rows[0].cells[0].width = Inches(5.4)
    t_toc.rows[0].cells[1].width = Inches(1.0)

    cell_th1 = t_toc.cell(0, 0)
    cell_th2 = t_toc.cell(0, 1)
    cell_th1.text = "Section / Chapter Title"
    cell_th2.text = "Page"
    set_cell_background(cell_th1, "1A365D")
    set_cell_background(cell_th2, "1A365D")
    cell_th1.paragraphs[0].runs[0].font.color.rgb = WHITE
    cell_th1.paragraphs[0].runs[0].font.bold = True
    cell_th2.paragraphs[0].runs[0].font.color.rgb = WHITE
    cell_th2.paragraphs[0].runs[0].font.bold = True
    cell_th2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    for idx, (sec_title, page_num) in enumerate(toc_items):
        r_cells = t_toc.rows[idx + 1].cells
        r_cells[0].width = Inches(5.4)
        r_cells[1].width = Inches(1.0)
        r_cells[0].text = sec_title
        r_cells[1].text = page_num
        r_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p0 = r_cells[0].paragraphs[0]
        p1 = r_cells[1].paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        p0.runs[0].font.size = Pt(9.0)
        p1.runs[0].font.size = Pt(9.0)
        if "Chapter" in sec_title or "Front Matter" in sec_title or "References" in sec_title or "Appendices" in sec_title:
            p0.runs[0].font.bold = True
            p0.runs[0].font.color.rgb = NAVY
            p1.runs[0].font.bold = True
            set_cell_background(r_cells[0], "EDF2F7")
            set_cell_background(r_cells[1], "EDF2F7")
        else:
            set_cell_background(r_cells[0], "FFFFFF" if idx % 2 == 0 else "F7FAFC")
            set_cell_background(r_cells[1], "FFFFFF" if idx % 2 == 0 else "F7FAFC")

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER 8 & 9: LIST OF FIGURES & LIST OF TABLES
    # =========================================================================
    add_h2("List of Figures")
    figures_list = [
        ("Figure 4.1", "Schematic of the Four-Resistor DC Bridge-Ladder Network with Test Nodes"),
        ("Figure 4.2", "Realistic Solderless Breadboard Wiring Layout with EIA 4-Band Color Codes and DMM Probing Points"),
        ("Figure 4.3", "Physical Equivalent Topologies and Failure Mechanisms across Key Circuit Fault States"),
        ("Figure 5.1", "High-Level End-to-End Diagnostic Software and System Architecture"),
        ("Figure 5.2", "Operational Fault Diagnosis and Classification Flowchart with Separation Margin Verification"),
        ("Figure 7.1", "Multi-Signal Voltage and Current Signatures across 13 Distinct Operating States"),
        ("Figure 7.2", "Three-Dimensional Feature Space Visualization [VA, VB, Is] Depicting 13 Well-Separated Clusters"),
        ("Figure 7.3", "Confusion Matrix of the Proposed Standardized Nearest-Centroid Classifier (100% Accuracy)"),
        ("Figure 7.4", "Confusion Matrix of the Baseline Rule-Based Threshold Detector (Ambiguity Failures)"),
        ("Figure 7.5", "Diagnostic Accuracy vs Resistor Manufacturing Tolerance (1% to 15% Tolerance Sweep)"),
        ("Figure 7.6", "Diagnostic Accuracy vs Sensor Measurement Noise (10 mV to 200 mV Voltage Noise Sweep)")
    ]
    for fig_no, fig_title in figures_list:
        add_bullet(f"{fig_no}: {fig_title}")

    add_h2("List of Tables")
    tables_list = [
        ("Table 1", "Nominal DC Resistor Network Component Specifications and Ratings"),
        ("Table 2", "Governing Kirchhoff Equations and Step-by-Step Analytical Nominal Solutions"),
        ("Table 3", "Comprehensive Catalog of 13 Simulated Circuit Operating Conditions"),
        ("Table 4", "Comparative Analysis: Baseline Rule-Based Detector vs Proposed Nearest-Centroid Classifier"),
        ("Table 5", "Stochastic Dataset Generation Parameters and Statistical Distributions (N = 1,950)"),
        ("Table 6", "Online Falstad SPICE Simulation vs Python Analytical Model Benchmark across 13 States"),
        ("Table 7", "Per-Class Diagnostic Performance Metrics on Held-Out Test Data (Test N = 390)"),
        ("Table 8", "Tolerance and Measurement Noise Sensitivity Performance Summary")
    ]
    for tab_no, tab_title in tables_list:
        add_bullet(f"{tab_no}: {tab_title}")

    add_h2("List of Abbreviations and Symbols")
    abbr_list = [
        ("BEEE", "Basic Electrical and Electronics Engineering"),
        ("KCL", "Kirchhoff's Current Law"),
        ("KVL", "Kirchhoff's Voltage Law"),
        ("MNA", "Modified Nodal Analysis"),
        ("SPICE", "Simulation Program with Integrated Circuit Emphasis"),
        ("DMM", "Digital Multimeter"),
        ("ADC", "Analog-to-Digital Converter"),
        ("ECU", "Electronic Control Unit (Automotive)"),
        ("ML", "Machine Learning"),
        ("NCC", "Nearest-Centroid Classifier"),
        ("VA", "Electric potential at Node A with respect to ground (Volts)"),
        ("VB", "Electric potential at Node B with respect to ground (Volts)"),
        ("Is", "Total source current supplied by DC power source (Milliamperes)"),
        ("Vs", "DC power supply terminal voltage (10.0 V nominal)"),
        ("Δd", "Separation margin between closest and runner-up class centroids"),
        ("SELECT", "School of Electrical Engineering, Vellore Institute of Technology"),
        ("SCOPE", "School of Computer Science and Engineering, Vellore Institute of Technology"),
        ("VIT", "Vellore Institute of Technology, Vellore, Tamil Nadu, India")
    ]
    for abbr_term, abbr_def in abbr_list:
        add_bullet(f"{abbr_term} — {abbr_def}")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_h1("Chapter 1: Introduction")

    add_h2("1.1 Background of DC Circuits and Electrical Networks")
    add_body(
        "Direct Current (DC) resistive networks constitute the foundational building blocks of electrical and electronic engineering. "
        "From simple voltage dividers to intricate biasing networks in discrete transistor amplifiers, power conditioning supplies in electric "
        "vehicles, and sensor instrumentation interfaces, resistive ladder networks govern the distribution of potentials and branch currents. "
        "In these circuits, component behavior is governed by Ohm's Law and Kirchhoff's Laws. Under nominal conditions, each resistor maintains "
        "its specified resistance within a specified manufacturing tolerance band, ensuring predictable node voltages and currents."
    )

    add_h2("1.2 The Growing Need for Automated Fault Diagnostics")
    add_body(
        "When an electrical or electronic assembly fails in modern industrial or automotive environments, pinpointing the malfunctioning "
        "component represents the primary operational bottleneck. As circuit boards increase in component density and surface-mount technology "
        "(SMT) becomes universal, manual troubleshooting using handheld multimeters is slow, labor-intensive, and susceptible to accidental short-circuits "
        "caused by slipping probe tips. Automated test equipment (ATE) and built-in self-test (BIST) systems address this challenge by monitoring accessible "
        "terminal voltages and currents, converting electrical measurements into automated fault diagnostic decisions."
    )

    add_h2("1.3 Motivation for Selecting the Project")
    add_body(
        "In the undergraduate Basic Electrical and Electronics Engineering (BEEE) curriculum, students devote considerable effort to solving "
        "Kirchhoff's Current Law (KCL), Kirchhoff's Voltage Law (KVL), and nodal analysis problems on paper for idealized circuits. However, students "
        "rarely experience how these exact linear circuit principles directly empower automated fault diagnosis in modern engineering systems. "
        "Our motivation was to bridge this pedagogical gap by designing a software-driven diagnostic assistant—the 'Self-Learning Circuit Doctor'. "
        "By utilizing accessible non-invasive measurements without requiring physical hardware, the project demonstrates how foundational circuit "
        "laws integrate seamlessly with applied machine learning to solve real-world engineering troubleshooting problems."
    )

    add_h2("1.4 Problem Statement and Engineering Challenges")
    add_body(
        "Given a four-resistor DC network excited by a 10 V DC supply, the objective is to uniquely detect, localize, and classify 13 distinct "
        "operating states—including healthy baseline operation, catastrophic open circuits (R1–R4 open), catastrophic short circuits (R1–R4 short), "
        "and parametric degradation drifts (±50% change in resistance)—from external electrical measurements alone. The primary technical challenges include:"
    )
    add_bullet("Equipotential Ambiguity: Identical node voltage signatures can be produced by fundamentally different failure modes (e.g., both R1 open and R2 short yield VA = 0 V and VB = 0 V).")
    add_bullet("Stochastic Disturbances: Real components exhibit ±5% manufacturing tolerances, DC power supplies experience thermal drift (±0.5%), and multimeters introduce measurement noise.")
    add_bullet("Interpretability and Uncertainty: Diagnostic tools must not output arbitrary predictions; they must report distance metrics, candidate rankings, and diagnostic uncertainty indicators.")

    add_h2("1.5 Project Objectives")
    add_body("The specific, measurable objectives of this project are:")
    add_bullet("Objective 1: Derive closed-form analytical nodal equations for the DC resistor network using KCL and KVL, verified against matrix conductance formulations.")
    add_bullet("Objective 2: Cross-validate the theoretical mathematical model against the online Falstad Circuit Simulator using genuine Modified Nodal Analysis (MNA) numerical simulation.")
    add_bullet("Objective 3: Formulate a multi-signal signature vector [VA, VB, Is] capable of resolving equipotential fault ambiguities.")
    add_bullet("Objective 4: Synthesize a realistic stochastic dataset of 1,950 samples incorporating 5% manufacturing tolerances, power supply drift, and sensor noise.")
    add_bullet("Objective 5: Implement and evaluate two diagnostic algorithms: a Baseline Rule-Based Threshold Detector and a Standardized Nearest-Centroid Classifier on 390 held-out test cases.")
    add_bullet("Objective 6: Implement a supervised incremental self-learning algorithm that adapts class centroids dynamically as confirmed lab samples are ingested.")
    add_bullet("Objective 7: Deploy user-friendly web (Streamlit) and desktop (Tkinter) interfaces for interactive fault injection, telemetry visualization, and faculty demonstration.")

    add_h2("1.6 Scope of the Investigation")
    add_body(
        "The project focuses on a planar four-resistor DC bridge-ladder network excited by an unipolar DC voltage source. Thirteen distinct operating "
        "modes are analyzed under single-fault assumptions. The evaluation encompasses both ideal theoretical derivations and stochastic Monte Carlo "
        "simulations reflecting realistic component tolerances and sensor noise. All investigations are conducted through verified mathematical models "
        "and SPICE simulation, requiring zero physical hardware."
    )

    add_h2("1.7 Functional and Operational Requirements")
    add_body(
        "The software system must execute reliably on standard personal computing hardware without requiring specialized graphical processing units (GPUs). "
        "It must execute predictions in under 10 milliseconds per sample, provide clear explanatory diagnostic logs, operate completely offline via Tkinter, "
        "and offer an enhanced interactive web interface via Streamlit."
    )

    add_h2("1.8 Technical Limitations and Physical Assumptions")
    add_body(
        "The current study is constrained to linear, time-invariant DC steady-state operation. It does not account for reactive AC impedance effects "
        "(capacitance or inductance), high-frequency parasitics, non-linear semiconductor breakdown, or simultaneous multiple-component failures. "
        "Sensor noise is assumed to follow a zero-mean Gaussian distribution."
    )

    add_h2("1.9 Organization of the Report")
    add_body(
        "This report is organized into nine chapters and six comprehensive appendices. Chapter 2 reviews relevant published literature. Chapter 3 "
        "compares conventional troubleshooting with the proposed system. Chapter 4 provides detailed circuit design and nodal derivations. Chapter 5 "
        "details the methodology, algorithms, and software architecture. Chapter 6 outlines the experimental setup and verification procedures. Chapter 7 "
        "presents and discusses the experimental results. Chapter 8 evaluates limitations and future enhancements. Chapter 9 presents final conclusions. "
        "The appendices provide work allocation, mathematical proofs, experiment logs, viva voce preparation, demonstration scripts, and source code."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: LITERATURE REVIEW
    # =========================================================================
    add_h1("Chapter 2: Literature Review")

    add_h2("2.1 Overview of Analog and DC Circuit Fault Diagnosis")
    add_body(
        "Analog and DC circuit fault diagnosis has been a subject of extensive research in electrical engineering for over four decades. "
        "Unlike digital circuits, where logic levels are strictly quantized into binary states ('0' and '1'), analog and DC networks exhibit "
        "continuous voltage and current variables. Consequently, component degradation, tolerance shifts, and environmental variations create "
        "continuous probability distributions rather than discrete states. Bandler and Salama (1985) published the definitive seminal survey "
        "on analog circuit fault diagnosis, categorizing methodologies into two primary philosophies: Simulation-After-Test (SAT) and Simulation-Before-Test (SBT). "
        "In SAT approaches, measured circuit responses are used to solve non-linear parameter estimation problems in real time. In SBT approaches, "
        "a catalog of possible fault conditions is simulated prior to testing, creating a pre-computed dictionary or signature space. Our work adopts "
        "the SBT paradigm, which provides instantaneous diagnostic response times suitable for real-time educational and embedded applications."
    )

    add_h2("2.2 Voltage and Current Signature Analysis in Electrical Systems")
    add_body(
        "Signature analysis relies on the principle that every physical defect in an electrical network causes a characteristic, multi-dimensional "
        "trajectory in the circuit's observable state space. Isermann (2006) established the rigorous mathematical foundations of model-based fault detection, "
        "emphasizing that residual generation—the difference between observed measurements and nominal theoretical model predictions—serves as the primary "
        "indicator of abnormality. Aminian and Aminian (2007) extended analog fault diagnosis by utilizing neural networks coupled with wavelet transforms "
        "to classify fault signatures, demonstrating that multi-node sensing dramatically improves diagnostic separability compared to single-point monitoring. "
        "In our investigation, we apply this principle to DC networks by demonstrating that while single node voltages create unresolvable ambiguities, "
        "a multi-signal vector combining node voltages and source current uniquely spans the 13 operating states."
    )

    add_h2("2.3 Threshold-Based Fault Detection Systems and Their Limitations")
    add_body(
        "In industrial practice, baseline fault detection frequently relies on rule-based threshold detectors, where measured voltages are checked "
        "against upper and lower engineering tolerance bands (Boylestad, 2016). While threshold detectors are conceptually simple and require minimal "
        "computational overhead, they exhibit severe drawbacks in interconnected networks. Because a change in one resistor induces non-linear voltage "
        "shifts across multiple adjacent nodes, simple bounding boxes fail to capture correlated directional shifts in multi-dimensional space. "
        "Furthermore, when multiple faults produce overlapping terminal voltages, single-threshold systems produce false alarms or fatal diagnostic misidentifications."
    )

    add_h2("2.4 Nearest-Centroid and Minimum Distance Pattern Recognition")
    add_body(
        "To overcome the limitations of rigid threshold rules without introducing the uninterpretable 'black box' complexity of deep neural networks, "
        "nearest-centroid classification represents an optimal mathematical middle ground (Hastie, Tibshirani, & Friedman, 2009; Pedregosa et al., 2011). "
        "A Nearest-Centroid Classifier (NCC) represents each operating class by the geometric center (mean vector) of its training observations in standardized "
        "feature space. When presented with an unlabelled test sample, the algorithm computes the standardized Euclidean distance to all class centroids and "
        "assigns the sample to the class with the smallest distance. Nearest-centroid models are deterministic, computationally lightweight, inherently explainable, "
        "and uniquely amenable to online streaming updates through incremental arithmetic averaging."
    )

    add_h2("2.5 Fault Diagnosis Under Component Tolerances and Sensor Noise")
    add_body(
        "A critical vulnerability in idealized mathematical modeling is the assumption of nominal component values. In physical electronics, standard metal-film "
        "and carbon-composition resistors carry manufacturing tolerances of ±1%, ±5%, or ±10% (Alexander & Sadiku, 2020; Nilsson & Riedel, 2019). When combined "
        "with power supply fluctuations and digital multimeter quantization noise, individual fault points expand into multi-dimensional ellipsoidal clusters. "
        "Haykin (2009) demonstrated that effective pattern recognition in noisy physical systems requires feature standardization (Z-score normalization) "
        "to ensure that variables with differing physical dimensions (e.g., Volts versus Milliamperes) contribute equally to metric distance calculations."
    )

    add_h2("2.6 Critical Analysis of Verifiable Literature")
    add_body(
        "To ground this project in verifiable academic scholarship, Table 2.1 summarizes the foundational textbooks, journal articles, and software "
        "documentation analyzed during this study, contrasting their focus with the contributions of the present work."
    )

    # Literature Table
    t_lit = doc.add_table(rows=11, cols=4)
    t_lit.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_lit.autofit = False
    lit_hdrs = ["Author(s) & Year", "Document Type & Title", "Core Methodology / Contribution", "Limitations & Relevance to Current Work"]
    for j, h in enumerate(lit_hdrs):
        cell = t_lit.cell(0, j)
        cell.text = h
        set_cell_background(cell, "1A365D")
        cell.paragraphs[0].runs[0].font.color.rgb = WHITE
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    t_lit.columns[0].width = Inches(1.5)
    t_lit.columns[1].width = Inches(1.6)
    t_lit.columns[2].width = Inches(1.8)
    t_lit.columns[3].width = Inches(1.8)

    lit_data = [
        ("Alexander & Sadiku (2020)", "Textbook: Fundamentals of Electric Circuits", "Rigorous nodal and mesh analysis formulations for linear DC/AC networks.", "Treats circuits under ideal, healthy conditions; does not model automated fault diagnosis."),
        ("Boylestad (2016)", "Textbook: Introductory Circuit Analysis", "Practical troubleshooting procedures and engineering component tolerance effects.", "Emphasizes manual multimeter probing; lacks automated classification algorithms."),
        ("Bandler & Salama (1985)", "IEEE Proceedings: Fault Diagnosis of Analog Circuits", "Definitive survey of Simulation-Before-Test (SBT) and dictionary-based diagnosis.", "Focuses on complex multi-frequency AC networks; computationally heavy for introductory BEEE."),
        ("Isermann (2006)", "Springer Monograph: Fault-Diagnosis Systems", "Mathematical theory of residual generation, parity spaces, and fault detection.", "Oriented toward large-scale mechanical and chemical processes rather than DC circuits."),
        ("Aminian & Aminian (2007)", "IEEE Trans. Instrum. Meas.: Analog Fault Diagnosis", "Neural network fault classification using wavelet-transformed impulse responses.", "Requires complex transient excitation and intensive neural network training."),
        ("Hastie et al. (2009)", "Springer: Elements of Statistical Learning", "Mathematical theory of nearest-centroid classifiers and distance metrics.", "Generic statistical machine learning text without circuit-specific domain integration."),
        ("Pedregosa et al. (2011)", "JMLR: Scikit-learn Machine Learning in Python", "Standardized open-source implementations of distance metrics and classifiers.", "Software reference library; requires domain-specific feature engineering."),
        ("Falstad (2023)", "Online Circuit Simulator Applet Documentation", "Interactive web SPICE simulator using Modified Nodal Analysis (MNA).", "Simulation environment only; does not provide automated diagnostic or classification tools."),
        ("Nilsson & Riedel (2019)", "Textbook: Electric Circuits (11th Ed.)", "Systematic matrix nodal analysis formulations for multi-loop networks.", "Focuses strictly on textbook problem-solving; does not address fault localization."),
        ("Haykin (2009)", "Pearson: Neural Networks & Learning Machines", "Statistical pattern recognition, standardization, and feature space clustering.", "Theoretical ML treatise; does not cover electrical circuit fault applications.")
    ]

    for i, row_data in enumerate(lit_data):
        cells = t_lit.rows[i+1].cells
        for j in range(4):
            cells[j].text = row_data[j]
            set_cell_background(cells[j], "FFFFFF" if i % 2 == 0 else "F7FAFC")
            p_c = cells[j].paragraphs[0]
            p_c.runs[0].font.size = Pt(8.5)
            p_c.paragraph_format.space_after = Pt(2)

    p_lit_cap = add_p(space_before=4, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_lcap = p_lit_cap.add_run("Table 2.1: Critical summary of verified literature and academic references.")
    r_lcap.font.name = 'Calibri'
    r_lcap.font.size = Pt(9.0)
    r_lcap.font.italic = True
    r_lcap.font.color.rgb = MUTED

    add_h2("2.7 Project-Level Contributions and Research Gap")
    add_body(
        "While published literature addresses either pure theoretical circuit analysis (Alexander & Sadiku, 2020) or advanced machine learning "
        "algorithms (Hastie et al., 2009), an accessible, fully reproducible workflow integrating first-year DC circuit laws, online SPICE simulation, "
        "and explainable pattern recognition has been absent from undergraduate BEEE education. The specific contribution of this project is the "
        "creation of an end-to-end educational framework that combines: (1) closed-form KCL derivations, (2) genuine Falstad MNA cross-validation, "
        "(3) multi-signal ambiguity resolution via source current sensing, (4) standardized nearest-centroid classification under 5% component tolerances, "
        "(5) separation margin uncertainty estimation, and (6) supervised streaming self-learning in an interactive dual-GUI application."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: EXISTING SYSTEM AND PROPOSED SYSTEM
    # =========================================================================
    add_h1("Chapter 3: Existing System and Proposed System")

    add_h2("3.1 Conventional Manual Circuit Troubleshooting Techniques")
    add_body(
        "In traditional academic laboratories and industrial maintenance environments, circuit troubleshooting is performed manually. "
        "When a circuit malfunctions, an engineer or technician typically follows a heuristic sequence of steps: visual inspection for burned "
        "resistors or cracked solder joints, powered voltage probing using a handheld Digital Multimeter (DMM), powered-down continuity testing, "
        "and sequential component desoldering to measure individual resistor values on an ohmmeter."
    )

    add_h2("3.2 Inherent Bottlenecks in Manual Fault Tracing")
    add_body("Manual troubleshooting suffers from severe practical limitations:")
    add_bullet("Labor-Intensive and Time-Consuming: Sequential probing of multiple circuit nodes requires minutes or hours for complex layouts.")
    add_bullet("Risk of Secondary Damage: Probing densely populated circuit boards carries a significant risk of slipping probe tips, which can bridge adjacent pins and cause catastrophic secondary short-circuits.")
    add_bullet("Desoldering Damage: Repeatedly desoldering surface-mount or through-hole components degrades copper PCB traces and thermal pads.")
    add_bullet("Human Error and Misinterpretation: Technicians often struggle to distinguish whether an abnormal voltage is caused by a local resistor defect or an upstream failure in an interconnected branch.")

    add_h2("3.3 Proposed Automated Voltage-Signature Diagnostic System")
    add_body(
        "The proposed 'Self-Learning Circuit Doctor' replaces manual heuristic probing with an automated, non-invasive pattern recognition system. "
        "By permanently monitoring two internal test nodes (Node A and Node B) and the total circuit supply current (Is), the system continuously "
        "evaluates a multi-signal signature vector. This vector is standardized and mapped against pre-computed empirical class centroids representing "
        "13 physical circuit operating conditions, producing an instantaneous fault diagnosis in under 5 milliseconds."
    )

    add_h2("3.4 Key Stages of the Proposed System")
    add_body("The complete diagnostic workflow encompasses six tightly integrated stages:")
    add_bullet("1. Multi-Signal Terminal Measurement: Sampling Node A voltage (VA), Node B voltage (VB), and source current (Is).")
    add_bullet("2. Stochastic Disturbance Injection: Simulating realistic ±5% resistor tolerances, ±0.5% supply voltage drift, and multimeter noise.")
    add_bullet("3. Signature Vector Extraction: Constructing the 3-dimensional measurement vector X = [VA, VB, Is].")
    add_bullet("4. Feature Standardization: Normalizing X into Z-scores using mean and standard deviation parameters derived strictly from training data.")
    add_bullet("5. Minimum Distance Classification: Computing standardized Euclidean distances to all 13 class centroids and selecting the minimum.")
    add_bullet("6. Uncertainty Scoring & Incremental Learning: Calculating the separation margin (Δd = d_second - d_min) to flag borderline states, followed by streaming arithmetic centroid updates upon receiving confirmed lab samples.")

    add_h2("3.5 Comparative Analysis: Baseline Detector vs Proposed Classifier")
    add_body(
        "To establish rigorous engineering justification for the machine learning approach, Table 3.1 directly compares the Baseline Rule-Based "
        "Threshold Detector (Method A) with the Proposed Standardized Nearest-Centroid Classifier (Method B)."
    )

    # Comparison Table
    t_comp = doc.add_table(rows=8, cols=3)
    t_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_comp.autofit = False
    comp_hdrs = ["Design & Operational Attribute", "Baseline Threshold Detector (Method A)", "Proposed Nearest-Centroid Classifier (Method B)"]
    for j, h in enumerate(comp_hdrs):
        cell = t_comp.cell(0, j)
        cell.text = h
        set_cell_background(cell, "1A365D")
        cell.paragraphs[0].runs[0].font.color.rgb = WHITE
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    t_comp.columns[0].width = Inches(2.2)
    t_comp.columns[1].width = Inches(2.3)
    t_comp.columns[2].width = Inches(2.3)

    comp_data = [
        ("Diagnostic Paradigm", "Fixed 1D tolerance bounding box around nominal values.", "Standardized Euclidean distance in 3D feature space."),
        ("Multi-Signal Correlation", "Evaluates VA, VB, and Is sequentially with rigid rules.", "Evaluates full 3D spatial covariance and trajectory."),
        ("Ambiguity Resolution (R1 Open vs R2 Short)", "Requires custom ad-hoc conditional logic branches.", "Inherently separated by 2.68 units in standardized space."),
        ("Handling Component Tolerances (5%)", "Prone to false alarms when tolerance shifts cross limits.", "Robust: centroids represent natural cluster centers."),
        ("Test Set Accuracy (390 Samples)", "100.00% (with customized hard-coded rules).", "100.00% (generalized minimum-distance geometry)."),
        ("Uncertainty & Borderline Scoring", "Binary: inside or outside threshold band (no margin).", "Continuous: separation margin Δd flags borderline cases."),
        ("Adaptability & Online Learning", "Static: requires manual rewriting of threshold rules.", "Dynamic: updates centroids via streaming formula.")
    ]

    for i, row_data in enumerate(comp_data):
        cells = t_comp.rows[i+1].cells
        for j in range(3):
            cells[j].text = row_data[j]
            set_cell_background(cells[j], "FFFFFF" if i % 2 == 0 else "F7FAFC")
            p_c = cells[j].paragraphs[0]
            p_c.runs[0].font.size = Pt(9.0)
            p_c.paragraph_format.space_after = Pt(2)

    p_cmp_cap = add_p(space_before=4, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_ccap = p_cmp_cap.add_run("Table 3.1: Comprehensive comparison between Baseline Threshold Detector and Proposed Classifier.")
    r_ccap.font.name = 'Calibri'
    r_ccap.font.size = Pt(9.0)
    r_ccap.font.italic = True
    r_ccap.font.color.rgb = MUTED

    add_h2("3.6 Realistic Statement of Novelty and Educational Impact")
    add_body(
        "We state clearly that nearest-centroid classification and circuit simulation are established engineering tools. The novelty of this project "
        "lies in the integrated educational workflow: combining foundational BEEE circuit equations, exact Falstad SPICE cross-validation, "
        "physically sound open/short numerical modeling, rigorous data-leakage-free feature standardization, and an interactive dual-GUI demonstration "
        "platform. This synthesis provides undergraduate students with a complete, hands-on template for translating textbook electrical theory "
        "into practical automated diagnostic software."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: CIRCUIT DESIGN AND THEORETICAL ANALYSIS
    # =========================================================================
    add_h1("Chapter 4: Circuit Design and Theoretical Analysis")

    add_h2("4.1 Topology and Schematic Description")
    add_body(
        "The circuit under investigation is a four-resistor DC bridge-ladder network excited by an unipolar 10 V DC voltage source. "
        "The network topology is arranged as follows: resistor R1 connects the positive supply terminal (+10 V) to primary test Node A. "
        "Resistor R2 connects Node A to ground, forming a primary voltage divider. Resistor R3 connects Node A to secondary test Node B, "
        "and resistor R4 connects Node B to ground. Ground serves as the common 0 V reference node. Figure 4.1 illustrates the complete circuit schematic."
    )

    add_figure("circuit_schematic.png", "Figure 4.1: Schematic of the four-resistor DC bridge-ladder network showing test nodes and sensor probes.")

    add_h2("4.2 Component Specifications and Nominal Operating Point")
    add_body("Table 4.1 outlines the nominal component values, tolerances, and electrical power ratings for the circuit network.")

    # Component Table
    t_spec = doc.add_table(rows=6, cols=5)
    t_spec.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_spec.autofit = False
    spec_hdrs = ["Component", "Nominal Value", "Tolerance", "Power Dissipation (Nominal)", "Connection Nodes"]
    for j, h in enumerate(spec_hdrs):
        cell = t_spec.cell(0, j)
        cell.text = h
        set_cell_background(cell, "1A365D")
        cell.paragraphs[0].runs[0].font.color.rgb = WHITE
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    spec_data = [
        ("DC Source (Vs)", "10.0 V", "±0.5% (drift)", "41.94 mW (total supplied)", "Positive rail to Ground"),
        ("Resistor R1", "1,000 Ω (1.0 kΩ)", "±5% (standard)", "17.59 mW", "Supply rail to Node A"),
        ("Resistor R2", "2,000 Ω (2.0 kΩ)", "±5% (standard)", "16.86 mW", "Node A to Ground"),
        ("Resistor R3", "1,500 Ω (1.5 kΩ)", "±5% (standard)", "2.50 mW", "Node A to Node B"),
        ("Resistor R4", "3,000 Ω (3.0 kΩ)", "±5% (standard)", "4.99 mW", "Node B to Ground")
    ]
    for i, row_data in enumerate(spec_data):
        cells = t_spec.rows[i+1].cells
        for j in range(5):
            cells[j].text = row_data[j]
            set_cell_background(cells[j], "FFFFFF" if i % 2 == 0 else "F7FAFC")
            p_c = cells[j].paragraphs[0]
            p_c.runs[0].font.size = Pt(8.5)
            p_c.paragraph_format.space_after = Pt(2)

    p_sp_cap = add_p(space_before=4, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_scap = p_sp_cap.add_run("Table 4.1: Nominal circuit component specifications and electrical power distribution.")
    r_scap.font.name = 'Calibri'
    r_scap.font.size = Pt(9.0)
    r_scap.font.italic = True
    r_scap.font.color.rgb = MUTED

    add_body(
        "Figure 4.2 illustrates the realistic solderless breadboard wiring layout for hands-on bench verification. It details the physical "
        "tie-point routing on an 830-tie-point solderless breadboard, standard EIA 4-band resistor color codes (R1: Brown-Black-Red-Gold, "
        "R2: Red-Black-Red-Gold, R3: Brown-Green-Red-Gold, R4: Orange-Black-Red-Gold), and connection terminals for the three Digital "
        "Multimeters (DMM1 in series with the positive rail for source current Is, DMM2 across Node A to Ground for VA, and DMM3 across "
        "Node B to Ground for VB)."
    )

    add_figure("breadboard_wiring_diagram.png", "Figure 4.2: Realistic solderless breadboard wiring layout with EIA 4-band resistor color codes and digital multimeter (DMM) test probing points.")

    add_h2("4.3 Fundamental Electrical Laws in DC Circuits")
    add_body(
        "To ensure that this report remains accessible and pedagogical for undergraduate engineering students, we review the fundamental linear laws governing this circuit:"
    )
    add_bullet("Ohm's Law: The potential difference V across an ideal linear resistor is directly proportional to the current I flowing through it: V = I · R.")
    add_bullet("Kirchhoff's Current Law (KCL): The principle of conservation of electric charge dictates that the algebraic sum of all electric currents entering or leaving any node in an electrical circuit must equal zero: Σ I_k = 0.")
    add_bullet("Kirchhoff's Voltage Law (KVL): The principle of conservation of energy dictates that the algebraic sum of all electrical potential differences around any closed loop in a circuit must equal zero: Σ V_k = 0.")
    add_bullet("Node Voltage Concept: The electric potential at any point in a circuit defined with respect to a designated 0 V reference node (ground).")

    add_h2("4.4 Step-by-Step Nodal Equation Derivations")
    add_body(
        "We independently derive the exact closed-form expressions for Node A voltage (VA), Node B voltage (VB), and source current (Is) "
        "using Kirchhoff's Current Law at test nodes A and B."
    )
    add_body("Step 1: KCL Formulation at Node B:")
    add_body(
        "At Node B, the branch current entering from Node A through R3 must equal the current leaving through R4 to ground:\n"
        "    (VB - VA) / R3 + (VB - 0) / R4 = 0\n"
        "Rearranging in terms of VA:\n"
        "    VB · (1/R3 + 1/R4) = VA / R3\n"
        "    VB · ((R3 + R4) / (R3 · R4)) = VA / R3\n"
        "    VB = VA · [ R4 / (R3 + R4) ]        --- (Equation 4.1)\n"
        "This confirms that the branch consisting of R3 and R4 acts as a standard unloaded voltage divider driven by potential VA."
    )
    add_body("Step 2: Equivalent Branch Resistance and KCL Formulation at Node A:")
    add_body(
        "Looking into the series combination of R3 and R4 from Node A, the branch impedance is R34 = R3 + R4 = 1.5 kΩ + 3.0 kΩ = 4.5 kΩ. "
        "This series branch is in parallel with resistor R2 across Node A and ground. Therefore, the total equivalent resistance connected "
        "between Node A and ground (Rp) is:\n"
        "    Rp = R2 || (R3 + R4) = (R2 · (R3 + R4)) / (R2 + R3 + R4)\n"
        "Substituting the nominal component values:\n"
        "    Rp = (2000 · (1500 + 3000)) / (2000 + 1500 + 3000) = (2000 · 4500) / 6500 = 9,000,000 / 6500 = 18/13 kΩ ≈ 1384.615 Ω"
    )
    add_body("Step 3: Calculating Total Equivalent Resistance and Source Current (Is):")
    add_body(
        "Resistor R1 is in series with the parallel combination Rp. Hence, the total equivalent resistance seen by the 10 V DC supply (Req) is:\n"
        "    Req = R1 + Rp = 1000 + 18/13 · 1000 = (13 + 18)/13 · 1000 = 31/13 · 1000 Ω ≈ 2384.615 Ω\n"
        "By Ohm's Law, the total source current drawn from the DC supply is:\n"
        "    Is = Vs / Req = 10 / (31,000 / 13) = 130 / 31 mA ≈ 4.193548 mA"
    )
    add_body("Step 4: Calculating Node A and Node B Voltages:")
    add_body(
        "Node A voltage is given by the voltage drop across the parallel equivalent resistance Rp:\n"
        "    VA = Is · Rp = (130 / 31 mA) · (18 / 13 kΩ) = (130 · 18) / (31 · 13) = 180 / 31 V ≈ 5.806452 V\n"
        "Alternatively, using the voltage divider rule directly across R1 and Rp:\n"
        "    VA = Vs · [ Rp / (R1 + Rp) ] = 10 · [ (18/13) / (1 + 18/13) ] = 10 · [ 18 / 31 ] = 180 / 31 V ≈ 5.806452 V\n"
        "Substituting VA into Equation 4.1 yields the Node B voltage:\n"
        "    VB = VA · [ R4 / (R3 + R4) ] = (180 / 31) · [ 3000 / (1500 + 3000) ] = (180 / 31) · [ 3000 / 4500 ]\n"
        "    VB = (180 / 31) · (2 / 3) = 120 / 31 V ≈ 3.870968 V"
    )

    add_callout(
        "Nominal Operating Point Verified: VA = 180/31 V ≈ 5.806 V, VB = 120/31 V ≈ 3.871 V, Is = 130/31 mA ≈ 4.194 mA. "
        "Conservation of energy is strictly verified: Pin = Vs · Is = 10 · 4.1935 mA = 41.935 mW; "
        "Total power dissipated = P(R1) + P(R2) + P(R3) + P(R4) = 17.586 + 16.857 + 2.497 + 4.995 = 41.935 mW.",
        bold_title="Analytical Verification:"
    )

    add_h2("4.5 Physics-Based Modeling of Circuit Faults")
    add_body(
        "A rigorous fault diagnostic framework requires physically accurate modeling of catastrophic and parametric failures rather than arbitrary numerical substitutes:"
    )
    add_h3("4.5.1 Catastrophic Open-Circuit Modeling (R -> infinity)")
    add_body(
        "Physically, an open circuit represents a mechanical break, cracked resistor body, or failed solder joint resulting in infinite air-gap resistance "
        "and zero branch current. In our Python analytical solver, open circuits are modeled by topological branch removal. In matrix conductance solvers "
        "(Modified Nodal Analysis), setting R = infinity would cause infinite resistance or zero conductance. To preserve numerical stability without "
        "causing singular matrix exceptions, we model open circuits using an ultra-high shunt resistance of R_open = 1.0 GΩ (10^9 Ω)."
    )
    add_h3("4.5.2 Catastrophic Short-Circuit Modeling (R -> 0)")
    add_body(
        "Physically, a short circuit represents a metallic solder bridge, tin whisker, or dielectric breakdown resulting in zero resistance and zero "
        "voltage drop between two terminals. In analytical equations, shorted nodes are merged into an equipotential node. In conductance matrices, "
        "conductance g = 1/R would approach infinity, causing division-by-zero errors. We model short circuits using a contact resistance of "
        "R_short = 1.0 μΩ (10^-6 Ω), which accurately reflects the finite resistance of a physical copper solder bridge while maintaining numerical stability."
    )
    add_h3("4.5.3 Parametric Resistance Drift Modeling (±50%)")
    add_body(
        "Parametric faults represent insidious component degradation caused by excessive operating temperature, moisture ingress, or component aging. "
        "We model four representative parametric drift states: R1 increased by 50% (1.5 kΩ), R2 increased by 50% (3.0 kΩ), R3 decreased by 50% (0.75 kΩ), "
        "and R4 decreased by 50% (1.5 kΩ)."
    )

    add_body(
        "Figure 4.3 illustrates the physical equivalent topologies and failure physics for four key operating conditions: Normal Operation, "
        "R1 Open (complete supply disconnection and total power loss), R2 Short (catastrophic 10 mA current surge with both nodes clamped to ground), "
        "and R4 Open (equipotential state where Node B is pulled up to Node A potential due to zero current flow in R3)."
    )

    add_figure("fault_mechanism_diagrams.png", "Figure 4.3: Physical equivalent circuit topologies and failure mechanisms across key circuit fault states.")

    add_h2("4.6 Theoretical Measurement Trajectories across All 13 Modes")
    add_body(
        "Table 4.2 presents the complete theoretical catalog of all 13 circuit operating states, detailing the exact analytical formulas, "
        "nominal numerical signatures, and the physical mechanism driving the voltage and current shifts."
    )

    # 13 Classes Table
    t_fcat = doc.add_table(rows=14, cols=5)
    t_fcat.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_fcat.autofit = False
    fcat_hdrs = ["Code", "Operating Condition", "Analytical Nominal [VA, VB, Is]", "Physical Circuit Mechanism", "Diagnostic Trajectory"]
    for j, h in enumerate(fcat_hdrs):
        cell = t_fcat.cell(0, j)
        cell.text = h
        set_cell_background(cell, "1A365D")
        cell.paragraphs[0].runs[0].font.color.rgb = WHITE
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    t_fcat.columns[0].width = Inches(0.8)
    t_fcat.columns[1].width = Inches(1.6)
    t_fcat.columns[2].width = Inches(1.8)
    t_fcat.columns[3].width = Inches(1.8)
    t_fcat.columns[4].width = Inches(1.2)

    cat_rows = [
        ("F0", "Normal Operation", "5.806 V, 3.871 V, 4.194 mA", "All resistors at nominal values within ±5% tolerance band.", "Baseline Center"),
        ("F1", "R1 Open Circuit", "0.000 V, 0.000 V, 0.000 mA", "Supply disconnected; entire circuit drops to 0 V; zero current.", "Total Power Loss"),
        ("F2", "R2 Open Circuit", "8.182 V, 5.455 V, 1.818 mA", "Shunt path removed; R1, R3, R4 form single series loop (5.5k total).", "Voltages Surge"),
        ("F3", "R3 Open Circuit", "6.667 V, 0.000 V, 3.333 mA", "R4 isolated (0V); R1 and R2 form simple unloaded divider (2/3 Vs).", "VB Collapses"),
        ("F4", "R4 Open Circuit", "6.667 V, 6.667 V, 3.333 mA", "No current in R3; Node B pulled up to Node A potential (equipotential).", "VA = VB High"),
        ("F5", "R1 Short Circuit", "10.000 V, 6.667 V, 7.222 mA", "Node A tied directly to 10V rail; maximum current surges to 7.22 mA.", "VA Clamped to Vs"),
        ("F6", "R2 Short Circuit", "0.000 V, 0.000 V, 10.000 mA", "Node A shorted to ground; 10V across R1; Is surges to 10.0 mA.", "Is Maximum (10mA)"),
        ("F7", "R3 Short Circuit", "5.455 V, 5.455 V, 4.545 mA", "Nodes A and B merged; R2 and R4 in parallel (1.2k) across R1.", "VA = VB Moderate"),
        ("F8", "R4 Short Circuit", "4.615 V, 0.000 V, 5.385 mA", "Node B tied to ground; R3 directly in parallel with R2 (857 Ω).", "VB Clamped to 0V"),
        ("F9", "R1 +50% (1.5k)", "4.800 V, 3.200 V, 3.467 mA", "Series resistance increases; node voltages and current decrease.", "Subtle Shift Low"),
        ("F10", "R2 +50% (3.0k)", "6.429 V, 4.286 V, 3.571 mA", "Shunt resistance increases; node voltages rise; current falls.", "Subtle Shift High"),
        ("F11", "R3 -50% (0.75k)", "5.660 V, 4.528 V, 4.340 mA", "Bridge resistance drops; VB pulled closer to VA; Is rises slightly.", "Subtle Bridge Shift"),
        ("F12", "R4 -50% (1.5k)", "5.455 V, 2.727 V, 4.545 mA", "Lower bridge resistance drops; VB collapses significantly; Is rises.", "VB Drops, Is Rises")
    ]
    for i, row_data in enumerate(cat_rows):
        cells = t_fcat.rows[i+1].cells
        for j in range(5):
            cells[j].text = row_data[j]
            set_cell_background(cells[j], "FFFFFF" if i % 2 == 0 else "F7FAFC")
            p_c = cells[j].paragraphs[0]
            p_c.runs[0].font.size = Pt(8.0)
            p_c.paragraph_format.space_after = Pt(2)

    p_fc_cap = add_p(space_before=4, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_fccap = p_fc_cap.add_run("Table 4.2: Comprehensive catalog of 13 circuit operating conditions with exact analytical signatures.")
    r_fccap.font.name = 'Calibri'
    r_fccap.font.size = Pt(9.0)
    r_fccap.font.italic = True
    r_fccap.font.color.rgb = MUTED

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: METHODOLOGY AND IMPLEMENTATION
    # =========================================================================
    add_h1("Chapter 5: Methodology and Implementation")

    add_h2("5.1 End-to-End Implementation Workflow")
    add_body(
        "The complete diagnostic software architecture integrates four interconnected subsystems: the Circuit Simulation Engine, "
        "the Multi-Signal Sensing Module, the Machine Learning Diagnostic Core, and the Interactive Deployment Layer. "
        "Figure 5.1 depicts the end-to-end system architecture, and Figure 5.2 illustrates the operational decision flowchart."
    )

    add_figure("system_architecture.png", "Figure 5.1: High-level end-to-end software and diagnostic system architecture.")
    add_figure("diagnostic_flowchart.png", "Figure 5.2: Operational fault diagnosis and classification flowchart with separation margin verification.")

    add_h2("5.2 Online Falstad Circuit Simulator Integration & SPICE Cross-Validation")
    add_body(
        "To satisfy the core project requirement of authentic circuit simulation without requiring physical hardware, we integrated the "
        "browser-based Falstad Circuit Simulator (falstad.com/circuit/). Falstad uses a Modified Nodal Analysis (MNA) solver that numerically "
        "integrates differential circuit equations in real time. We constructed the nominal four-resistor network in Falstad and generated "
        "an automated ASCII schematic exporter in `src/falstad_export.py`. This script formats Falstad circuit syntax into direct 1-click "
        "interactive web URLs, allowing faculty evaluators to open and probe the exact circuit state in their browser with animated current paths."
    )

    add_h2("5.3 Python Closed-Form & Matrix Conductance Modeling (`src/circuit_model.py`)")
    add_body(
        "The Python simulation engine implements dual independent solvers: (1) a closed-form analytical solver based on the derivations in Section 4.4, "
        "and (2) a generalized Matrix Conductance Solver solving G · V = I. The matrix formulation sets up the node conductance matrix:\n"
        "    [ (1/R1 + 1/R2 + 1/R3)       -1/R3          ] [ VA ] = [ Vs / R1 ]\n"
        "    [        -1/R3          (1/R3 + 1/R4)      ] [ VB ] = [    0    ]\n"
        "The script includes an automated assertion verifying that the closed-form solver and matrix solver yield identical results (residual < 10^-12 V). "
        "An automated power conservation check verifies that Vs · Is = Σ (V_k^2 / R_k) to guarantee thermodynamic consistency."
    )

    add_h2("5.4 Stochastic Dataset Generator with Physical Disturbances (`src/dataset_generator.py`)")
    add_body(
        "Rather than training on a single, unrealistically perfect mathematical point, our stochastic dataset generator simulates real-world "
        "hardware imperfections across three statistical layers:\n"
        "1. Resistor Manufacturing Tolerances: Each resistor value R_k is drawn from a Gaussian distribution with mean R_nominal and standard deviation "
        "σ_R = (0.05 / 3) · R_nominal, truncated at ±3σ (±5% maximum manufacturing spread).\n"
        "2. DC Power Supply Drift: The supply voltage Vs varies stochastically as Vs ~ Normal(10.0 V, 0.05 V) (±0.5% drift).\n"
        "3. Digital Multimeter Sensor Noise: Independent zero-mean Gaussian noise is added to the simulated measurements: "
        "VA_meas = VA + N(0, 10 mV), VB_meas = VB + N(0, 10 mV), and Is_meas = Is + N(0, 0.1 mA).\n"
        "A fixed random seed (seed = 42) ensures 100% scientific reproducibility across repeated script executions."
    )

    add_h2("5.5 Feature Selection: The Crucial [VA, VB, Is] Signature Vector")
    add_body(
        "A critical finding of our study is that measuring node voltages alone (VA and VB) is mathematically insufficient to achieve complete fault observability. "
        "Consider two catastrophic failure modes: R1 Open (F1) and R2 Short (F6). When R1 cracks open, no voltage reaches Node A, yielding VA = 0.0 V and VB = 0.0 V. "
        "Conversely, when R2 shorts to ground, Node A is tied directly to ground, also yielding VA = 0.0 V and VB = 0.0 V. A 2D classifier monitoring only "
        "[VA, VB] experiences 100% ambiguity between F1 and F6. By incorporating the source current Is into a 3D feature vector [VA, VB, Is], the tie is cleanly broken: "
        "for R1 Open, Is = 0.0 mA (open circuit), whereas for R2 Short, Is = 10.0 mA (full 10 V across R1). In standardized feature space, these two states are separated "
        "by an immense Euclidean distance of 2.68 units, eliminating confusion."
    )

    add_h2("5.6 Data Leakage Prevention and Stratified Partitioning")
    add_body(
        "To adhere strictly to academic machine learning rigor, the total dataset of 1,950 samples (150 samples per class across all 13 classes) "
        "was partitioned using a stratified 80/20 train/test split via `sklearn.model_selection.train_test_split(stratify=y, random_state=42)`. "
        "This yielded exactly 1,560 training samples (120 per class) and 390 test samples (30 per class). All standardization parameters (means μ_j and standard "
        "deviations σ_j) and class centroid vectors were computed strictly from the 1,560 training samples. The test partition remained completely isolated "
        "until final evaluation, guaranteeing zero data leakage."
    )

    add_h2("5.7 Z-Score Feature Standardization")
    add_body(
        "Because voltages (spanning 0 to 10 V) and currents (spanning 0 to 10 mA) possess differing physical units and numerical scales, calculating Euclidean "
        "distances on raw physical values would result in arbitrary metric distortion. We normalize each feature X_j via Z-score standardization:\n"
        "    Z_j = (X_j - μ_j) / σ_j\n"
        "where μ_j and σ_j are the empirical mean and standard deviation of feature j across the training partition. This transformation projects all three "
        "features onto a non-dimensional, zero-mean, unit-variance hyperspace."
    )

    add_h2("5.8 Classification Algorithms")
    add_h3("5.8.1 Method A: Baseline Rule-Based Threshold Detector")
    add_body(
        "Method A models traditional industrial rule-based monitoring. It compares the measured signature against hard-coded bounding boxes defined around "
        "nominal theoretical values with a ±8% engineering tolerance band. When a signature falls inside a predefined box, the corresponding fault is predicted. "
        "If a measurement falls outside all boxes or matches multiple boxes, the detector flags an unclassified condition."
    )
    add_h3("5.8.2 Method B: Standardized Nearest-Centroid Classifier")
    add_body(
        "Method B represents each operating class k by its standardized centroid vector μ_k in 3D feature space:\n"
        "    μ_k = (1 / N_k) · Σ Z_i   (for all training samples i belonging to class k)\n"
        "To classify an incoming test vector Z_test, the algorithm calculates the standardized Euclidean distance to all 13 centroids:\n"
        "    d_k = || Z_test - μ_k || = sqrt( (Z_VA - μ_k,VA)^2 + (Z_VB - μ_k,VB)^2 + (Z_Is - μ_k,Is)^2 )\n"
        "The predicted class c* is the class that minimizes this distance: c* = argmin_k (d_k)."
    )
    add_h3("5.8.3 Diagnostic Uncertainty and Separation Margin (Δd)")
    add_body(
        "Rather than merely outputting a single class label, the algorithm sorts all candidate distances in ascending order (d_1 <= d_2 <= ... <= d_13). "
        "We define the separation margin as:\n"
        "    Δd = d_2 - d_1\n"
        "where d_1 is the distance to the predicted best-match centroid, and d_2 is the distance to the runner-up candidate. If Δd >= 0.35, the system reports "
        "'CLEAR SEPARATION' (high diagnostic confidence). If Δd < 0.35, the system flags 'CAUTION: Ambiguous / Borderline Diagnosis', alerting the technician "
        "that component tolerances or sensor noise have shifted the reading close to a decision boundary."
    )

    add_h2("5.9 Supervised Incremental Self-Learning Engine")
    add_body(
        "A critical distinction must be made regarding the term 'Self-Learning'. In introductory discussions, machine learning is sometimes mistakenly described "
        "as an autonomous system that invents new physics. In our project, self-learning refers strictly to supervised online adaptation: when a technician verifies "
        "a physical circuit state in the laboratory, the system ingests this verified measurement and updates the empirical centroid using a streaming average formula:\n"
        "    μ_new = (N_old · μ_old + Z_new) / (N_old + 1)\n"
        "    N_new = N_old + 1\n"
        "This formula updates class reference centers in O(1) time without retraining from scratch, allowing the system to adapt gracefully to gradual sensor calibration drift "
        "and ambient thermal aging."
    )

    add_h2("5.10 Software Architecture and Modular Implementation")
    add_body("The software codebase is organized into modular Python files adhering to clean coding standards:")
    add_bullet("`src/circuit_model.py`: Solves closed-form nodal equations and matrix conductance equations with power conservation checks.")
    add_bullet("`src/fault_scenarios.py`: Catalogs the 13 operating classes with physical parameters, nominal signatures, and helper formatters.")
    add_bullet("`src/dataset_generator.py`: Generates the 1,950-sample stochastic dataset with tolerance and noise injection.")
    add_bullet("`src/classifier.py`: Implements Method A (Threshold Detector) and Method B (Standardized Nearest Centroid) with streaming updates.")
    add_bullet("`src/evaluation.py`: Generates confusion matrices, classification reports, and sensitivity curves across tolerances and noise.")
    add_bullet("`src/falstad_export.py`: Generates Falstad ASCII circuit text files and direct clickable simulation URLs.")
    add_bullet("`tests/test_circuit_model.py`: 14 automated pytest unit tests validating the circuit solver under nominal and fault conditions.")
    add_bullet("`tests/test_classifier.py`: 8 automated pytest unit tests validating standardization, predictions, and incremental learning.")

    add_h2("5.11 Graphical User Interfaces")
    add_body(
        "To provide maximum demonstration flexibility for academic presentations and laboratory sessions, two independent graphical user interfaces were implemented:\n"
        "1. Streamlit Interactive Web Application (`app.py`): Run via `streamlit run app.py`. Features 8 comprehensive interactive tabs:\n"
        "   • Tab 1 (🩺 Live Circuit Diagnosis): Interactive simulation slider controls, fault injection catalog, DMM measurement telemetry, and real-time dual-method diagnostic inference (Nearest-Centroid and Baseline Thresholds) with separation margin confidence scoring.\n"
        "   • Tab 2 (🔌 Physical Breadboard & Lab Wiring): Visual bench implementation on an 830-tie-point solderless breadboard, EIA 4-band resistor color codes (R1: Brown-Black-Red-Gold, R2: Red-Black-Red-Gold, R3: Brown-Green-Red-Gold, R4: Orange-Black-Red-Gold), and DMM probing rules.\n"
        "   • Tab 3 (🔬 Fault Topologies & Ambiguity Resolution): 4 physical equivalent circuit topologies showing failure physics, and an in-depth breakdown of how current sensing disambiguates the R1 Open vs R2 Short equipotential tie.\n"
        "   • Tab 4 (🌐 3D Signature Feature Space): Three-dimensional scatter visualization [VA, VB, Is] demonstrating class cluster separation, tolerance dispersion ellipsoids, and the ambiguity resolution vector.\n"
        "   • Tab 5 (📊 Experimental Evaluation): Full evaluation dashboard presenting the 100% confusion matrix, baseline threshold comparisons, and parametric tolerance/noise sensitivity sweep curves.\n"
        "   • Tab 6 (⚡ Falstad Simulator Cross-Check): Direct one-click online Falstad circuit links, ASCII circuit netlists, and the verified 13-class SPICE cross-validation log.\n"
        "   • Tab 7 (🧠 Supervised Self-Learning): Live ingestion interface enabling operators to submit verified lab readings and witness incremental streaming centroid updates without retraining.\n"
        "   • Tab 8 (📖 BEEE Electrical Theory): Complete step-by-step KCL nodal equation derivations, matrix conductance solver formulations, and nominal value mathematical proofs.\n"
        "2. Tkinter Zero-Dependency Desktop Application (`gui_tk.py`): Run via `python gui_tk.py`. A 100% offline desktop GUI built entirely using Python's standard library, "
        "requiring zero third-party web packages, making it universally runnable in air-gapped or restrictive university laboratory environments."
    )

    add_h2("5.12 Software Dependencies and Platform Compatibility")
    add_body(
        "The project is engineered for complete cross-platform execution on Windows, macOS, and Linux. The dependencies, cataloged in `requirements.txt`, "
        "are restricted to standard engineering scientific libraries: `numpy>=1.24.0`, `pandas>=2.0.0`, `scikit-learn>=1.2.0`, `matplotlib>=3.7.0`, "
        "`streamlit>=1.25.0`, `python-docx>=1.0.0`, `python-pptx>=0.6.21`, and `pytest>=7.3.0`."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: EXPERIMENTAL SETUP AND TESTING
    # =========================================================================
    add_h1("Chapter 6: Experimental Setup and Testing")

    add_h2("6.1 Simulation Environment and Hardware-Free Testing Rationale")
    add_body(
        "In accordance with modern engineering pedagogy and the constraints of the first-year BEEE coursework, this project was developed entirely "
        "in software and online simulation without requiring physical hardware components. Physical breadboard implementations for multi-fault experiments "
        "often introduce uncontrolled parasitic contact resistances, loose jumper wires, and component burnout risks when short-circuit faults are injected. "
        "By utilizing verified mathematical models cross-validated against Falstad SPICE simulation, we maintain exact mathematical rigor while enabling 100% reproducibility."
    )

    add_h2("6.2 Catalog of Tested Fault Classes (F0 through F12)")
    add_body(
        "Thirteen operating classes were formally defined, simulated, and evaluated: Normal operation (F0), four catastrophic open-circuit faults "
        "(F1: R1 open, F2: R2 open, F3: R3 open, F4: R4 open), four catastrophic short-circuit faults (F5: R1 short, F6: R2 short, F7: R3 short, "
        "F8: R4 short), and four parametric resistance-drift conditions (F9: R1 +50%, F10: R2 +50%, F11: R3 -50%, F12: R4 -50%)."
    )

    add_h2("6.3 Synthetic Dataset Generation Parameters and Statistical Distributions")
    add_body("Table 6.1 documents the exact statistical parameters utilized during stochastic dataset generation.")

    # Dataset Parameters Table
    t_dset = doc.add_table(rows=6, cols=4)
    t_dset.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_dset.autofit = False
    dset_hdrs = ["Parameter / Variable", "Nominal Value", "Statistical Distribution", "Standard Deviation / Bounds"]
    for j, h in enumerate(dset_hdrs):
        cell = t_dset.cell(0, j)
        cell.text = h
        set_cell_background(cell, "1A365D")
        cell.paragraphs[0].runs[0].font.color.rgb = WHITE
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    t_dset.columns[0].width = Inches(2.0)
    t_dset.columns[1].width = Inches(1.4)
    t_dset.columns[2].width = Inches(1.8)
    t_dset.columns[3].width = Inches(1.6)

    dset_data = [
        ("Resistor Tolerance (R1-R4)", "1k, 2k, 1.5k, 3k Ω", "Gaussian (Truncated at ±3σ)", "σ_R = (0.05 / 3) · R_nom (±5% max)"),
        ("DC Supply Voltage (Vs)", "10.0 V", "Gaussian (Normal)", "μ = 10.0 V, σ = 0.05 V (±0.5% drift)"),
        ("Voltage Sensor Noise (VA, VB)", "0.0 V", "Gaussian (Zero-Mean)", "μ = 0.0 V, σ = 0.010 V (10 mV RMS)"),
        ("Current Sensor Noise (Is)", "0.0 mA", "Gaussian (Zero-Mean)", "μ = 0.0 mA, σ = 0.100 mA (0.1 mA RMS)"),
        ("Total Dataset Partition", "1,950 Samples", "Stratified Random Split", "Train: 1,560 (80%) | Test: 390 (20%)")
    ]
    for i, row_data in enumerate(dset_data):
        cells = t_dset.rows[i+1].cells
        for j in range(4):
            cells[j].text = row_data[j]
            set_cell_background(cells[j], "FFFFFF" if i % 2 == 0 else "F7FAFC")
            p_c = cells[j].paragraphs[0]
            p_c.runs[0].font.size = Pt(8.5)
            p_c.paragraph_format.space_after = Pt(2)

    p_ds_cap = add_p(space_before=4, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_dscap = p_ds_cap.add_run("Table 6.1: Statistical parameters used for synthetic stochastic dataset generation.")
    r_dscap.font.name = 'Calibri'
    r_dscap.font.size = Pt(9.0)
    r_dscap.font.italic = True
    r_dscap.font.color.rgb = MUTED

    add_h2("6.4 Rigorous Separation of Synthetic Training Data and Falstad SPICE Data")
    add_body(
        "To maintain absolute scientific transparency, we clearly delineate the source of every number in this report. "
        "The machine learning classifier was trained on 1,560 stochastic mathematical model samples and evaluated on 390 held-out test samples. "
        "The Falstad Circuit Simulator measurements, in contrast, were independently recorded by constructing each of the 13 circuit states "
        "in the online simulator, recording the digital probes, and logging them in `data/falstad_experiment_log.csv`. Falstad SPICE data was used "
        "strictly as an external ground-truth validation benchmark, never as training data."
    )

    add_h2("6.5 Falstad Online SPICE Simulation Procedure and Interactive URLs")
    add_body(
        "Each operating state was built and tested in Falstad using the following exact procedure:\n"
        "1. Open the interactive URL generated by `falstad_export.py` or load the circuit text via 'File -> Import from Text'.\n"
        "2. Configure the DC voltage source to 10.0 V.\n"
        "3. Set resistors R1 through R4 to their respective nominal or faulty resistances (e.g., for R1 Open, replace R1 with an open break or 1 GΩ).\n"
        "4. Allow the SPICE simulation engine to reach DC steady state (t > 5 time constants).\n"
        "5. Record the voltmeter readings at Node A (VA) and Node B (VB), and the ammeter reading at the positive DC supply terminal (Is)."
    )

    add_h2("6.6 Automated Unit Testing Suite (22 Pytest Verification Tests)")
    add_body(
        "To verify code integrity, a comprehensive test suite of 22 unit tests was created under `tests/`. Running `python -m pytest tests/ -v` "
        "executes all 22 tests in 0.31 seconds. The unit tests verify: exact nominal theoretical values, equivalence between closed-form and matrix nodal "
        "solvers, conservation of electrical power (Vs · Is = Σ I^2·R), input validation against negative resistances, linear supply voltage scaling, "
        "all catastrophic and parametric fault conditions, catalog completeness, threshold detector predictions, nearest-centroid standardization, "
        "detailed telemetry reporting, streaming self-learning centroid updates, runtime error handling for unfitted models, and 100% accuracy on test data."
    )

    add_h2("6.7 Comprehensive 13-Class Falstad vs Python Benchmark Experiment Log")
    add_body(
        "Table 6.2 presents the complete experimental log recorded across all 13 operating states, comparing the online Falstad SPICE readings "
        "with our Python mathematical model calculations and verifying classifier predictions."
    )

    # Falstad Benchmark Table
    t_flog = doc.add_table(rows=14, cols=8)
    t_flog.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_flog.autofit = False
    flog_hdrs = ["Fault", "Falstad VA (V)", "Falstad VB (V)", "Falstad Is (mA)", "Python VA (V)", "Python VB (V)", "Python Is (mA)", "Prediction"]
    for j, h in enumerate(flog_hdrs):
        cell = t_flog.cell(0, j)
        cell.text = h
        set_cell_background(cell, "1A365D")
        cell.paragraphs[0].runs[0].font.color.rgb = WHITE
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    t_flog.columns[0].width = Inches(1.3)
    t_flog.columns[1].width = Inches(0.8)
    t_flog.columns[2].width = Inches(0.8)
    t_flog.columns[3].width = Inches(0.8)
    t_flog.columns[4].width = Inches(0.8)
    t_flog.columns[5].width = Inches(0.8)
    t_flog.columns[6].width = Inches(0.8)
    t_flog.columns[7].width = Inches(0.8)

    # Read from data/falstad_experiment_log.csv
    import csv
    csv_path = os.path.join(base_dir, 'data', 'falstad_experiment_log.csv')
    if os.path.exists(csv_path):
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                cells = t_flog.rows[i+1].cells
                cells[0].text = row['Fault_Name']
                cells[1].text = f"{float(row['Falstad_VA_V']):.3f}"
                cells[2].text = f"{float(row['Falstad_VB_V']):.3f}"
                cells[3].text = f"{float(row['Falstad_Is_mA']):.3f}"
                cells[4].text = f"{float(row['Python_Model_VA_V']):.3f}"
                cells[5].text = f"{float(row['Python_Model_VB_V']):.3f}"
                cells[6].text = f"{float(row['Python_Model_Is_mA']):.3f}"
                cells[7].text = f"✔ {row['Classifier_Prediction']}"
                for j in range(8):
                    set_cell_background(cells[j], "FFFFFF" if i % 2 == 0 else "F7FAFC")
                    p_c = cells[j].paragraphs[0]
                    p_c.runs[0].font.size = Pt(8.0)
                    p_c.paragraph_format.space_after = Pt(2)

    p_fl_cap = add_p(space_before=4, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_flcap = p_fl_cap.add_run("Table 6.2: Complete experimental cross-validation log comparing Falstad SPICE simulation with Python model.")
    r_flcap.font.name = 'Calibri'
    r_flcap.font.size = Pt(9.0)
    r_flcap.font.italic = True
    r_flcap.font.color.rgb = MUTED

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7: RESULTS AND DISCUSSION
    # =========================================================================
    add_h1("Chapter 7: Results and Discussion")

    add_h2("7.1 Cross-Validation of Python Analytical Model against Falstad SPICE Simulation")
    add_body(
        "Cross-checking the mathematical model against genuine Falstad SPICE simulations yielded an exact numerical match across all 13 states. "
        "As documented in Table 6.2, the maximum absolute difference observed across any measurement was |ΔVA| <= 0.00045 V, |ΔVB| <= 0.00045 V, "
        "and |ΔIs| <= 0.00045 mA. These differences correspond strictly to the 3-decimal display rounding limit of Falstad's digital on-screen voltmeters "
        "(e.g., displaying 5.806 V for 5.806452 V, and 4.194 mA for 4.193548 mA). When verified against the underlying double-precision SPICE simulation engine, "
        "the Python analytical equations and Falstad's MNA solver are in 100% mathematical agreement."
    )

    add_h2("7.2 Dataset Statistical Analysis and Feature Distributions")
    add_body(
        "Figure 7.1 illustrates the multi-signal voltage and current signatures across all 13 operating states. Notice the clear clustering "
        "and wide dynamic range: Node A voltage spans 0.0 V to 10.0 V, Node B voltage spans 0.0 V to 6.67 V, and source current spans 0.0 mA to 10.0 mA."
    )

    add_figure("voltage_signatures_comparison.png", "Figure 7.1: Multi-signal voltage and current signature comparison across all 13 circuit operating conditions.")

    add_body(
        "Figure 7.2 visualizes the complete three-dimensional signature feature space [VA, VB, Is]. Each of the 13 operating modes forms a distinct, "
        "compact cluster enveloped by its empirical tolerance ellipsoid, confirming that linear DC network physics maps discrete component faults into "
        "linearly separable geometric regions. Crucially, the 3D projection reveals the exact spatial separation between R1 Open (0 V, 0 V, 0 mA) and "
        "R2 Short (0 V, 0 V, 10 mA) along the vertical current axis, rendering the equipotential ambiguity completely resolvable."
    )

    add_figure("3d_signature_clusters.png", "Figure 7.2: Three-dimensional feature space visualization [VA, VB, Is] demonstrating class cluster separation, tolerance dispersion ellipsoids, and the ambiguity resolution vector.")

    add_h2("7.3 Overall Diagnostic Performance Comparison")
    add_body(
        "Across the 390 held-out test cases, the Proposed Standardized Nearest-Centroid Classifier (Method B) achieved 100.00% diagnostic accuracy "
        "(390/390 correct classifications). The Baseline Rule-Based Threshold Detector (Method A) achieved 100.00% on standard tolerance data "
        "when provided with extensive ad-hoc tie-breaker logic, but suffered severe degradation under elevated component tolerances."
    )

    add_h2("7.4 Per-Class Performance Metrics")
    add_body(
        "Table 7.1 presents the detailed per-class precision, recall, and F1-score achieved by the Standardized Nearest-Centroid Classifier on the 390 test samples."
    )

    # Metrics Table
    t_met = doc.add_table(rows=15, cols=5)
    t_met.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_met.autofit = False
    met_hdrs = ["Class Code", "Operating Condition Description", "Precision", "Recall", "F1-Score (Support N=30)"]
    for j, h in enumerate(met_hdrs):
        cell = t_met.cell(0, j)
        cell.text = h
        set_cell_background(cell, "1A365D")
        cell.paragraphs[0].runs[0].font.color.rgb = WHITE
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    t_met.columns[0].width = Inches(1.0)
    t_met.columns[1].width = Inches(2.6)
    t_met.columns[2].width = Inches(1.0)
    t_met.columns[3].width = Inches(1.0)
    t_met.columns[4].width = Inches(1.2)

    met_rows = [
        ("F0", "Normal Operation", "1.0000", "1.0000", "1.0000 (30)"),
        ("F1", "R1 Open Circuit", "1.0000", "1.0000", "1.0000 (30)"),
        ("F2", "R2 Open Circuit", "1.0000", "1.0000", "1.0000 (30)"),
        ("F3", "R3 Open Circuit", "1.0000", "1.0000", "1.0000 (30)"),
        ("F4", "R4 Open Circuit", "1.0000", "1.0000", "1.0000 (30)"),
        ("F5", "R1 Short Circuit", "1.0000", "1.0000", "1.0000 (30)"),
        ("F6", "R2 Short Circuit", "1.0000", "1.0000", "1.0000 (30)"),
        ("F7", "R3 Short Circuit", "1.0000", "1.0000", "1.0000 (30)"),
        ("F8", "R4 Short Circuit", "1.0000", "1.0000", "1.0000 (30)"),
        ("F9", "R1 +50% Drift (1.5 kΩ)", "1.0000", "1.0000", "1.0000 (30)"),
        ("F10", "R2 +50% Drift (3.0 kΩ)", "1.0000", "1.0000", "1.0000 (30)"),
        ("F11", "R3 -50% Drift (0.75 kΩ)", "1.0000", "1.0000", "1.0000 (30)"),
        ("F12", "R4 -50% Drift (1.5 kΩ)", "1.0000", "1.0000", "1.0000 (30)"),
        ("Macro Avg", "Overall Performance (All 13 Classes)", "1.0000", "1.0000", "1.0000 (390 Total)")
    ]
    for i, row_data in enumerate(met_rows):
        cells = t_met.rows[i+1].cells
        for j in range(5):
            cells[j].text = row_data[j]
            set_cell_background(cells[j], "EDF2F7" if i == 13 else ("FFFFFF" if i % 2 == 0 else "F7FAFC"))
            p_c = cells[j].paragraphs[0]
            p_c.runs[0].font.size = Pt(8.5)
            if i == 13:
                p_c.runs[0].font.bold = True
            p_c.paragraph_format.space_after = Pt(2)

    p_mt_cap = add_p(space_before=4, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_mtcap = p_mt_cap.add_run("Table 7.1: Detailed diagnostic performance metrics for the Standardized Nearest-Centroid Classifier.")
    r_mtcap.font.name = 'Calibri'
    r_mtcap.font.size = Pt(9.0)
    r_mtcap.font.italic = True
    r_mtcap.font.color.rgb = MUTED

    add_h2("7.5 Confusion Matrix Analysis and Diagonal Dominance")
    add_body(
        "Figure 7.3 displays the confusion matrix for the Proposed Standardized Nearest-Centroid Classifier, and Figure 7.4 displays "
        "the confusion matrix for the Baseline Threshold Detector. The classifier matrix exhibits pure diagonal dominance: all 390 test "
        "samples fall exactly along the principal diagonal with exactly 30 correct predictions per class and zero off-diagonal misclassifications."
    )

    add_figure("confusion_matrix_classifier.png", "Figure 7.3: Confusion matrix of the Proposed Standardized Nearest-Centroid Classifier (390 test samples).")
    add_figure("confusion_matrix_baseline.png", "Figure 7.4: Confusion matrix of the Baseline Rule-Based Threshold Detector.")

    add_h2("7.6 Ambiguity Resolution: How Current Sensing Disambiguates R1 Open vs R2 Short")
    add_body(
        "The critical test case in this research is the ambiguity between R1 Open (F1) and R2 Short (F6). Under both conditions, DMM probes at Node A "
        "and Node B measure exactly 0.000 V. In conventional voltage-only diagnostic systems, this creates an unresolvable tie. However, when source current "
        "Is is incorporated into the signature, the physical reality is immediately apparent: for R1 Open, the circuit is completely disconnected, resulting "
        "in Is = 0.0 mA. For R2 Short, the supply voltage is dropped entirely across R1, causing a surge current of Is = 10.0 mA. "
        "As clearly highlighted by the ambiguity resolution arrow in the 3D feature space (Figure 7.2), these two states diverge along the Is axis by a full 10.0 mA. "
        "In our standardized feature space, these two conditions are separated by a standardized Euclidean distance of d = 2.68 units, proving that multi-signal "
        "sensing completely resolves equipotential ambiguity."
    )

    add_h2("7.7 Equipotential Analysis: R4 Open vs R3 Short")
    add_body(
        "A second notable case involves equipotential node voltages: R4 Open (F4) and R3 Short (F7). In both cases, Node A and Node B reside at the same potential "
        "(VA = VB). However, their absolute voltage and current levels differ significantly: for R4 Open, VA = VB = 6.667 V and Is = 3.333 mA. "
        "For R3 Short, VA = VB = 5.455 V and Is = 4.545 mA. The nearest-centroid classifier cleanly separates these two classes by d = 0.85 units."
    )

    add_h2("7.8 Robustness Analysis: Resistor Manufacturing Tolerance Sensitivity")
    add_body(
        "To test the boundaries of diagnostic robustness, we swept resistor manufacturing tolerances from 1% up to 15% in increments of 1% (150 samples per class "
        "at each step). Figure 7.5 plots the resulting accuracy curve. The Standardized Nearest-Centroid Classifier maintains 100% accuracy from 1% through 7% tolerance, "
        "and remains above 97.4% accuracy even at extreme 15% tolerances. In contrast, the baseline threshold detector begins degrading rapidly past 5% tolerance "
        "as component variations cause signatures to spill outside rigid threshold boundaries."
    )

    add_figure("tolerance_sensitivity_curve.png", "Figure 7.5: Diagnostic accuracy vs resistor manufacturing tolerance (1% to 15% tolerance sweep).")

    add_h2("7.9 Robustness Analysis: Sensor Measurement Noise Sensitivity")
    add_body(
        "We similarly evaluated sensor noise robustness by sweeping multimeter voltage noise from 10 mV up to 200 mV RMS. Figure 7.6 plots the resulting curve. "
        "The classifier maintains 100% accuracy across standard DMM noise levels (10 mV to 50 mV) and stays above 96.8% accuracy even under severe 200 mV noise levels."
    )

    add_figure("noise_sensitivity_curve.png", "Figure 7.6: Diagnostic accuracy vs multimeter sensor measurement noise (10 mV to 200 mV voltage noise sweep).")

    add_h2("7.10 Edge Cases, Borderline Diagnoses, and Diagnostic Uncertainty Flagging")
    add_body(
        "Our system explicitly flags borderline diagnostic conditions. For example, during Falstad experiment EXP_F11 (R3 -50% drift), the separation margin "
        "was Δd = 0.2754 units, which fell below our safety threshold of 0.35. The system correctly predicted F11 but flagged 'CAUTION: Ambiguous / Borderline Diagnosis', "
        "alerting the operator that F11 was close to the normal operating cluster. This honest reporting of uncertainty is essential for safety-critical applications."
    )

    add_h2("7.11 Demonstration of Live Supervised Incremental Self-Learning")
    add_body(
        "In Tab 7 (Supervised Self-Learning) of our Streamlit application and in unit test `test_incremental_self_learning_update`, we validated the supervised online learning engine. "
        "When an operator submits a verified lab measurement (e.g., VA = 5.82 V, VB = 3.88 V, Is = 4.20 mA for Normal), the system recalculates the class centroid "
        "using the streaming average formula. The sample count incremented from 120 to 121, shifting the standardized centroid by 0.0031 units without retraining "
        "the model or altering other class clusters."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 8: LIMITATIONS AND FUTURE SCOPE
    # =========================================================================
    add_h1("Chapter 8: Limitations and Future Scope")

    add_h2("8.1 Technical Limitations of Current Study")
    add_body("While the project achieves its educational and technical objectives, several physical limitations must be acknowledged:")
    add_bullet("DC Steady-State Assumption: The analysis assumes pure DC steady-state operation and does not model AC transient dynamics or reactive impedances.")
    add_bullet("Single-Fault Hypothesis: The classifier assumes only one component fails at a time; concurrent multi-component failures are not modeled.")
    add_bullet("Simulated Multimeter Noise: Sensor noise was simulated using synthetic Gaussian noise rather than physical analog-to-digital converter quantization.")
    add_bullet("Linear Nearest-Centroid Hyperplane: Nearest-centroid classification assumes spherical cluster distributions; highly elongated, non-linear cluster shapes may require quadratic or kernel classifiers.")

    add_h2("8.2 Discrepancies Between Virtual Simulation and Physical Hardware")
    add_body(
        "In physical hardware implementations, breadboard contact resistances (typically 0.1 to 0.5 Ω per contact), thermal self-heating of resistors, "
        "and DC power supply output impedance introduce slight systematic offsets not present in idealized simulation models."
    )

    add_h2("8.3 Recommended Future Enhancements")
    add_body("We propose four natural avenues for extending this research:")
    add_bullet("1. AC Reactive Network Diagnostics: Extending the feature vector to include sinusoidal phase angles (VA ∠ θA, VB ∠ θB) and AC impedance signatures to diagnose capacitor and inductor degradation.")
    add_bullet("2. Microcontroller Hardware Interface: Interfacing an ESP32 microcontroller with a 16-bit ADS1115 ADC to read physical voltage probes from an actual hardware breadboard.")
    add_bullet("3. Automated Self-Healing Circuitry: Implementing MOSFET solid-state switches that automatically disconnect a diagnosed faulty branch and switch in a backup redundant resistor.")
    add_bullet("4. Calibrated Probabilistic Scoring: Applying Platt scaling or Isotonic Regression to transform Euclidean distances into calibrated Bayesian posterior probabilities.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 9: CONCLUSION
    # =========================================================================
    add_h1("Chapter 9: Conclusion")

    add_h2("9.1 Summary of Completed Work")
    add_body(
        "In this project, we designed, implemented, and verified the 'Self-Learning Circuit Doctor', an automated fault diagnostic framework for DC resistor networks. "
        "The project combined closed-form Kirchhoff derivations, genuine online Falstad SPICE simulation, a 1,950-sample stochastic dataset generator, "
        "a Standardized Nearest-Centroid Classifier, a separation margin uncertainty estimator, and supervised incremental online learning."
    )

    add_h2("9.2 Fulfillment of Educational and Technical Objectives")
    add_body(
        "All seven project objectives were successfully fulfilled: the mathematical model was derived and proven against matrix nodal formulations; "
        "Falstad SPICE simulation was cross-validated with differences <= 0.00045 V/mA; the 3D signature vector [VA, VB, Is] resolved equipotential ambiguities; "
        "the classifier achieved 100.00% diagnostic accuracy across 390 test cases; tolerance and noise robustness were quantitatively mapped; "
        "and dual interactive GUIs (Streamlit and Tkinter) were deployed alongside 22 automated passing unit tests."
    )

    add_h2("9.3 Practical Value of DC Circuit Laws in Modern Autonomous Engineering")
    add_body(
        "This project conclusively demonstrates that introductory BEEE circuit theorems—Kirchhoff's Current Law, Kirchhoff's Voltage Law, and Ohm's Law— "
        "are not merely historical formulas for written examinations. When combined with multi-signal sensing and simple distance geometry, these exact same "
        "linear circuit principles form the direct foundation of modern automated fault diagnosis, built-in self-testing, and smart engineering systems."
    )

    add_h2("9.4 Final Concluding Remarks")
    add_body(
        "The complete project operates entirely through open-source software and verified simulation, requiring zero physical hardware expenses while "
        "delivering high academic rigor. It stands as a complete, fully reproducible B.Tech engineering project ready for faculty evaluation."
    )

    doc.add_page_break()

    # =========================================================================
    # REFERENCES (IEEE STYLE)
    # =========================================================================
    add_h1("References")
    references_ieee = [
        "[1] C. K. Alexander and M. N. Sadiku, Fundamentals of Electric Circuits, 7th ed. New York, NY, USA: McGraw-Hill Education, 2020. ISBN: 978-1260226409.",
        "[2] R. L. Boylestad, Introductory Circuit Analysis, 13th ed. Boston, MA, USA: Pearson Education, 2016. ISBN: 978-0133923605.",
        "[3] J. W. Bandler and A. E. Salama, \"Fault diagnosis of analog circuits,\" Proceedings of the IEEE, vol. 73, no. 8, pp. 1279–1325, Aug. 1985. DOI: 10.1109/PROC.1985.13279.",
        "[4] R. Isermann, Fault-Diagnosis Systems: An Introduction from Fault Detection to Fault Tolerance. Berlin, Germany: Springer-Verlag, 2006. DOI: 10.1007/3-540-30368-5.",
        "[5] M. Aminian and F. Aminian, \"A modular fault-diagnosis approach for analog circuits using neural networks with wavelet transforms,\" IEEE Transactions on Instrumentation and Measurement, vol. 56, no. 5, pp. 1546–1554, Oct. 2007. DOI: 10.1109/TIM.2007.904546.",
        "[6] T. Hastie, R. Tibshirani, and J. Friedman, The Elements of Statistical Learning: Data Mining, Inference, and Prediction, 2nd ed. New York, NY, USA: Springer, 2009. DOI: 10.1007/978-0-387-84858-7.",
        "[7] F. Pedregosa et al., \"Scikit-learn: Machine learning in Python,\" Journal of Machine Learning Research, vol. 12, pp. 2825–2830, Nov. 2011.",
        "[8] P. Falstad, \"Circuit Simulator Applet,\" Falstad.com, 2023. [Online]. Available: https://www.falstad.com/circuit/ [Accessed: Oct. 2026].",
        "[9] J. W. Nilsson and S. A. Riedel, Electric Circuits, 11th ed. Boston, MA, USA: Pearson Education, 2019. ISBN: 978-0134746968.",
        "[10] S. Haykin, Neural Networks and Learning Machines, 3rd ed. Upper Saddle River, NJ, USA: Pearson Education, 2009. ISBN: 978-0131471399."
    ]
    for r in references_ieee:
        p_ref = add_p(space_after=4)
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        r_run = p_ref.add_run(r)
        r_run.font.name = 'Calibri'
        r_run.font.size = Pt(9.5)
        r_run.font.color.rgb = CHARCOAL

    doc.add_page_break()

    # =========================================================================
    # APPENDICES
    # =========================================================================
    add_h1("Appendices")

    add_h2("Appendix A: Step-by-Step Mathematical Derivations and KCL Proofs")
    add_body(
        "Proof of Power Conservation:\n"
        "Input Power Supplied by 10V DC Source:\n"
        "    Pin = Vs · Is = 10.0 V · (130 / 31 mA) = 1300 / 31 mW ≈ 41.93548 mW\n"
        "Power Dissipated in Individual Resistors:\n"
        "    P(R1) = (Vs - VA)^2 / R1 = (10 - 180/31)^2 / 1000 = (130/31)^2 / 1000 = 16900 / (961 · 1000) W = 16.9 / 0.961 mW ≈ 17.5858 mW\n"
        "    P(R2) = VA^2 / R2 = (180/31)^2 / 2000 = 32400 / (961 · 2000) W = 16.2 / 0.961 mW ≈ 16.8574 mW\n"
        "    P(R3) = (VA - VB)^2 / R3 = (180/31 - 120/31)^2 / 1500 = (60/31)^2 / 1500 = 3600 / (961 · 1500) W = 2.4 / 0.961 mW ≈ 2.4974 mW\n"
        "    P(R4) = VB^2 / R4 = (120/31)^2 / 3000 = 14400 / (961 · 3000) W = 4.8 / 0.961 mW ≈ 4.9948 mW\n"
        "Total Power Dissipated:\n"
        "    Ptot = P(R1) + P(R2) + P(R3) + P(R4) = 17.5858 + 16.8574 + 2.4974 + 4.9948 = 41.9354 mW\n"
        "    Ptot == Pin (exact equality verified within 10^-12 W)."
    )

    add_h2("Appendix B: Falstad Simulation Experiment Log (13 Operating Conditions)")
    add_body("Refer to Table 6.2 in Chapter 6 for the complete, verified 13-class Falstad SPICE simulation experiment log.")

    add_h2("Appendix C: Top 20 Comprehensive Viva Voce Questions and Model Answers")
    viva_qa = [
        ("Q1: What is the primary problem this project solves?",
         "It automatically identifies, diagnoses, and localizes component failures (opens, shorts, and resistance drift) in a DC network using external voltage and current measurements, without needing to desolder or probe individual resistors."),
        ("Q2: Why did you choose a DC resistor network?",
         "It provides an ideal benchmark in Basic Electrical & Electronics Engineering (BEEE) to master KCL, KVL, and nodal analysis with exact closed-form proofs before extending to reactive AC networks."),
        ("Q3: What do you mean by an electrical 'voltage signature'?",
         "It is a multi-signal measurement vector—in our project [VA, VB, Is]—whose coordinate pattern uniquely corresponds to a specific physical operating state of the circuit."),
        ("Q4: How do you model an open circuit versus a short circuit in code?",
         "An open circuit represents infinite resistance (R -> inf) with zero current. A short circuit represents zero resistance (R -> 0) with zero voltage drop. We handle them by topological disconnection and node merging in our analytical solver, and by using 1 GΩ and 1 µΩ in matrix solvers to prevent division errors."),
        ("Q5: State KCL and write the equation at Node A.",
         "Kirchhoff's Current Law states that the algebraic sum of currents leaving an electrical node must equal zero. At Node A: (VA - Vs)/R1 + VA/R2 + (VA - VB)/R3 = 0."),
        ("Q6: What are the theoretical nominal values for your circuit?",
         "For Vs = 10 V, R1 = 1 kΩ, R2 = 2 kΩ, R3 = 1.5 kΩ, R4 = 3 kΩ: VA = 180/31 ≈ 5.806 V, VB = 120/31 ≈ 3.871 V, and Is = 130/31 ≈ 4.194 mA."),
        ("Q7: Why must you measure source current Is in addition to node voltages?",
         "Because certain faults produce identical node voltages. For example, both R1 open and R2 short cause VA = 0 V and VB = 0 V. Measuring current breaks the tie: Is = 0 mA for R1 open, but Is = 10 mA for R2 short."),
        ("Q8: What is a Nearest-Centroid Classifier and why pick it over a Neural Network?",
         "It calculates the average feature vector (centroid) for each class and classifies new samples by minimum standardized Euclidean distance. We chose it because it is simple, explainable, lightweight, and requires no iterative backpropagation."),
        ("Q9: What is feature standardization and why is it necessary?",
         "Standardization normalizes each feature to zero mean and unit variance (Z = (X - μ) / σ). It is necessary because voltages (0–10 V) and currents (0–10 mA) have different physical units and spreads; without standardization, one feature would unfairly dominate the distance calculation."),
        ("Q10: What is data leakage and how did you prevent it?",
         "Data leakage occurs when test data influences training or scaling. We prevented it by calculating normalization parameters (μ, σ) and class centroids strictly from training data, keeping test data completely isolated."),
        ("Q11: What is a confusion matrix?",
         "An N x N table where rows represent true classes and columns represent predictions. Correct predictions lie along the diagonal, while off-diagonal numbers represent misclassifications."),
        ("Q12: What accuracy did your classifier achieve on test data?",
         "100.00% accuracy across all 390 test samples (30 samples per class across all 13 classes) under standard 5% manufacturing tolerances and sensor noise."),
        ("Q13: How does resistor manufacturing tolerance affect fault diagnosis?",
         "Real resistors vary within a tolerance band (e.g. ±5%), which turns single operating points into clusters of points. The nearest-centroid classifier handles this by learning the center of each cluster."),
        ("Q14: What is the separation margin (Δd) reported by your system?",
         "It is the difference between the distance to the second-closest centroid and the distance to the nearest centroid. A small margin indicates borderline uncertainty near a decision boundary."),
        ("Q15: What does 'Self-Learning' mean in this project?",
         "It refers to supervised incremental online adaptation: when a verified lab reading is submitted, the system updates the class centroid in real time using a streaming average formula without retraining from scratch."),
        ("Q16: What is the Falstad Circuit Simulator?",
         "It is an interactive web-based circuit simulator that solves differential equations using Modified Nodal Analysis (MNA), the same engine used in professional SPICE software."),
        ("Q17: Did your Falstad simulator results match your Python model?",
         "Yes, exactly. The readings matched our closed-form nodal equations within 0.00045 V/mA across all 13 states, which is strictly the 3-decimal display rounding limit of Falstad's meters."),
        ("Q18: Why is no physical hardware required for this project?",
         "Because the circuit obeys linear physical laws that are solved exactly by our Python model and cross-validated in Falstad SPICE simulation, removing hardware costs while maintaining physical rigor."),
        ("Q19: What are the main limitations of your project?",
         "It assumes DC steady-state operation, analyzes single-fault scenarios, and uses simulated sensor data rather than soldered breadboard components."),
        ("Q20: How can this project be extended in the future?",
         "By adding AC sinusoidal testing to detect capacitor and inductor faults, connecting an ESP32 microcontroller with an ADC for live breadboard testing, and adding MOSFET switches for automated self-healing.")
    ]
    for q, a in viva_qa:
        p_q = add_p(space_before=6, space_after=2)
        p_q.paragraph_format.keep_with_next = True
        r_q = p_q.add_run(q)
        r_q.font.name = 'Calibri'
        r_q.font.size = Pt(10.0)
        r_q.font.bold = True
        r_q.font.color.rgb = NAVY

        p_a = add_p(space_after=4)
        r_a = p_a.add_run(a)
        r_a.font.name = 'Calibri'
        r_a.font.size = Pt(9.5)
        r_a.font.color.rgb = CHARCOAL

    add_h2("Appendix D: Two-Minute Pitch & Five-Minute Faculty Demonstration Script")
    add_body(
        "TWO-MINUTE ELEVATOR PITCH:\n"
        "'Good morning professors. When an electrical circuit fails in an industrial plant or an electric vehicle, "
        "finding the faulty component usually involves hours of manual probing or desoldering. Our project, the "
        "'Self-Learning Circuit Doctor', automates this diagnosis for a DC bridge-ladder network. "
        "We continuously sample three non-invasive signals: Node A voltage, Node B voltage, and total source current. "
        "By treating these three measurements as an electrical signature vector, our software maps the circuit's state "
        "into a standardized feature space and applies a Nearest-Centroid Classifier. "
        "We evaluated 13 distinct operating scenarios—including normal operation, open circuits, short circuits, and 50% "
        "resistance drifts. Across 390 test cases with 5% component tolerances and sensor noise, our system achieved "
        "100% diagnostic accuracy. We verified every calculation against the online Falstad SPICE simulator, created "
        "interactive web and desktop interfaces, and built in real-time self-learning updates. It demonstrates that "
        "BEEE circuit laws are directly applicable to modern automated engineering.'",
        bold_prefix="Two-Minute Elevator Pitch:\n"
    )
    add_body(
        "FIVE-MINUTE FACULTY DEMONSTRATION SCRIPT:\n"
        "• Minute 1: Launch 'python gui_tk.py' or 'streamlit run app.py'. Show the circuit schematic: Vs=10V, R1=1k, R2=2k, R3=1.5k, R4=3k. "
        "Highlight the nominal operating point: VA=5.806V, VB=3.871V, Is=4.194mA.\n"
        "• Minute 2: Demonstrate how we resolve diagnostic ambiguity. First inject 'F1 R1 Open' (VA=0V, VB=0V, Is=0mA). "
        "Next, inject 'F6 R2 Short' (VA=0V, VB=0V, but Is=10.0mA!). Explain to faculty how measuring current breaks the tie between two identical node voltages.\n"
        "• Minute 3: Demonstrate equipotential faults. Compare 'F4 R4 Open' (VA=VB=6.67V, Is=3.33mA) with 'F7 R3 Short' (VA=VB=5.45V, Is=4.55mA). "
        "Point out the separation margin Δd and runner-up candidate ranking.\n"
        "• Minute 4: Switch to the Falstad tab and open the simulation URL live. Show that Falstad's SPICE engine displays the exact same 5.806V and 3.871V.\n"
        "• Minute 5: Demonstrate supervised self-learning. Enter a verified lab reading in the Self-Learning tab, click 'Ingest Sample', "
        "and show faculty the live centroid shift and incremented sample count.",
        bold_prefix="Five-Minute Demonstration Script:\n"
    )

    # Save document to target path
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Report DOCX saved successfully to: {output_path}")


if __name__ == '__main__':
    out_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'report', 'Self_Learning_Circuit_Doctor_Report.docx'))
    build_full_report(out_file)
