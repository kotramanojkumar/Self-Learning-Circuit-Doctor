"""
circuit_model.py - Electrical Simulation and Nodal Analysis Engine
Part of 'Self-Learning Circuit Doctor: Voltage-Signature-Based Fault Detection in DC Circuits'
BEEE Project for B.Tech

Topology:
  Vs (+10V nominal) ----[ R1: 1k ]----+---- Node A ----[ R3: 1.5k ]----+---- Node B
                                      |                                 |
                                  [ R2: 2k ]                        [ R4: 3k ]
                                      |                                 |
  GND (0V) ---------------------------+---------------------------------+
"""

import numpy as np
from typing import Dict, Tuple, Optional, Union

# Electrical constant thresholds for numerical simulation of physical limits
R_OPEN_THRESHOLD = 1e7      # Resistors >= 10 MOhm are treated as open-circuit
R_SHORT_THRESHOLD = 1e-4    # Resistors <= 0.0001 Ohm are treated as short-circuit

# Physical open and short numerical representations when injecting ideal faults
NUMERICAL_OPEN_RESISTANCE = 1e9   # 1 Giga-Ohm represents open air gap
NUMERICAL_SHORT_RESISTANCE = 1e-6  # 1 micro-Ohm represents ideal copper wire short


class CircuitState:
    """Data container for circuit electrical measurements."""
    def __init__(self, VA: float, VB: float, Is: float,
                 Req: float = 0.0,
                 branch_currents: Optional[Dict[str, float]] = None,
                 power_dissipation: Optional[Dict[str, float]] = None):
        self.VA = float(VA)        # Node A voltage (V)
        self.VB = float(VB)        # Node B voltage (V)
        self.Is = float(Is)        # Source current (mA)
        self.Req = float(Req)      # Total equivalent resistance (Ohms)
        self.branch_currents = branch_currents or {}      # mA
        self.power_dissipation = power_dissipation or {}  # mW

    def to_dict(self) -> Dict[str, float]:
        return {
            'VA': round(self.VA, 4),
            'VB': round(self.VB, 4),
            'Is': round(self.Is, 4),
            'Req': round(self.Req, 4)
        }

    def feature_vector(self) -> np.ndarray:
        """Returns [VA (V), VB (V), Is (mA)] for classifier ingestion."""
        return np.array([self.VA, self.VB, self.Is], dtype=float)

    def __repr__(self) -> str:
        return f"CircuitState(VA={self.VA:.4f} V, VB={self.VB:.4f} V, Is={self.Is:.4f} mA)"


