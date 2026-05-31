from dataclasses import dataclass
from typing import Tuple, Dict

_PAULI_OPERATORS = {"I", "X", "Y", "Z"}

_SINGLE_QUBI_PRIOR = {
    "I": 0,
    "X": 1,
    "Y": 2,
    "Z": 3,
}
_XX = [
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
]

_H_MAP = {
    "I": ("I", 1),
    "X": ("Z", 1),
    "Y": ("-Y", 1),
    "Z": ("X", 1),
}
_S_MAP = {
    "I": ("I", 1),
    "X": ("Y", 1),
    "Y": ("-X", 1),
    "Z": ("Z", 1),
}

_CNOT_PAIR_MAP: Dict[Tuple[str, str], Tuple[str, str, int]] = {
    ("I", "I"): ("I", "I", 1),
    ("I", "X"): ("I", "X", 1),
    ("I", "Y"): ("Z", "Y", 1),
    ("I", "Z"): ("Z", "Z", 1),
    ("X", "I"): ("X", "X", 1),
    ("X", "X"): ("X", "I", 1),
    ("X", "Y"): ("Y", "Z", 1),
    ("X", "Z"): ("Y", "Y", 1),
    ("Y", "I"): ("Y", "X", 1),
    ("Y", "X"): ("Z", "Y", 1),
    ("Y", "Y"): ("X", "Z", -1),
    ("Y", "Z"): ("X", "Y", 1),
    ("Z", "I"): ("Z", "I", 1),
    ("Z", "X"): ("Z", "X", 1),
    ("Z", "Y"): ("I", "Y", 1),
    ("Z", "Z"): ("I", "Z", 1),
}


@dataclass(frozen=True)
class PauliString:
    string: str
    phase: complex = 1 + 0j

    def __post_init__(self):
        normalized = self.string.upper()
        if any(ch not in _PAULI_OPERATORS for ch in normalized):
            raise ValueError(f"Invalid Pauli string: {self.string}")
        object.__setattr__(self, "string", normalized)
        object.__setattr__(self, "phase", complex(self.phase))

    def _conjugate_single(self, index: int, mapping: Dict[str, Tuple[str, int]]) -> "PauliString":
        chars = list(self.string)
        old = chars[index]
        new_symbol, sign = mapping.get(old, (old, 1))
        phase = self.phase * sign
        if new_symbol.startswith("-"):
            phase *= -1
            new_symbol = new_symbol[1:]
        chars[index] = new_symbol
        return PauliString("".join(chars), phase)

    def _conjugate_cnot(self, control: int, target: int) -> "PauliString":
        chars = list(self.string)
        c = chars[control]
        t = chars[target]
        new_c, new_t, sign = _CNOT_PAIR_MAP.get((c, t), (c, t, 1))
        chars[control] = new_c
        chars[target] = new_t
        return PauliString("".join(chars), self.phase * sign)

    def conjugate_by(self, gate: str, targets: Tuple[int, ...]) -> "PauliString":
        gate_name = gate.upper()
        if gate_name == "H":
            return self._conjugate_single(targets[0], _H_MAP)
        if gate_name == "S":
            return self._conjugate_single(targets[0], _S_MAP)
        if gate_name == "CNOT":
            return self._conjugate_cnot(targets[0], targets[1])
        return self


def transform_observable(pauli_string: str, gate: str, *targets: int) -> PauliString:
    pauli = PauliString(pauli_string)
    return pauli.conjugate_by(gate, tuple(targets))
