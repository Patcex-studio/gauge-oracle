import pytest
from theory.gauge_group import Z8Element, character
from theory.lattice import Lattice1D
from theory.states import FluxConfig1D
from theory.defects import apply_t_gate


def test_z8element_arithmetic():
    a = Z8Element(7)
    b = Z8Element(2)
    assert a + b == Z8Element(1)
    assert a.inverse() == Z8Element(1)
    assert a.phase().real == pytest.approx(0.7071067811865476)
    assert a.phase().imag == pytest.approx(-0.7071067811865476)


def test_character_matches_phase():
    result = character(Z8Element(1), Z8Element(2))
    assert result.real == pytest.approx(0.0)
    assert result.imag == pytest.approx(1.0)


def test_fluxconfig1d_defects():
    config = FluxConfig1D(4, {0: 1, 2: 2})
    assert config.get_edge(0, 0) == 1
    assert config.get_edge(0, 1) == 1
    assert config.get_edge(0, 2) == 3


def test_apply_t_gate_adds_defect():
    config = FluxConfig1D(3)
    new_config = apply_t_gate(config, 1)
    assert new_config.defects[1] == 1
    assert config.defects == {}


def test_fluxconfig1d_add_defect_mod8():
    config = FluxConfig1D(4)
    config2 = config.add_defect(0, 7).add_defect(0, 1)
    assert config2.defects[0] == 0


def test_fluxconfig1d_edge_flux_and_amplitude():
    config = FluxConfig1D(4, {0: 1, 2: 2})
    assert config.get_edge_flux(0, 0) == 1
    assert config.get_edge_flux(0, 1) == 1
    assert config.get_edge_flux(0, 2) == 3
    assert config.amplitude(0) == pytest.approx((-0.7071067811865475 + 0.7071067811865476j))


def test_lattice1d_shape():
    lattice = Lattice1D(5)
    assert len(lattice.vertices) == 5
    assert len(lattice.edges) == 4
    assert lattice.neighbors(0) == (1,)
    assert lattice.neighbors(2) == (1, 3)


def test_lattice2d_not_implemented():
    import pytest
    from theory.lattice import Lattice2D

    with pytest.raises(NotImplementedError):
        Lattice2D(3, 3)
