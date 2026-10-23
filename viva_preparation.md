# Self-Learning Circuit Doctor: Viva Voce & Demonstration Guide
**B.Tech BEEE Project Preparation Document**

**Institution:** Vellore Institute of Technology (VIT), Vellore  
**Team Members:**  
- **KOTRA MANOJ KUMAR** (Reg. No: `23BCE2113`) — B.Tech CSE (SCOPE)  
- **Mayank Yadav** (Reg. No: `23BCE0119`) — B.Tech CSE (SCOPE)  
**Project Guide:** Prof. POOMPAVAI T, School of Electrical Engineering (SELECT)  
**Academic Session:** 2026–2027

---

## Part 1: Two-Minute Elevator Pitch

> *"Good morning respected professors. When an electrical circuit malfunctions in an industrial plant, automotive ECU, or renewable power converter, technicians traditionally spend hours manually probing test points or desoldering components. Our project, the **'Self-Learning Circuit Doctor'**, automates this entire diagnostic process.*
>
> *Using a four-resistor DC bridge/ladder network ($V_s = 10\text{ V}$, $R_1 = 1\text{ k}\Omega$, $R_2 = 2\text{ k}\Omega$, $R_3 = 1.5\text{ k}\Omega$, $R_4 = 3\text{ k}\Omega$), we continuously monitor three non-invasive electrical signals: Node A voltage ($V_A$), Node B voltage ($V_B$), and total supply current ($I_s$). By treating these three measurements as an electrical 'signature vector', our Python software maps the circuit's state into a standardized feature space and applies a Standardized Nearest-Centroid Classifier.*
>
> *We evaluated 13 distinct operating scenarios—including normal operation, catastrophic open circuits, short circuits, and 50% resistance drifts. Across 390 held-out test cases with 5% component tolerances and sensor measurement noise, our system achieved **100.00% diagnostic accuracy** with zero false classifications.*
>
> *Furthermore, our model is cross-validated against the online Falstad SPICE simulator, requires zero physical hardware, and features an interactive graphical interface with real-time supervised self-learning updates. It proves that BEEE circuit laws are the direct foundation of modern automated engineering. Thank you."*

---

## Part 2: Five-Minute Live Project Demonstration Script

| Time | Action | Screen / Script | Key Faculty Takeaway |
| :--- | :--- | :--- | :--- |
| **0:00 – 1:00** | **System Launch & Baseline** | Run `python gui_tk.py` (or `streamlit run app.py`). Point to the circuit schematic and nominal baseline: $V_A = 5.806\text{ V}$, $V_B = 3.871\text{ V}$, $I_s = 4.194\text{ mA}$. | Shows understanding of KCL/KVL derivations and theoretical baseline. |
| **1:00 – 2:00** | **Resolving Ambiguities ($R_1$ Open vs $R_2$ Short)** | In the GUI, inject `F1_R1_OPEN`. Show that $V_A=0\text{ V}, V_B=0\text{ V}, I_s=0\text{ mA}$. Next, inject `F6_R2_SHORT`. Show that $V_A=0\text{ V}, V_B=0\text{ V}$, but $I_s=10.0\text{ mA}$! | Explains why measuring source current $I_s$ is essential—voltage alone cannot separate these two faults. |
| **2:00 – 3:00** | **Equipotential Faults ($R_4$ Open vs $R_3$ Short)** | Inject `F4_R4_OPEN` ($V_A = V_B = 6.67\text{ V}, I_s = 3.33\text{ mA}$). Next, inject `F7_R3_SHORT` ($V_A = V_B = 5.45\text{ V}, I_s = 4.55\text{ mA}$). | Demonstrates that even when $V_A = V_B$, the absolute voltage and current levels distinguish the faults cleanly. |
| **3:00 – 4:00** | **Falstad SPICE Simulation Cross-Check** | Switch to the Falstad tab. Click the 1-click web URL to open the simulator live in browser. Show faculty the interactive current animations and voltmeter probes showing $5.806\text{ V}$ and $3.871\text{ V}$. | Proves model is validated against genuine SPICE numerical simulation, not fabricated numbers. |
| **4:00 – 5:00** | **Supervised Self-Learning Ingestion** | Open the Self-Learning tab. Submit a newly verified laboratory reading (e.g., $V_A = 5.82\text{ V}, V_B = 3.88\text{ V}, I_s = 4.20\text{ mA}$ for Normal). Click **Ingest Sample**. Show the live centroid shift and sample count increment. | Explains the true engineering meaning of self-learning (supervised online adaptation). |

