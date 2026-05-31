from __future__ import annotations
from typing import List, Tuple, Dict, Optional
from calculations.transfer_matrix.tm_1d import expectation_value
from theory.clifford_ops import PauliString

Gate = Tuple[str, int, Optional[int]]


def build_defects(circuit: List[Gate]) -> Dict[int, int]:
    defects: Dict[int, int] = {}
    for gate in circuit:
        name = gate[0].upper()
        if name == "T":
            _, target, _ = gate
            defects[target] = (defects.get(target, 0) + 1) % 8
    return defects


def transform_observable_through_cliffords(observable: str, circuit: List[Gate]) -> PauliString:
    pauli = PauliString(observable)
    for gate in reversed(circuit):
        name = gate[0].upper()
        if name in {"H", "S"}:
            _, target, _ = gate
            pauli = pauli.conjugate_by(name, (target,))
        elif name == "CNOT":
            _, control, target = gate
            pauli = pauli.conjugate_by(name, (control, target))
    return pauli


def evaluate_expectation(n: int, circuit: List[Gate], observable: str) -> complex:
    if len(observable) != n:
        raise ValueError("Observable length must equal the number of qubits")
    defects = build_defects(circuit)
    return expectation_value(n, defects, observable, clifford_circuit=circuit)
