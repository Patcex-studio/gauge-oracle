from pathlib import Path
import numpy as np
import pytest
from theory.gauge_group import Z8Element, character
from theory.lattice import Lattice1D
from theory.states import FluxConfig1D
from theory.observables import observable_matrix, measure_operator_on_config
from theory.clifford_ops import PauliString
from calculations.transfer_matrix.benchmark import run_benchmark
from calculations.transfer_matrix.tm_1d import (
    build_transfer_matrix_full,
    expectation_with_transfer_matrix,
    observable_operator,
)


def test_z8_subtraction_and_phase_character():
    a = Z8Element(3)
    b = Z8Element(5)
    assert a - b == Z8Element(6)
    assert a.phase() == pytest.approx(complex(-0.7071067811865475, 0.7071067811865476))
    assert character(Z8Element(1), Z8Element(2)) == pytest.approx(1j)


def test_pauli_string_s_cnot_conjugation():
    pauli = PauliString("XYI")
    result = pauli.conjugate_by("S", (0,))
    assert result.string[0] == "Y"
    result2 = PauliString("XZ").conjugate_by("CNOT", (0, 1))
    assert result2.string == "YY"


def test_z8_arithmetic_variants():
    a = Z8Element(3)
    assert a * 2 == Z8Element(5)
    assert a + 5 == Z8Element(0)
    assert a - 7 == Z8Element(4)
    assert (-a) == Z8Element(5)


def test_lattice1d_repr_and_neighbors():
    lattice = Lattice1D(4)
    assert repr(lattice) == "Lattice1D(n_qubits=4)"
    assert lattice.neighbors(1) == (0, 2)


def test_observable_matrix_y():
    y = observable_matrix("Y")
    assert y.shape == (8, 8)
    vec = np.zeros(8, dtype=complex)
    vec[0] = 1
    out = y @ vec
    assert out[4] == 1j


def test_transfer_matrix_full_diagonal_phase():
    full = build_transfer_matrix_full(1, {0: 1})
    assert full.shape == (8, 8)
    assert full[1, 0] != 0
    assert full[0, 0] == 0


def test_expectation_with_transfer_matrix_identity():
    n = 3
    defects = {}
    actual = expectation_with_transfer_matrix(n, defects, "III")
    assert actual == pytest.approx(1.0)


def test_measure_operator_on_config_zx():
    config = FluxConfig1D(3, {0: 1, 1: 2})
    value = measure_operator_on_config(config, "XIY")
    assert isinstance(value, complex)


def test_transfer_matrix_observable_operator_list():
    ops = observable_operator("XYZ")
    assert len(ops) == 3
    assert ops[0].shape == (8, 8)
    config = FluxConfig1D(3, {0: 1, 1: 2})
    assert config.get_edge(0, 0) == 1
    assert config.get_edge(0, 1) == 3
    vector = config.as_vector()
    assert len(vector) == 8
    assert vector[0] == config.amplitude(0)


def test_measure_operator_on_config():
    config = FluxConfig1D(3, {0: 1, 1: 2})
    value = measure_operator_on_config(config, "ZZI")
    assert value == 1


def test_observable_matrices():
    x = observable_matrix("X")
    z = observable_matrix("Z")
    y = observable_matrix("Y")
    vec = np.zeros(8, dtype=complex)
    vec[0] = 1
    assert x[4, 0] == 1
    assert z[1, 1] == -1
    assert np.allclose((y @ vec)[4], 1j)
    assert len(observable_operator("XZZ")) == 3


def test_build_transfer_matrix_full_and_expectation_with_clifford():
    n = 2
    defects = {0: 1, 1: 2}
    full = build_transfer_matrix_full(n, defects)
    assert full.shape == (64, 64)
    base = expectation_with_transfer_matrix(n, defects, "ZI")
    transformed = PauliString("ZI").conjugate_by("H", (0,))
    actual = expectation_with_transfer_matrix(n, defects, "ZI", clifford_circuit=[("H", 0, None)])
    assert actual == pytest.approx(expectation_with_transfer_matrix(n, defects, transformed.string))


def test_benchmark_writes_plot(tmp_path: Path):
    output = tmp_path / "benchmark.png"
    run_benchmark(str(output))
    assert output.exists()
