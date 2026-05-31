import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from calculations.transfer_matrix.benchmark import run_benchmark


if __name__ == "__main__":
    run_benchmark()
