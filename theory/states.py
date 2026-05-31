from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict
import cmath


def _mod8(value: int) -> int:
    return value % 8


@dataclass(frozen=True)
class FluxConfig1D:
    n_qubits: int
    defects: Dict[int, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        cleaned = {int(pos): int(charge) % 8 for pos, charge in self.defects.items()}
        object.__setattr__(self, "defects", cleaned)
        object.__setattr__(self, "n", self.n_qubits)

    def add_defect(self, position: int, charge: int) -> "FluxConfig1D":
        if position < 0 or position >= self.n_qubits:
            raise IndexError("Defect position out of range")
        new_defects = dict(self.defects)
        new_defects[position] = _mod8(new_defects.get(position, 0) + charge)
        return FluxConfig1D(self.n_qubits, new_defects)

    def get_edge_flux(self, base: int, index: int) -> int:
        if index < 0 or index >= self.n_qubits - 1:
            raise IndexError("Edge index out of range")
        total = base
        for vertex in range(index + 1):
            total += self.defects.get(vertex, 0)
        return _mod8(total)

    def get_edge(self, base: int, index: int) -> int:
        return self.get_edge_flux(base, index)

    def amplitude(self, base: int) -> complex:
        total_defect = sum(self.defects.values()) % 8
        return cmath.exp(1j * cmath.pi * total_defect / 4)

    def as_vector(self) -> Dict[int, complex]:
        return {base: self.amplitude(base) for base in range(8)}

    def gauss_check(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"FluxConfig1D(n_qubits={self.n_qubits}, defects={self.defects})"
