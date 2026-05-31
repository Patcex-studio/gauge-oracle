from __future__ import annotations
from typing import Dict, List, Optional, Sequence, Tuple
import numpy as np
from theory.clifford_ops import PauliString
from theory.observables import observable_matrix

Gate = Tuple[str, int, Optional[int]]
MAX_FULL_TRANSFER_MATRIX_QUBITS = 4


def build_transfer_layer(tau: int) -> np.ndarray:
    tau_mod = tau % 8
    phase = np.exp(1j * np.pi * tau_mod / 4)
    layer = np.zeros((8, 8), dtype=complex)
    for q in range(8):
        layer[(q + tau_mod) % 8, q] = phase
    return layer


def _apply_clifford_circuit_to_observable(observable: str, clifford_circuit: Sequence[Gate]) -> PauliString:
    pauli = PauliString(observable)
    for gate in reversed(clifford_circuit):
        name = gate[0].upper()
        if name in {"H", "S"}:
            _, target, _ = gate
            pauli = pauli.conjugate_by(name, (target,))
        elif name == "CNOT":
            _, control, target = gate
            pauli = pauli.conjugate_by(name, (control, target))
    return pauli


def expectation_value(
    n: int,
    defects: Dict[int, int],
    observable: str,
    clifford_circuit: Optional[Sequence[Gate]] = None,
) -> complex:
    if len(observable) != n:
        raise ValueError("Observable length must equal n")

    phase = 1 + 0j
    if clifford_circuit:
        transformed = _apply_clifford_circuit_to_observable(observable, clifford_circuit)
        observable = transformed.string
        phase = transformed.phase

    initial_state = np.ones(8, dtype=complex) / np.sqrt(8)

    denominator_state = initial_state.copy()
    for vertex in range(n):
        denominator_state = build_transfer_layer(defects.get(vertex, 0)) @ denominator_state
    denominator = np.vdot(initial_state, denominator_state)
    if denominator == 0:
        return 0.0

    numerator_state = initial_state.copy()
    for vertex in range(n):
        numerator_state = build_transfer_layer(defects.get(vertex, 0)) @ numerator_state
        pauli = observable[vertex]
        if pauli != "I":
            numerator_state = observable_matrix(pauli) @ numerator_state

    return phase * np.vdot(initial_state, numerator_state) / denominator


def _single_transfer_layer(tau: int) -> np.ndarray:
    phase = np.exp(1j * np.pi * (tau % 8) / 4)
    layer = np.zeros((8, 8), dtype=complex)
    for q in range(8):
        layer[(q + tau) % 8, q] = phase
    return layer


def build_transfer_matrix_full(n_qubits: int, defects: Dict[int, int]) -> np.ndarray:
    if n_qubits <= 0:
        raise ValueError("n_qubits must be positive")
    if n_qubits > MAX_FULL_TRANSFER_MATRIX_QUBITS:
        raise ValueError(
            f"Full transfer matrix is too large for n_qubits={n_qubits}. Use sequential evaluation instead."
        )

    vertex_layers = [_single_transfer_layer(defects.get(vertex, 0)) for vertex in range(n_qubits)]
    full_matrix = vertex_layers[0]
    for layer in vertex_layers[1:]:
        full_matrix = np.kron(full_matrix, layer)
    return full_matrix


def observable_operator(pauli_string: str) -> List[np.ndarray]:
    return [_pauli_single_matrix(p) for p in pauli_string]


def _pauli_single_matrix(pauli: str) -> np.ndarray:
    pauli = pauli.upper()
    if pauli == "I":
        return np.eye(8, dtype=complex)
    if pauli == "Z":
        diag = [(-1) ** (q % 2) for q in range(8)]
        return np.diag(diag)
    if pauli == "X":
        matrix = np.zeros((8, 8), dtype=complex)
        for q in range(8):
            matrix[(q + 4) % 8, q] = 1.0
        return matrix
    if pauli == "Y":
        x = _pauli_single_matrix("X")
        z = _pauli_single_matrix("Z")
        return 1j * x @ z
    raise ValueError(f"Unsupported Pauli symbol: {pauli}")


def expectation_with_transfer_matrix(
    n_qubits: int,
    defects: Dict[int, int],
    observable: str,
    clifford_circuit: Optional[Sequence[Gate]] = None,
) -> complex:
    if len(observable) != n_qubits:
        raise ValueError("Observable length must equal n_qubits")

    phase = 1 + 0j
    if clifford_circuit:
        transformed = _apply_clifford_circuit_to_observable(observable, clifford_circuit)
        observable = transformed.string
        phase = transformed.phase

    initial_state = np.ones(8, dtype=complex) / np.sqrt(8)

    denominator_state = initial_state.copy()
    for vertex in range(n_qubits):
        denominator_state = _single_transfer_layer(defects.get(vertex, 0)) @ denominator_state
    denominator = np.vdot(initial_state, denominator_state)
    if denominator == 0:
        return 0.0

    numerator_state = initial_state.copy()
    for vertex, pauli in enumerate(observable):
        numerator_state = _single_transfer_layer(defects.get(vertex, 0)) @ numerator_state
        if pauli != "I":
            numerator_state = _pauli_single_matrix(pauli) @ numerator_state

    return phase * np.vdot(initial_state, numerator_state) / denominator
