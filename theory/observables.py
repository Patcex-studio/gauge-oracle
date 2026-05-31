import numpy as np
from .states import FluxConfig1D


def measure_operator_on_config(flux_config: FluxConfig1D, pauli_string: str, base: int = 0) -> complex:
    if len(pauli_string) != flux_config.n:
        raise ValueError("Pauli string length must equal the number of qubits")
    value = 1 + 0j
    for index, symbol in enumerate(pauli_string.upper()):
        if symbol == "I":
            continue
        q = flux_config.get_edge(base, min(index, flux_config.n - 2)) if flux_config.n > 1 else 0
        if symbol == "Z":
            value *= (-1) ** (q % 2)
        elif symbol == "X":
            value *= 1 if q % 4 == 0 else -1
        elif symbol == "Y":
            value *= 1j * (-1) ** (q % 2)
    return value


def observable_matrix(pauli_string: str) -> np.ndarray:
    matrix = np.eye(8, dtype=complex)
    for i, symbol in enumerate(pauli_string.upper()):
        if symbol == "I":
            continue
        if symbol == "Z":
            diag = [(-1) ** (q % 2) for q in range(8)]
            matrix = np.diag(diag) @ matrix
        elif symbol == "X":
            op = np.zeros((8, 8), dtype=complex)
            for q in range(8):
                op[(q + 4) % 8, q] = 1.0
            matrix = op @ matrix
        elif symbol == "Y":
            x = np.zeros((8, 8), dtype=complex)
            for q in range(8):
                x[(q + 4) % 8, q] = 1.0
            z = np.diag([(-1) ** (q % 2) for q in range(8)])
            matrix = 1j * x @ z @ matrix
    return matrix