---

## Part 3: Top 20 Comprehensive Viva Questions and Answers

### Q1: What problem does this project solve?
**Answer:** It automates the detection, diagnosis, and localization of component faults (open circuits, short circuits, and resistance degradation) in DC resistor networks by analyzing external voltage and current signatures without requiring technicians to manually desolder or probe every component.

### Q2: Why was a DC resistor network selected for this study?
**Answer:** The DC resistor network serves as the foundational benchmark in Basic Electrical & Electronics Engineering (BEEE). It allows direct, rigorous mathematical verification using Kirchhoff's laws and nodal analysis before extending the methodology to reactive AC systems.

### Q3: What is meant by an electrical "voltage signature"?
**Answer:** An electrical voltage signature is a characteristic multi-variable vector—in our project $[V_A, V_B, I_s]$—whose coordinates uniquely map to a specific physical operating condition of the circuit.

### Q4: How is an open circuit physically and numerically modeled?
**Answer:** Physically, an open circuit represents a broken connection or infinite air-gap resistance ($R \to \infty$) with zero branch current ($I = 0$). Numerically, to avoid zero-division in conductance matrices, it is modeled either through topological branch removal or by setting $R = 1\text{ G}\Omega$ ($10^9\ \Omega$).

### Q5: How is a short circuit physically and numerically modeled?
**Answer:** Physically, a short circuit represents a zero-resistance metallic bridge ($R \to 0$) causing zero voltage drop ($\Delta V = 0$). Numerically, it is modeled either by merging the shorted nodes into an equipotential node or by using a contact resistance of $1\ \mu\Omega$ ($10^{-6}\ \Omega$).

### Q6: State Kirchhoff's Current Law (KCL) and write the KCL equation at Node A.
**Answer:** KCL states that the algebraic sum of currents entering or leaving an electrical node must equal zero. At Node A:
$$\frac{V_A - V_s}{R_1} + \frac{V_A}{R_2} + \frac{V_A - V_B}{R_3} = 0$$

### Q7: What are the exact theoretical nominal values for the project circuit?
**Answer:** For $V_s = 10\text{ V}$, $R_1 = 1\text{ k}\Omega$, $R_2 = 2\text{ k}\Omega$, $R_3 = 1.5\text{ k}\Omega$, and $R_4 = 3\text{ k}\Omega$:
- Equivalent parallel resistance: $R_p = R_2 \parallel (R_3 + R_4) = 2 \parallel 4.5 = \frac{18}{13}\text{ k}\Omega \approx 1.385\text{ k}\Omega$
- Total circuit resistance: $R_{total} = R_1 + R_p = 1 + \frac{18}{13} = \frac{31}{13}\text{ k}\Omega \approx 2.385\text{ k}\Omega$
- Source current: $I_s = \frac{V_s}{R_{total}} = \frac{130}{31}\text{ mA} \approx \mathbf{4.194\text{ mA}}$
- Node A voltage: $V_A = V_s \frac{R_p}{R_1 + R_p} = \frac{180}{31}\text{ V} \approx \mathbf{5.806\text{ V}}$
- Node B voltage: $V_B = V_A \left(\frac{R_4}{R_3 + R_4}\right) = \frac{120}{31}\text{ V} \approx \mathbf{3.871\text{ V}}$

### Q8: Why is measuring source current $I_s$ essential? Could we diagnose faults using only voltages?
**Answer:** No, measuring voltages alone creates critical diagnostic ambiguities. For instance, both $R_1$ Open and $R_2$ Short produce $V_A = 0\text{ V}$ and $V_B = 0\text{ V}$. Measuring source current resolves this: $I_s = 0\text{ mA}$ for $R_1$ Open (circuit disconnected), whereas $I_s = 10.0\text{ mA}$ for $R_2$ Short (full 10V drops across $R_1$).

