import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from services.presentation.system_capability_summary_service import (
    generate_system_capability_summary,
)


def main():
    summary = generate_system_capability_summary(
        hydraulic_summary={
            "total_gpm": 295,
            "system_pressure_psi": 120,
        },
        multi_scenario_proposals={
            "good": {},
            "better": {},
            "best": {},
        },
    )

    required = [
        "FLD SYSTEM CAPABILITY SUMMARY",
        "295 GPM",
        "120 PSI",
        "1.5 inch attack hose",
        "3 deployment/proposal scenarios",
    ]

    for phrase in required:
        if phrase not in summary:
            raise AssertionError(f"Missing phrase: {phrase}")

    print("System capability summary smoke test passed.")
    print(summary)


if __name__ == "__main__":
    main()
