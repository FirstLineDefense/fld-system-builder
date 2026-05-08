import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from domain.schemas import (
    build_system_input_dto,
    validate_system_input_dto,
)


def run():
    cases = [
        {
            "name": "minimal_valid",
            "input": {
                "project_name": "Regression Test A",
            },
        },
        {
            "name": "null_branches",
            "input": {
                "project_name": "Regression Test B",
                "branches": None,
            },
        },
        {
            "name": "missing_project_name",
            "input": {},
        },
    ]

    failures = []

    for case in cases:
        dto = build_system_input_dto(case["input"])
        valid, errors = validate_system_input_dto(dto)

        print(f"\nCASE: {case['name']}")
        print("DTO:", dto)
        print("VALID:", valid)
        print("ERRORS:", errors)

        if dto["branches"] is None:
            failures.append(f"{case['name']} branches normalization failed")

        if not isinstance(dto["branches"], list):
            failures.append(f"{case['name']} branches not list")

    if failures:
        print("\nFAILURES:")
        for failure in failures:
            print("-", failure)

        raise SystemExit(1)

    print("\nDTO regression harness passed")


if __name__ == "__main__":
    run()
