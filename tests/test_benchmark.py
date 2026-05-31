import csv
from pathlib import Path

import numpy as np
from calculations.transfer_matrix.benchmark import run_benchmark


def test_benchmark_creates_csv_and_png(tmp_path: Path):
    csv_path, png_path = run_benchmark(output_dir=str(tmp_path), n_list=[100, 200, 400, 800], repeats=5)

    assert Path(csv_path).exists()
    assert Path(png_path).exists()

    times = []
    ns = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            ns.append(int(row["n"]))
            times.append(float(row["median_time_sec"]))

    assert len(ns) == 4
    coefficients = np.polyfit(ns, times, 1)
    fitted = np.polyval(coefficients, ns)
    ss_res = np.sum((np.array(times) - fitted) ** 2)
    ss_tot = np.sum((np.array(times) - np.mean(times)) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    assert r2 > 0.99
