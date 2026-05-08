import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from services.presentation.project_identity_service import (
    generate_project_identity,
)


def main():
    identity = generate_project_identity()

    required = {
        "project_name",
        "client_name",
        "proposal_revision",
        "proposal_status",
        "designer",
        "generated_date",
    }

    missing = required - set(identity.keys())

    if missing:
        raise AssertionError(
            f"Missing fields: {missing}"
        )

    print("Project identity smoke test passed.")
    print(identity)


if __name__ == "__main__":
    main()
