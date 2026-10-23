"""
fault_scenarios.py - Comprehensive Catalog of DC Circuit Operating Conditions
Part of 'Self-Learning Circuit Doctor: Voltage-Signature-Based Fault Detection in DC Circuits'
BEEE Project for B.Tech

Defines 13 operating classes:
  1.  F0_NORMAL:    Normal operation
  2.  F1_R1_OPEN:   R1 open circuit (disconnected from positive supply)
  3.  F2_R2_OPEN:   R2 open circuit (resistor lifted from ground)
  4.  F3_R3_OPEN:   R3 open circuit (coupling between Node A and Node B severed)
  5.  F4_R4_OPEN:   R4 open circuit (Node B pull-down to ground broken)
  6.  F5_R1_SHORT:  R1 short circuit (Node A shorted directly to +Vs)
  7.  F6_R2_SHORT:  R2 short circuit (Node A clamped directly to Ground)
  8.  F7_R3_SHORT:  R3 short circuit (Node A and Node B joined as a single node)
  9.  F8_R4_SHORT:  R4 short circuit (Node B clamped directly to Ground)
  10. F9_R1_INC50:  R1 resistance increased by +50% (degraded contact / overheating)
  11. F10_R2_INC50: R2 resistance increased by +50% (component aging / crack)
  12. F11_R3_DEC50: R3 resistance decreased by -50% (partial internal breakdown)
  13. F12_R4_DEC50: R4 resistance decreased by -50% (partial breakdown / leakage)
"""

from typing import Dict, Any, List
import numpy as np
from src.circuit_model import (
    DCResistorNetwork, CircuitState,
    NUMERICAL_OPEN_RESISTANCE, NUMERICAL_SHORT_RESISTANCE
)


