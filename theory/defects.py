from .states import FluxConfig1D


def apply_t_gate(flux_config: FluxConfig1D, qubit: int) -> FluxConfig1D:
    defects = dict(flux_config.defects)
    defects[qubit] = (defects.get(qubit, 0) + 1) % 8
    return FluxConfig1D(flux_config.n_qubits, defects=defects)
