import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from calculations.tm_1d import evaluate_expectation


def random_1d_circuit(n: int, depth: int) -> list[tuple[str, int, int | None]]:
    gates = []
    for _ in range(depth):
        name = random.choice(["H", "S", "T", "CNOT"])
        if name in {"H", "S", "T"}:
            target = random.randrange(n)
            gates.append((name, target, None))
        else:
            control = random.randrange(n - 1)
            target = control + 1
            gates.append((name, control, target))
    return gates


def main() -> None:
    for L in [10, 20]:
        circuit = random_1d_circuit(L, depth=15)
        observable = "Z" + "I" * (L - 1)
        value = evaluate_expectation(L, circuit, observable)
        print(f"L={L}, <Z_0>={value:.6f}")


if __name__ == "__main__":
    main()