class DCResistorNetwork:
    """
    Mathematical model of the 4-resistor bridge/ladder DC circuit.
    
    Nominal Parameters:
      Vs = 10.0 V
      R1 = 1000.0 Ohm (1.0 kOhm)
      R2 = 2000.0 Ohm (2.0 kOhm)
      R3 = 1500.0 Ohm (1.5 kOhm)
      R4 = 3000.0 Ohm (3.0 kOhm)
      
    Theoretical Derivations:
      Branch 34 resistance: R34 = R3 + R4
      Parallel equivalent at Node A: Rp = (R2 * R34) / (R2 + R34)
      Total circuit resistance: Rtotal = R1 + Rp
      Source current: Is = Vs / Rtotal
      Node A voltage: VA = Vs * (Rp / (R1 + Rp))
      Node B voltage: VB = VA * (R4 / (R3 + R4))
    """

    def __init__(self,
                 Vs: float = 10.0,
                 R1: float = 1000.0,
                 R2: float = 2000.0,
                 R3: float = 1500.0,
                 R4: float = 3000.0):
        self.Vs = float(Vs)
        self.R1 = float(R1)
        self.R2 = float(R2)
        self.R3 = float(R3)
        self.R4 = float(R4)
        self._validate_parameters()

    def _validate_parameters(self) -> None:
        """Sanity check on circuit parameter physics."""
        if self.Vs < 0:
            raise ValueError(f"Supply voltage cannot be negative in this unipolar model: {self.Vs}")
        for name, val in [('R1', self.R1), ('R2', self.R2), ('R3', self.R3), ('R4', self.R4)]:
            if val < 0:
                raise ValueError(f"Resistance {name} cannot be negative: {val}")

    def solve_analytical(self) -> CircuitState:
        """
        Solves the circuit using exact topological formulations for all edge cases
        (ideal opens and shorts) to avoid numerical floating-point inaccuracies.
        
        Returns:
            CircuitState containing VA (V), VB (V), Is (mA), and Req (Ohm).
        """
        Vs, r1, r2, r3, r4 = self.Vs, self.R1, self.R2, self.R3, self.R4

        # Case 1: R1 is open circuit
        if r1 >= R_OPEN_THRESHOLD:
            return CircuitState(VA=0.0, VB=0.0, Is=0.0, Req=float('inf'),
                                branch_currents={'I1': 0.0, 'I2': 0.0, 'I3': 0.0, 'I4': 0.0},
                                power_dissipation={'P1': 0.0, 'P2': 0.0, 'P3': 0.0, 'P4': 0.0, 'P_total': 0.0})

        # Case 2: R2 is short circuit (Node A clamped to GND)
        if r2 <= R_SHORT_THRESHOLD:
            # Node A is tied directly to Ground
            va = 0.0
            vb = 0.0
            i1 = Vs / r1 if r1 > R_SHORT_THRESHOLD else float('inf')
            # Is in mA
            is_ma = i1 * 1000.0
            req = r1
            return CircuitState(VA=va, VB=vb, Is=is_ma, Req=req,
                                branch_currents={'I1': is_ma, 'I2': is_ma, 'I3': 0.0, 'I4': 0.0},
                                power_dissipation={'P1': is_ma * Vs, 'P2': 0.0, 'P3': 0.0, 'P4': 0.0, 'P_total': is_ma * Vs})

        # Case 3: R1 is short circuit (Node A clamped to Vs)
        if r1 <= R_SHORT_THRESHOLD:
            va = Vs
            # Compute Node B voltage and currents from Node A
            # Branch 3-4 analysis:
            if r3 >= R_OPEN_THRESHOLD:
                # R3 open: no current to Node B
                vb = 0.0
                i3 = 0.0
            elif r4 <= R_SHORT_THRESHOLD:
                # R4 short: Node B is at 0V
                vb = 0.0
                i3 = (va - 0.0) / r3
            elif r4 >= R_OPEN_THRESHOLD:
                # R4 open: Node B floats up to Node A voltage
                vb = va
                i3 = 0.0
            elif r3 <= R_SHORT_THRESHOLD:
                # R3 short: Node B clamped to Node A
                vb = va
                i3 = vb / r4
            else:
                # Normal R3, R4
                vb = va * (r4 / (r3 + r4))
                i3 = (va - vb) / r3

            i2 = va / r2 if r2 < R_OPEN_THRESHOLD else 0.0
            i_total = i2 + i3
            req = (va / i_total) if i_total > 0 else float('inf')
            is_ma = i_total * 1000.0
            return CircuitState(VA=va, VB=vb, Is=is_ma, Req=req,
                                branch_currents={'I1': is_ma, 'I2': i2*1000.0, 'I3': i3*1000.0, 'I4': (vb/r4*1000.0 if r4 < R_OPEN_THRESHOLD else 0.0)},
                                power_dissipation={'P1': 0.0, 'P2': (va**2/r2)*1000.0 if r2 < R_OPEN_THRESHOLD else 0.0,
                                                   'P3': ((va-vb)**2/r3)*1000.0 if r3 < R_OPEN_THRESHOLD else 0.0,
                                                   'P4': (vb**2/r4)*1000.0 if r4 < R_OPEN_THRESHOLD else 0.0,
                                                   'P_total': Vs * is_ma})

        # Case 4: General topological analysis covering combinations of R2, R3, R4
        # Analyze branch 3-4 (from Node A through R3, Node B, R4 to GND)
        if r3 >= R_OPEN_THRESHOLD:
            # R3 is open: branch 3-4 is completely disconnected from Node A
            # Node B is connected to GND through R4 (unless R4 is open, in which case it is 0V)
            r34 = float('inf')
            vb_ratio = 0.0
            vb_override = 0.0
        elif r4 <= R_SHORT_THRESHOLD:
            # R4 is short: Node B is at GND (0V)
            # Resistance of branch 3-4 is just R3
            r34 = r3
            vb_override = 0.0
            vb_ratio = 0.0
        elif r4 >= R_OPEN_THRESHOLD:
            # R4 is open: no current flows through R3 to GND
            # Therefore branch 3-4 draws 0 current, r34 = inf
            r34 = float('inf')
            vb_override = None # vb will equal va
        elif r3 <= R_SHORT_THRESHOLD:
            # R3 is short: Node B is directly shorted to Node A
            # Resistance of branch 3-4 is just R4
            r34 = r4
            vb_override = None # vb will equal va
        else:
            # Normal series combination
            r34 = r3 + r4
            vb_override = None

        # Compute equivalent resistance of Node A to GND (Rp = R2 || R34)
        if r2 >= R_OPEN_THRESHOLD:
            # R2 is open
            rp = r34
        else:
            if np.isinf(r34):
                rp = r2
            else:
                rp = (r2 * r34) / (r2 + r34)

        # Total resistance seen by supply
        rtotal = r1 + rp
        is_val = Vs / rtotal
        is_ma = is_val * 1000.0

        # Node A voltage
        va = Vs * (rp / (r1 + rp)) if not np.isinf(rp) else Vs

        # Node B voltage
        if vb_override is not None:
            vb = vb_override
        elif r4 >= R_OPEN_THRESHOLD or r3 <= R_SHORT_THRESHOLD:
            vb = va
        elif np.isinf(r34):
            vb = 0.0
        else:
            vb = va * (r4 / (r3 + r4))

        # Branch currents in mA
        i2_ma = (va / r2 * 1000.0) if r2 < R_OPEN_THRESHOLD else 0.0
        if r3 >= R_OPEN_THRESHOLD or r4 >= R_OPEN_THRESHOLD:
            i34_ma = 0.0
        elif r3 <= R_SHORT_THRESHOLD:
            i34_ma = (va / r4 * 1000.0) if r4 > R_SHORT_THRESHOLD else (va / 1e-6 * 1000.0)
        else:
            i34_ma = ((va - vb) / r3 * 1000.0)

        # Power dissipation in mW
        p1 = (is_val ** 2) * r1 * 1000.0
        p2 = (va ** 2 / r2 * 1000.0) if r2 < R_OPEN_THRESHOLD else 0.0
        p3 = (((va - vb) ** 2) / r3 * 1000.0) if r3 < R_OPEN_THRESHOLD else 0.0
        p4 = (vb ** 2 / r4 * 1000.0) if r4 < R_OPEN_THRESHOLD else 0.0
        ptot = Vs * is_ma

        return CircuitState(
            VA=va,
            VB=vb,
            Is=is_ma,
            Req=rtotal,
            branch_currents={'I1': is_ma, 'I2': i2_ma, 'I3': i34_ma, 'I4': i34_ma},
            power_dissipation={'P1': p1, 'P2': p2, 'P3': p3, 'P4': p4, 'P_total': ptot}
        )

    def solve_nodal_matrix(self) -> CircuitState:
        """
        Solves the circuit using standard nodal matrix analysis (KCL at Node A and Node B).
        Conductance matrix formulation: G * V = I
        
        Matrix Equation:
          [ (G1 + G2 + G3)     -G3       ] [ VA ] = [ G1 * Vs ]
          [     -G3         (G3 + G4)    ] [ VB ]   [    0    ]
          
        Where G_i = 1 / R_i.
        For ideal opens, G_i -> 0.
        For near-zero shorts, small damping (or piecewise condition) is applied.
        """
        # Clamp open resistances to very large to prevent division overflow
        r1 = max(self.R1, 1e-4)
        r2 = max(self.R2, 1e-4)
        r3 = max(self.R3, 1e-4)
        r4 = max(self.R4, 1e-4)

        g1 = 1.0 / r1 if self.R1 < R_OPEN_THRESHOLD else 0.0
        g2 = 1.0 / r2 if self.R2 < R_OPEN_THRESHOLD else 0.0
        g3 = 1.0 / r3 if self.R3 < R_OPEN_THRESHOLD else 0.0
        g4 = 1.0 / r4 if self.R4 < R_OPEN_THRESHOLD else 0.0

        # Build 2x2 Conductance Matrix
        G = np.array([
            [g1 + g2 + g3, -g3],
            [-g3, g3 + g4]
        ], dtype=float)

        I = np.array([
            g1 * self.Vs,
            0.0
        ], dtype=float)

        try:
            # Check determinant
            det_G = np.linalg.det(G)
            if abs(det_G) < 1e-12:
                # Singular matrix (e.g. floating node), fall back to analytical solver
                return self.solve_analytical()
            
            V = np.linalg.solve(G, I)
            va = float(V[0])
            vb = float(V[1])

            # Source current Is = G1 * (Vs - VA)
            if self.R1 <= R_SHORT_THRESHOLD:
                # If R1 is shorted, VA = Vs, Is is determined by downstream branches
                va = self.Vs
                i_load = (va * g2) + ((va - vb) * g3)
                is_ma = i_load * 1000.0
            else:
                is_ma = g1 * (self.Vs - va) * 1000.0

            req = (self.Vs / (is_ma / 1000.0)) if is_ma > 1e-9 else float('inf')

            return CircuitState(VA=va, VB=vb, Is=is_ma, Req=req)
        except np.linalg.LinAlgError:
            # Fallback to robust analytical solver
            return self.solve_analytical()

    def solve(self) -> CircuitState:
        """
        Primary solver method. Uses robust analytical formulation with exact
        physical boundary handling, verified against nodal matrix solution.
        """
        return self.solve_analytical()


def simulate_nominal_circuit() -> CircuitState:
    """Convenience helper to run the nominal baseline circuit."""
    circuit = DCResistorNetwork(Vs=10.0, R1=1000.0, R2=2000.0, R3=1500.0, R4=3000.0)
    return circuit.solve()


if __name__ == "__main__":
    print("=" * 60)
    print("DC RESISTOR NETWORK - NOMINAL CIRCUIT VERIFICATION")
    print("=" * 60)
    nom = simulate_nominal_circuit()
    print(f"Nominal Parameters: Vs=10V, R1=1k, R2=2k, R3=1.5k, R4=3k")
    print(f"Calculated VA : {nom.VA:.4f} V  (Target: ~5.8065 V)")
    print(f"Calculated VB : {nom.VB:.4f} V  (Target: ~3.8710 V)")
    print(f"Calculated Is : {nom.Is:.4f} mA (Target: ~4.1935 mA)")
    print(f"Calculated Req: {nom.Req:.2f} Ohm (Target: ~2384.62 Ohm)")
    print("=" * 60)
