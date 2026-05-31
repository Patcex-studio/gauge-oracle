from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Lattice1D:
    n_qubits: int
    vertices: Tuple[int, ...]
    edges: Tuple[Tuple[int, int], ...]

    def __init__(self, n_qubits: int):
        object.__setattr__(self, "n_qubits", n_qubits)
        object.__setattr__(self, "vertices", tuple(range(n_qubits)))
        object.__setattr__(self, "edges", tuple((i, i + 1) for i in range(max(0, n_qubits - 1))))

    def neighbors(self, vertex: int) -> Tuple[int, ...]:
        if vertex < 0 or vertex >= self.n_qubits:
            raise IndexError("Vertex out of range")
        nbrs = []
        if vertex > 0:
            nbrs.append(vertex - 1)
        if vertex + 1 < self.n_qubits:
            nbrs.append(vertex + 1)
        return tuple(nbrs)

    def __repr__(self) -> str:
        return f"Lattice1D(n_qubits={self.n_qubits})"


@dataclass(frozen=True)
class Lattice2D:
    Lx: int
    Ly: int

    def __init__(self, Lx: int, Ly: int):
        raise NotImplementedError("Only 1D is implemented in code")

    def __repr__(self) -> str:
        return "Lattice2D(NotImplemented)"
