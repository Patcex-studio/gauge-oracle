import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from calculations.tm_1d import evaluate_expectation


def main():
    n = 3
    circuit = [
        ("H", 0, None),
        ("CNOT", 0, 1),
        ("CNOT", 0, 2),
    ]
    for observable in ["XXX", "ZZZ"]:
        expectation = evaluate_expectation(n, circuit, observable)
        print(f"Observable {observable}: {expectation:.6f}")


if __name__ == "__main__":
    main()