### Q9: What is a Nearest-Centroid Classifier and how does it work?
**Answer:** A Nearest-Centroid Classifier is a supervised machine learning model. During training, it computes the mean feature vector (centroid) for each class in standardized space:
$$\mathbf{C}_c = \frac{1}{N_c} \sum_{i \in c} \mathbf{Z}_i$$
During testing, an unknown sample $\mathbf{z}$ is assigned to the class with the smallest Euclidean distance:
$$\hat{y} = \arg\min_c \|\mathbf{z} - \mathbf{C}_c\|_2$$

### Q10: What is feature standardization and why is it mandatory here?
**Answer:** Feature standardization transforms each feature to have zero mean and unit variance ($z = (x - \mu)/\sigma$). It is mandatory because voltages ($0\text{ to }10\text{ V}$) and currents ($0\text{ to }10\text{ mA}$) represent different physical units; without standardization, Euclidean distances would be skewed by whichever feature has a wider numerical range.

### Q11: What is data leakage and how did your pipeline prevent it?
**Answer:** Data leakage occurs when test data inadvertently influences model training or parameter estimation. We strictly avoided it by computing standardization statistics ($\mu, \sigma$) and class centroids solely from the training partition ($N=1560$), keeping the held-out test partition ($N=390$) completely isolated until final evaluation.

### Q12: What is a confusion matrix?
**Answer:** A confusion matrix is an $N \times N$ table where rows represent true physical classes and columns represent predicted classes. A perfect classifier produces a strictly diagonal matrix, where off-diagonal entries (false positives and false negatives) are all zero.

### Q13: What accuracy did your classifier achieve on held-out test data?
**Answer:** The Standardized Nearest-Centroid Classifier achieved **100.00% accuracy** (390 out of 390 test samples classified correctly) under standard 5% component manufacturing tolerances and sensor noise.

### Q14: How does component manufacturing tolerance affect predictions?
**Answer:** Real-world resistors vary within tolerance bands (e.g. $\pm 5\%$). This causes measured signatures to form clouds or clusters around nominal points. As long as the clusters do not overlap, nearest-centroid classification cleanly separates them. In our tolerance sensitivity study, accuracy remained above 98% even at 10% tolerance.

### Q15: What is the "separation margin" and what does it indicate?
**Answer:** The separation margin is $\Delta d = d_{second} - d_{nearest}$. If $\Delta d$ is large, the prediction is robust. If $\Delta d < 0.35$ standardized units, the measurement is near a decision boundary, and the Circuit Doctor flags a cautionary warning of diagnostic uncertainty.

### Q16: What does "Self-Learning" mean in your project?
**Answer:** It refers to supervised incremental online learning. When a technician submits a newly verified laboratory measurement, the system updates the class centroid in real time using a streaming average formula ($O(1)$ complexity) without retraining from scratch:
$$\mathbf{C}_{c, new} = \mathbf{C}_{c, old} + \frac{1}{N_{c, new}} (\mathbf{z}_{new} - \mathbf{C}_{c, old})$$

### Q17: What is Falstad Circuit Simulator and how did you use it?
**Answer:** Falstad is a web-based electronic circuit simulator that uses Modified Nodal Analysis (MNA), the same mathematical formulation as SPICE. We built our circuit in Falstad, confirmed nominal readings ($5.806\text{ V}, 3.871\text{ V}, 4.194\text{ mA}$), simulated representative fault scenarios, and generated clickable URLs for live faculty testing.

### Q18: Why is no physical hardware required for this project?
**Answer:** Because the circuit's behavior is governed by deterministic linear laws that are fully solved by our Python mathematical engine and verified against Falstad's SPICE engine. This eliminates hardware parts cost while maintaining complete physical and academic rigor.

### Q19: What are the main limitations of your project?
**Answer:** 
1. It is restricted to steady-state DC resistive networks (dynamic reactive elements $L$ and $C$ are not modeled).
2. It assumes single-component failure modes rather than simultaneous multiple faults.
3. It relies on simulation-generated stochastic data rather than soldered breadboard sensors.

### Q20: What future improvements are planned?
**Answer:** 
1. Expanding to AC circuits using phasor signatures ($[|V|, \angle\theta, |I|]$) to detect capacitor and inductor degradation.
2. Interfacing with an ESP32 microcontroller and ADS1115 16-bit ADCs for portable hardware breadboard testing.
3. Integrating solid-state MOSFET switches for automated self-healing circuit reconfiguration.
