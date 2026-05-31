import cmath
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Z8Element:
    value: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", int(self.value) % 8)

    def __add__(self, other: Union["Z8Element", int]) -> "Z8Element":
        if isinstance(other, Z8Element):
            return Z8Element(self.value + other.value)
        return Z8Element(self.value + int(other))

    def __sub__(self, other: Union["Z8Element", int]) -> "Z8Element":
        if isinstance(other, Z8Element):
            return Z8Element(self.value - other.value)
        return Z8Element(self.value - int(other))

    def __mul__(self, other: Union["Z8Element", int]) -> "Z8Element":
        # In additive representation multiplication corresponds to addition.
        return self.__add__(other)

    def __neg__(self) -> "Z8Element":
        return Z8Element(-self.value)

    def inverse(self) -> "Z8Element":
        return Z8Element(-self.value)

    def phase(self) -> complex:
        return cmath.exp(2j * cmath.pi * self.value / 8)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Z8Element):
            return self.value == other.value
        if isinstance(other, int):
            return self.value == other % 8
        return False

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return f"Z8Element({self.value})"


ZERO = Z8Element(0)
ONE = Z8Element(1)
TWO = Z8Element(2)
THREE = Z8Element(3)
FOUR = Z8Element(4)
FIVE = Z8Element(5)
SIX = Z8Element(6)
SEVEN = Z8Element(7)


def character(g: Union[Z8Element, int], charge: Union[Z8Element, int]) -> complex:
    g_value = g.value if isinstance(g, Z8Element) else int(g)
    charge_value = charge.value if isinstance(charge, Z8Element) else int(charge)
    return cmath.exp(2j * cmath.pi * g_value * charge_value / 8)
