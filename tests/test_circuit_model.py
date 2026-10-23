"""
test_circuit_model.py - Unit Tests for DC Resistor Network Solver and Fault Scenarios
Part of 'Self-Learning Circuit Doctor: Voltage-Signature-Based Fault Detection in DC Circuits'
"""

import sys
import os
import pytest
import numpy as np

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.circuit_model import (
    DCResistorNetwork, simulate_nominal_circuit,
    NUMERICAL_OPEN_RESISTANCE, NUMERICAL_SHORT_RESISTANCE
)
from src.fault_scenarios import create_circuit_for_fault, FAULT_CATALOG, FAULT_CLASSES


class TestNominalCircuit:
    """Tests for nominal circuit operating conditions (Vs=10V, R1=1k, R2=2k, R3=1.5k, R4=3k)."""

    def test_nominal_exact_theoretical_values(self):
        """Verifies calculated values match theoretical derivations to 3 decimal places."""
        circuit = DCResistorNetwork(Vs=10.0, R1=1000.0, R2=2000.0, R3=1500.0, R4=3000.0)
        state = circuit.solve()

        # Expected:
        # VA = 180 / 31 ~ 5.80645 V
        # VB = 120 / 31 ~ 3.87097 V
        # Is = 130 / 31 ~ 4.19355 mA
        # Req = 31 / 13 kOhm ~ 2384.62 Ohm
        assert state.VA == pytest.approx(180.0 / 31.0, rel=1e-4)
        assert state.VB == pytest.approx(120.0 / 31.0, rel=1e-4)
        assert state.Is == pytest.approx(130.0 / 31.0, rel=1e-4)
        assert state.Req == pytest.approx(31000.0 / 13.0, rel=1e-4)

    def test_matrix_nodal_solver_matches_analytical(self):
        """Cross-checks nodal matrix conductance solver against topological analytical solver."""
        circuit = DCResistorNetwork(Vs=10.0, R1=1000.0, R2=2000.0, R3=1500.0, R4=3000.0)
        sol_analytical = circuit.solve_analytical()
        sol_nodal = circuit.solve_nodal_matrix()

        assert sol_nodal.VA == pytest.approx(sol_analytical.VA, rel=1e-3)
        assert sol_nodal.VB == pytest.approx(sol_analytical.VB, rel=1e-3)
        assert sol_nodal.Is == pytest.approx(sol_analytical.Is, rel=1e-3)

    def test_conservation_of_power(self):
        """Tellegen's Theorem / Energy Conservation: P_source = P_R1 + P_R2 + P_R3 + P_R4."""
        circuit = DCResistorNetwork(Vs=10.0, R1=1000.0, R2=2000.0, R3=1500.0, R4=3000.0)
        state = circuit.solve()
        p = state.power_dissipation

        sum_dissipated = p['P1'] + p['P2'] + p['P3'] + p['P4']
        p_supplied = p['P_total']
        assert sum_dissipated == pytest.approx(p_supplied, rel=1e-4)

    def test_negative_resistance_validation(self):
        """Checks that unphysical negative resistances trigger ValueError."""
        with pytest.raises(ValueError):
            DCResistorNetwork(Vs=10.0, R1=-100.0, R2=2000.0, R3=1500.0, R4=3000.0)

    def test_variable_supply_scaling(self):
        """Verifies linearity of the DC circuit with respect to supply voltage."""
        c10 = DCResistorNetwork(Vs=10.0).solve()
        c20 = DCResistorNetwork(Vs=20.0).solve()

        assert c20.VA == pytest.approx(2.0 * c10.VA, rel=1e-4)
        assert c20.VB == pytest.approx(2.0 * c10.VB, rel=1e-4)
        assert c20.Is == pytest.approx(2.0 * c10.Is, rel=1e-4)


class TestFaultScenarios:
    """Verifies all 13 operating classes match theoretical physics."""

    def test_r1_open_disconnects_circuit(self):
        net = create_circuit_for_fault('F1_R1_OPEN')
        state = net.solve()
        assert state.VA == 0.0
        assert state.VB == 0.0
        assert state.Is == 0.0

    def test_r2_open_raises_voltages(self):
        net = create_circuit_for_fault('F2_R2_OPEN')
        state = net.solve()
        assert state.VA == pytest.approx(90.0 / 11.0, rel=1e-3)
        assert state.VB == pytest.approx(60.0 / 11.0, rel=1e-3)
        assert state.Is == pytest.approx(20.0 / 11.0, rel=1e-3)

    def test_r3_open_isolates_node_b(self):
        net = create_circuit_for_fault('F3_R3_OPEN')
        state = net.solve()
        assert state.VA == pytest.approx(20.0 / 3.0, rel=1e-3)
        assert state.VB == 0.0
        assert state.Is == pytest.approx(10.0 / 3.0, rel=1e-3)

    def test_r4_open_floats_node_b(self):
        net = create_circuit_for_fault('F4_R4_OPEN')
        state = net.solve()
        assert state.VA == pytest.approx(20.0 / 3.0, rel=1e-3)
        assert state.VB == pytest.approx(state.VA, rel=1e-3)
        assert state.Is == pytest.approx(10.0 / 3.0, rel=1e-3)

    def test_r1_short_clamps_node_a_to_vs(self):
        net = create_circuit_for_fault('F5_R1_SHORT')
        state = net.solve()
        assert state.VA == 10.0
        assert state.VB == pytest.approx(20.0 / 3.0, rel=1e-3)
        assert state.Is == pytest.approx(65.0 / 9.0, rel=1e-3)

    def test_r2_short_clamps_node_a_to_gnd(self):
        net = create_circuit_for_fault('F6_R2_SHORT')
        state = net.solve()
        assert state.VA == 0.0
        assert state.VB == 0.0
        assert state.Is == 10.0

    def test_r3_short_equipotential_nodes(self):
        net = create_circuit_for_fault('F7_R3_SHORT')
        state = net.solve()
        assert state.VA == pytest.approx(60.0 / 11.0, rel=1e-3)
        assert state.VB == pytest.approx(state.VA, rel=1e-3)
        assert state.Is == pytest.approx(50.0 / 11.0, rel=1e-3)

    def test_r4_short_clamps_node_b_to_gnd(self):
        net = create_circuit_for_fault('F8_R4_SHORT')
        state = net.solve()
        assert state.VA == pytest.approx(60.0 / 13.0, rel=1e-3)
        assert state.VB == 0.0
        assert state.Is == pytest.approx(70.0 / 13.0, rel=1e-3)

    def test_all_13_classes_have_catalog_entries(self):
        assert len(FAULT_CLASSES) == 13
        for k in FAULT_CLASSES:
            assert k in FAULT_CATALOG
            net = create_circuit_for_fault(k)
            st = net.solve()
            assert st.VA >= 0.0
            assert st.VB >= 0.0
            assert st.Is >= 0.0


if __name__ == '__main__':
    pytest.main(['-v', __file__])
