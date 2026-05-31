import random
import numpy as np
import pytest
from calculations.tm_1d import evaluate_expectation, build_defects, transform_observable_through_cliffords
from calculations.transfer_matrix.tm_1d import expectation_with_transfer_matrix
from theory.states import FluxConfig1D
from tests.utils import exact_expectation


def test_vacuum_expectation_matches_exact():
    n = 4
    circuit = []
    observable = "XXXX"
    defects = build_defects(circuit)
    expected = exact_expectation(n, defects, observable)
    actual = evaluate_expectation(n, circuit, observable)
    assert pytest.approx(actual, rel=1e-8, abs=1e-8) == expected


def test_single_t_defect():
    n = 4
    circuit = [("T", 2, None)]
    observable = "XXXX"
    expected = exact_expectation(n, build_defects(circuit), observable)
    actual = evaluate_expectation(n, circuit, observable)
    assert pytest.approx(actual, rel=1e-8, abs=1e-8) == expected


def test_clifford_transform_with_h():
    from calculations.tm_1d import transform_observable_through_cliffords

    n = 3
    circuit = [("H", 0, None)]
    observable = "ZZZ"
    transformed = transform_observable_through_cliffords(observable, circuit)
    expected = exact_expectation(n, build_defects(circuit), transformed.string)
    actual = evaluate_expectation(n, circuit, observable)
    assert pytest.approx(actual, rel=1e-8, abs=1e-8) == expected


def test_evaluate_expectation_with_cliffords_and_t():
    n = 3
    circuit = [("H", 0, None), ("CNOT", 0, 1), ("T", 1, None)]
    observable = "ZII"
    transformed = transform_observable_through_cliffords(observable, circuit)
    expected = exact_expectation(n, build_defects(circuit), transformed.string)
    actual = evaluate_expectation(n, circuit, observable)
    assert pytest.approx(actual, rel=1e-8, abs=1e-8) == expected


def test_expectation_with_clifford_circuit_support():
    n = 3
    circuit = [("H", 0, None), ("CNOT", 0, 2), ("T", 1, None)]
    observable = "ZIZ"
    defects = build_defects(circuit)
    actual = expectation_with_transfer_matrix(n, defects, observable, clifford_circuit=circuit)
    transformed = transform_observable_through_cliffords(observable, circuit)
    expected = expectation_with_transfer_matrix(n, defects, transformed.string)
    assert pytest.approx(actual, rel=1e-8, abs=1e-8) == expected


def test_three_t_defects():
    n = 5
    circuit = [("T", 0, None), ("T", 2, None), ("T", 4, None)]
    observable = "XXXXX"
    expected = exact_expectation(n, build_defects(circuit), observable)
    actual = evaluate_expectation(n, circuit, observable)
    assert pytest.approx(actual, rel=1e-8, abs=1e-8) == expected


def test_large_n_sequential_evaluation():
    n = 10
    circuit = [("T", 1, None), ("T", 5, None), ("T", 9, None)]
    observable = "X" * n
    expected = exact_expectation(n, build_defects(circuit), observable)
    actual = evaluate_expectation(n, circuit, observable)
    assert pytest.approx(actual, rel=1e-8, abs=1e-8) == expected


def test_expectation_value_matches_exact_small_n():
    from calculations.transfer_matrix.tm_1d import expectation_value

    for n in range(1, 7):
        circuit = [("T", i, None) for i in range(n)]
        observable = "X" * n
        defects = build_defects(circuit)
        exact = exact_expectation(n, defects, observable)
        actual = expectation_value(n, defects, observable)
        assert pytest.approx(actual, rel=1e-8, abs=1e-8) == exact


def test_t_defect_mod8_repeats():
    from theory.defects import apply_t_gate
    config = FluxConfig1D(3)
    for _ in range(8):
        config = apply_t_gate(config, 1)
    assert config.defects.get(0, 0) == 0


def test_linear_time_scaling():
    import time

    rng = random.Random(1234)
    sizes = [100, 200, 400, 800]
    medians = []
    for n in sizes:
        defect_positions = rng.sample(list(range(n)), max(1, n // 10))
        circuit = [("T", pos, None) for pos in defect_positions]
        observable = "X" * n
        runs = []
        for _ in range(3):
            start = time.perf_counter()
            evaluate_expectation(n, circuit, observable)
            runs.append(time.perf_counter() - start)
        medians.append(float(np.median(runs)))

    for previous, current in zip(medians, medians[1:]):
        ratio = current / previous
        assert ratio <= 2.5 * 1.05
