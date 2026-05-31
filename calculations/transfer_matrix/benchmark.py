import csv
from pathlib import Path
import time
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from calculations.transfer_matrix.tm_1d import expectation_value


def run_benchmark(
    output_dir: str = "experiments/benchmark",
    n_list: Optional[List[int]] = None,
    defect_density: float = 0.1,
    repeats: int = 5,
) -> Tuple[str, str]:
    if n_list is None:
        n_list = [10, 100, 500, 1000, 2000, 5000, 10000]

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    csv_path = output_path / "tm_1d_benchmark.csv"
    png_path = output_path / "tm_1d_runtime.png"

    results: List[Tuple[int, float, float, int]] = []
    rng = np.random.default_rng(123456)

    for n in n_list:
        defect_count = max(1, int(n * defect_density))
        positions = rng.choice(n, size=defect_count, replace=False)
        defects: Dict[int, int] = {int(pos): 1 for pos in positions}
        observable = "X" * n

        run_times: List[float] = []
        for _ in range(repeats):
            start = time.perf_counter()
            expectation_value(n, defects, observable)
            run_times.append(time.perf_counter() - start)

        median_time = float(np.median(run_times))
        std_dev = float(np.std(run_times, ddof=0))
        results.append((n, median_time, std_dev, defect_count))
        print(f"n={n}, defect_count={defect_count}, median={median_time:.6f}s, std={std_dev:.6f}s")

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["n", "median_time_sec", "std_dev_sec", "defect_count"])
        writer.writerows(results)

    n_values = np.array([row[0] for row in results], dtype=float)
    medians = np.array([row[1] for row in results], dtype=float)
    std_dev = np.array([row[2] for row in results], dtype=float)

    coefficients = np.polyfit(n_values, medians, 1)
    fitted = np.polyval(coefficients, n_values)
    ss_res = np.sum((medians - fitted) ** 2)
    ss_tot = np.sum((medians - medians.mean()) ** 2)
    r_squared = float(1.0 - ss_res / ss_tot) if ss_tot > 0 else 1.0
    slope = float(coefficients[0])
    intercept = float(coefficients[1])

    plt.figure(figsize=(8, 5))
    plt.errorbar(n_values, medians, yerr=std_dev, fmt="o", capsize=4, label="Median runtime")
    plt.plot(n_values, fitted, label=f"Linear fit: {slope:.3e} n + {intercept:.3e}")
    plt.xlabel("n qubits")
    plt.ylabel("median wall time (s)")
    plt.title("1D transfer matrix runtime vs n")
    plt.legend()
    plt.grid(True)
    plt.text(
        0.05,
        0.95,
        f"slope={slope:.3e}\nR^2={r_squared:.4f}",
        transform=plt.gca().transAxes,
        verticalalignment="top",
        bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "black"},
    )
    plt.tight_layout()
    plt.savefig(png_path)
    print(f"Saved benchmark plot to {png_path}")

    return str(csv_path), str(png_path)


if __name__ == "__main__":
    run_benchmark()
