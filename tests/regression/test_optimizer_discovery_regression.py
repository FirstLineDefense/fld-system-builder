import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from services.optimizer_discovery_service import (
    discover_optimizers,
)


def run():
    optimizers = discover_optimizers()

    print("\nDISCOVERED OPTIMIZERS:")
    print(optimizers)

    assert len(optimizers) >= 1

    optimizer = optimizers[0]

    assert optimizer["name"] == "basic"

    assert (
        "minimum_viable_match"
        in optimizer["capabilities"]
    )

    print("\nOptimizer discovery regression passed")


if __name__ == "__main__":
    run()