FAULT_CATALOG: Dict[str, Dict[str, Any]] = {
    'F0_NORMAL': {
        'code': 'F0',
        'name': 'Normal Operation',
        'r1_factor': 1.0, 'r2_factor': 1.0, 'r3_factor': 1.0, 'r4_factor': 1.0,
        'is_open': None, 'is_short': None,
        'description': (
            "All resistors operate within standard 5% manufacturing tolerances at nominal values "
            "(R1=1k, R2=2k, R3=1.5k, R4=3k, Vs=10V). Current flows nominally through both branches."
        ),
        'expected_va': 5.8065, 'expected_vb': 3.8710, 'expected_is': 4.1935
    },
    'F1_R1_OPEN': {
        'code': 'F1',
        'name': 'R1 Open Circuit',
        'r1_factor': None, 'r2_factor': 1.0, 'r3_factor': 1.0, 'r4_factor': 1.0,
        'is_open': 'R1', 'is_short': None,
        'description': (
            "R1 is severed (infinite impedance). The entire DC network is disconnected from the 10V supply rail. "
            "No current enters the circuit (Is = 0 mA) and all internal nodes discharge to 0V (VA = 0V, VB = 0V)."
        ),
        'expected_va': 0.0000, 'expected_vb': 0.0000, 'expected_is': 0.0000
    },
    'F2_R2_OPEN': {
        'code': 'F2',
        'name': 'R2 Open Circuit',
        'r1_factor': 1.0, 'r2_factor': None, 'r3_factor': 1.0, 'r4_factor': 1.0,
        'is_open': 'R2', 'is_short': None,
        'description': (
            "R2 is disconnected from ground. Node A loses its direct shunt to ground, forcing all source current "
            "exclusively into the R3-R4 series branch. Total loop resistance rises to 5.5 kOhm, dropping source current to 1.82 mA "
            "while Node A and B voltages rise significantly."
        ),
        'expected_va': 8.1818, 'expected_vb': 5.4545, 'expected_is': 1.8182
    },
    'F3_R3_OPEN': {
        'code': 'F3',
        'name': 'R3 Open Circuit',
        'r1_factor': 1.0, 'r2_factor': 1.0, 'r3_factor': None, 'r4_factor': 1.0,
        'is_open': 'R3', 'is_short': None,
        'description': (
            "R3 is broken between Node A and Node B. Node B is isolated from the input supply and pulled to 0V through R4. "
            "Node A acts as a simple two-resistor voltage divider formed by R1 and R2 (VA = 10 * 2/3 = 6.67V)."
        ),
        'expected_va': 6.6667, 'expected_vb': 0.0000, 'expected_is': 3.3333
    },
    'F4_R4_OPEN': {
        'code': 'F4',
        'name': 'R4 Open Circuit',
        'r1_factor': 1.0, 'r2_factor': 1.0, 'r3_factor': 1.0, 'r4_factor': None,
        'is_open': 'R4', 'is_short': None,
        'description': (
            "R4 is disconnected from ground. No current can flow through R3 because Node B has no return path to ground. "
            "Consequently, zero current flows through R3, resulting in zero voltage drop across R3. Node B floats up to equal VA (6.67V)."
        ),
        'expected_va': 6.6667, 'expected_vb': 6.6667, 'expected_is': 3.3333
    },
    'F5_R1_SHORT': {
        'code': 'F5',
        'name': 'R1 Short Circuit',
        'r1_factor': None, 'r2_factor': 1.0, 'r3_factor': 1.0, 'r4_factor': 1.0,
        'is_open': None, 'is_short': 'R1',
        'description': (
            "R1 is shorted (zero impedance). Node A is tied directly to the +10V supply rail (VA = 10.0V). "
            "Maximum load current is drawn by R2 and the R3-R4 branch, driving source current to 7.22 mA."
        ),
        'expected_va': 10.0000, 'expected_vb': 6.6667, 'expected_is': 7.2222
    },
    'F6_R2_SHORT': {
        'code': 'F6',
        'name': 'R2 Short Circuit',
        'r1_factor': 1.0, 'r2_factor': None, 'r3_factor': 1.0, 'r4_factor': 1.0,
        'is_open': None, 'is_short': 'R2',
        'description': (
            "R2 is shorted to ground, clamping Node A to 0V. Node B also drops to 0V. The full 10V supply drops across R1 (1 kOhm), "
            "causing a large fault current of exactly 10.0 mA. Notice this is cleanly distinguished from R1 Open by Is."
        ),
        'expected_va': 0.0000, 'expected_vb': 0.0000, 'expected_is': 10.0000
    },
    'F7_R3_SHORT': {
        'code': 'F7',
        'name': 'R3 Short Circuit',
        'r1_factor': 1.0, 'r2_factor': 1.0, 'r3_factor': None, 'r4_factor': 1.0,
        'is_open': None, 'is_short': 'R3',
        'description': (
            "R3 is shorted, joining Node A and Node B into an equipotential node (VA = VB = 5.45V). "
            "R2 (2k) and R4 (3k) are placed in direct parallel across Node A/B to ground, lowering equivalent resistance to 1.2 kOhm."
        ),
        'expected_va': 5.4545, 'expected_vb': 5.4545, 'expected_is': 4.5455
    },
    'F8_R4_SHORT': {
        'code': 'F8',
        'name': 'R4 Short Circuit',
        'r1_factor': 1.0, 'r2_factor': 1.0, 'r3_factor': 1.0, 'r4_factor': None,
        'is_open': None, 'is_short': 'R4',
        'description': (
            "R4 is shorted directly to ground, forcing VB = 0V. Node A is loaded by R2 in parallel with R3 alone (Req = 0.857 kOhm). "
            "Source current rises to 5.38 mA while Node A drops to 4.62V."
        ),
        'expected_va': 4.6154, 'expected_vb': 0.0000, 'expected_is': 5.3846
    },
    'F9_R1_INC50': {
        'code': 'F9',
        'name': 'R1 +50% (1.5k)',
        'r1_factor': 1.5, 'r2_factor': 1.0, 'r3_factor': 1.0, 'r4_factor': 1.0,
        'is_open': None, 'is_short': None,
        'description': (
            "R1 resistance drifts from 1.0 kOhm to 1.5 kOhm (+50%). Higher series source resistance increases the drop before Node A, "
            "lowering VA to 4.80V, VB to 3.20V, and total supply current to 3.47 mA."
        ),
        'expected_va': 4.8000, 'expected_vb': 3.2000, 'expected_is': 3.4667
    },
    'F10_R2_INC50': {
        'code': 'F10',
        'name': 'R2 +50% (3.0k)',
        'r1_factor': 1.0, 'r2_factor': 1.5, 'r3_factor': 1.0, 'r4_factor': 1.0,
        'is_open': None, 'is_short': None,
        'description': (
            "R2 resistance increases from 2.0 kOhm to 3.0 kOhm (+50%). Node A shunt impedance increases, allowing VA to rise "
            "to 6.43V and VB to 4.29V, while total source current decreases slightly to 3.57 mA."
        ),
        'expected_va': 6.4286, 'expected_vb': 4.2857, 'expected_is': 3.5714
    },
    'F11_R3_DEC50': {
        'code': 'F11',
        'name': 'R3 -50% (0.75k)',
        'r1_factor': 1.0, 'r2_factor': 1.0, 'r3_factor': 0.5, 'r4_factor': 1.0,
        'is_open': None, 'is_short': None,
        'description': (
            "R3 resistance drops from 1.5 kOhm to 750 Ohm (-50%). Stronger coupling between Node A and Node B raises VB towards VA "
            "(VB = 4.53V, VA = 5.66V) while drawing slightly more source current (4.34 mA)."
        ),
        'expected_va': 5.6604, 'expected_vb': 4.5283, 'expected_is': 4.3396
    },
    'F12_R4_DEC50': {
        'code': 'F12',
        'name': 'R4 -50% (1.5k)',
        'r1_factor': 1.0, 'r2_factor': 1.0, 'r3_factor': 1.0, 'r4_factor': 0.5,
        'is_open': None, 'is_short': None,
        'description': (
            "R4 resistance drops from 3.0 kOhm to 1.5 kOhm (-50%). Node B pull-down to ground becomes stronger, pulling VB down "
            "to 2.73V while Node A drops slightly to 5.45V and Is rises to 4.55 mA."
        ),
        'expected_va': 5.4545, 'expected_vb': 2.7273, 'expected_is': 4.5455
    }
}

