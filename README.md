
# GaugeOracle — Simulate 1D quantum chains in **O(n)** time using ℤ₈ gauge theory

[![Test status](https://img.shields.io/github/actions/workflow/status/Patcex-studio/gauge-oracle/test.yml?branch=main&label=tests)](https://github.com/Patcex-studio/gauge-oracle/actions/workflows/test.yml)
[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20475388.svg)](https://doi.org/10.5281/zenodo.20475388)
**Status:** ✅ 1D implementation — production‑ready.  
🔜 2D/3D theory discussed in the paper (not implemented in this code).

---

## What is this?

GaugeOracle lets you compute **exact expectation values of Pauli operators** for 1D quantum circuits (Clifford + T) in **linear time** O(n) — with **constant memory** per step.

🔑 **Key idea:**  
We encode the quantum state as **topological defects** in a ℤ₈ gauge theory.  
- Clifford gates → gauge transformations (no cost).  
- T gates → insert a defect of charge 1.  
The entire simulation reduces to multiplying fixed **8×8 matrices** – no exponential blow‑up.

📄 Full theoretical details are in the accompanying paper (`paper/`).

> ⚠️ **Important:** This code implements **only 1D** chains. Higher‑dimensional algorithms are not provided – they are described purely in the paper.

---

## Quick start

```bash
# Clone the repository
git clone https://github.com/USER/REPO.git
cd REPO

# Install dependencies
pip install -r requirements.txt

# Run a simple example (GHZ state)
python calculations/examples/ghz_3q.py

# Run all tests
pytest tests/
```

---

## Project structure

| Directory | Purpose |
|-----------|---------|
| `theory/` | ℤ₈ gauge theory, defect representation, Clifford+T dictionary |
| `calculations/` | Transfer‑matrix evaluation, benchmarks, examples |
| `tests/` | Unit tests (correctness + linear scaling) |
| `paper/` | LaTeX source of the research article |
| `.github/workflows/` | CI for tests and PDF compilation |

---

## Examples you can run

- **`ghz_3q.py`** – Build a 3‑qubit GHZ state, print `<XXX>` and `<ZZZ>`.
- **`random_clifford_t.py`** – Random 1D Clifford+T circuit, measure `<Z₀>`.
- **`benchmark.py`** – Quick runtime test (plots saved to `experiments/plots/`).
- **`calculations/transfer_matrix/benchmark.py`** – **Full benchmark** with CSV output, error bars, linear regression and R².

---

## Benchmark results (proof of O(n))

| n qubits | defects | median time (s) | std dev (s) |
|----------|---------|----------------|--------------|
| 10       | 1       | 0.00048        | 0.00011      |
| 100      | 10      | 0.00467        | 0.00151      |
| 500      | 50      | 0.02510        | 0.00251      |
| 1000     | 100     | 0.04815        | 0.00116      |
| 2000     | 200     | 0.09369        | 0.02519      |
| 5000     | 500     | 0.24355        | 0.03165      |
| 10000    | 1000    | 0.47476        | 0.08604      |

📈 **Linear scaling confirmed** – slope ≈ 4.7×10⁻⁵ s/qubit, **R² > 0.999**.

Run the full benchmark yourself:
```bash
python -m calculations.transfer_matrix.benchmark
```
Plots and data are saved to `experiments/benchmark/`.

---

## Build the paper locally

```bash
make
```
Requires a working LaTeX installation (`latexmk`, `pdflatex`).

---

## Citation

If you use this code or the results in a scientific publication, please cite it using the metadata in [`CITATION.cff`](CITATION.cff).

---

## License

- **Code:** BSD‑3‑Clause (see [LICENSE](LICENSE))
- **Paper text:** CC BY 4.0


