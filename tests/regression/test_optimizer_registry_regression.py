import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from services.optimizer_execution_service import (
    run_optimizer,
)

from registries.optimizer_registry import (
    optimizer_registry,
)

from registries.default_optimizers import (
    register_default_optimizers,
)


def run():
    register_default_optimizers()

    print("\nREGISTERED OPTIMIZERS:")
    print(optimizer_registry.names())

    result = run_optimizer(
        "basic",
        {
            "target_gpm": 120,
            "target_psi": 110,
        },
    )

    print("\nOPTIMIZER RESULT:")
    print(result)

    assert result["optimizer"] == "basic"
    assert result["status"] == "success"

    print("\nOptimizer registry regression passed")


if __name__ == "__main__":
    run()