# Ordered class labels for consistent index mapping
FAULT_CLASSES: List[str] = list(FAULT_CATALOG.keys())


def create_circuit_for_fault(fault_key: str,
                             Vs: float = 10.0,
                             base_r1: float = 1000.0,
                             base_r2: float = 2000.0,
                             base_r3: float = 1500.0,
                             base_r4: float = 3000.0) -> DCResistorNetwork:
    """
    Instantiates a DCResistorNetwork configured with the exact physical fault parameters.
    """
    if fault_key not in FAULT_CATALOG:
        raise KeyError(f"Unknown fault condition '{fault_key}'. Available: {FAULT_CLASSES}")

    info = FAULT_CATALOG[fault_key]
    
    # Calculate resistances
    r1 = base_r1 * info['r1_factor'] if info['r1_factor'] is not None else base_r1
    r2 = base_r2 * info['r2_factor'] if info['r2_factor'] is not None else base_r2
    r3 = base_r3 * info['r3_factor'] if info['r3_factor'] is not None else base_r3
    r4 = base_r4 * info['r4_factor'] if info['r4_factor'] is not None else base_r4

    # Apply open/short condition overrides
    if info['is_open'] == 'R1':
        r1 = NUMERICAL_OPEN_RESISTANCE
    elif info['is_open'] == 'R2':
        r2 = NUMERICAL_OPEN_RESISTANCE
    elif info['is_open'] == 'R3':
        r3 = NUMERICAL_OPEN_RESISTANCE
    elif info['is_open'] == 'R4':
        r4 = NUMERICAL_OPEN_RESISTANCE

    if info['is_short'] == 'R1':
        r1 = NUMERICAL_SHORT_RESISTANCE
    elif info['is_short'] == 'R2':
        r2 = NUMERICAL_SHORT_RESISTANCE
    elif info['is_short'] == 'R3':
        r3 = NUMERICAL_SHORT_RESISTANCE
    elif info['is_short'] == 'R4':
        r4 = NUMERICAL_SHORT_RESISTANCE

    return DCResistorNetwork(Vs=Vs, R1=r1, R2=r2, R3=r3, R4=r4)


def get_fault_summary_table() -> List[Dict[str, Any]]:
    """Returns a structured summary table of all 13 operating classes for reports and displays."""
    rows = []
    for k, v in FAULT_CATALOG.items():
        net = create_circuit_for_fault(k)
        state = net.solve()
        rows.append({
            'Code': v['code'],
            'Label': k,
            'Name': v['name'],
            'VA (V)': round(state.VA, 4),
            'VB (V)': round(state.VB, 4),
            'Is (mA)': round(state.Is, 4),
            'Req (Ω)': round(state.Req, 2) if not np.isinf(state.Req) else 'Open',
            'Description': v['description']
        })
    return rows


if __name__ == '__main__':
    print("=" * 80)
    print("ALL 13 DC FAULT SCENARIOS - REFERENCE SIGNATURE TABLE")
    print("=" * 80)
    for row in get_fault_summary_table():
        print(f"[{row['Code']:>2}] {row['Name']:<22} | VA: {row['VA (V)']:>6.3f} V | VB: {row['VB (V)']:>6.3f} V | Is: {row['Is (mA)']:>6.3f} mA | Req: {str(row['Req (Ω)']):>8}")
    print("=" * 80)
