import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from services.system_execution_service import (
    normalize_and_validate_system_input,
)


def run():
    sample = {
        "project_name": "Service Execution Regression",
        "water_source": "pool",
        "branches": [
            {
                "zone": "A",
                "flow_gpm": 55,
            }
        ],
    }

    dto = normalize_and_validate_system_input(sample)

    print("\nDTO RESULT:")
    print(dto)

    assert dto["project_name"] == "Service Execution Regression"
    assert dto["water_source"] == "pool"
    assert isinstance(dto["branches"], list)
    assert len(dto["branches"]) == 1

    branch = dto["branches"][0]

    assert branch["zone"] == "A"
    assert branch["flow_gpm"] == 55

    print("\nService execution regression passed")


if __name__ == "__main__":
    run()
