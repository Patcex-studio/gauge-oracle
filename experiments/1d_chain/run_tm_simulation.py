import time
from calculations.tm_1d import evaluate_expectation


def run_simulation():
    for n in [10, 50, 100, 200]:
        circuit = [("T", i % n, None) for i in range(min(n, 10))]
        observable = "X" * n
        start = time.perf_counter()
        value = evaluate_expectation(n, circuit, observable)
        elapsed = time.perf_counter() - start
        print(f"n={n}, expectation={value:.6f}, elapsed={elapsed:.6f}s")


if __name__ == "__main__":
    run_simulation()
