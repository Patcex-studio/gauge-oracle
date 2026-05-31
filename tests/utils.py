import numpy as np
from theory.observables import observable_matrix
from calculations.transfer_matrix.tm_1d import build_transfer_layer


def exact_expectation(n: int, defects: dict[int, int], observable: str) -> complex:
    if len(observable) != n:
        raise ValueError("Observable length must equal the number of qubits")
    state = np.ones(8, dtype=complex) / np.sqrt(8)
    vector = state.copy()
    for vertex in range(n):
        tau = defects.get(vertex, 0) % 8
        layer = build_transfer_layer(tau)
        vector = layer @ vector
        if observable[vertex] != "I":
            vector = observable_matrix(observable[vertex]) @ vector

    denominator_state = state.copy()
    for vertex in range(n):
        tau = defects.get(vertex, 0) % 8
        layer = build_transfer_layer(tau)
        denominator_state = layer @ denominator_state

    denominator = np.vdot(state, denominator_state)
    return 0.0 if denominator == 0 else np.vdot(state, vector) / denominator
