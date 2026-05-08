import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from services.presentation.proposal_metadata_service import (
    generate_proposal_metadata,
)


def main():
    metadata = generate_proposal_metadata(
        client_name="John Smith",
        property_address="123 Canyon Ridge Rd",
    )

    required = {
        "proposal_id",
        "generated_date",
        "generated_time",
        "client_name",
        "property_address",
        "prepared_by",
        "proposal_status",
    }

    missing = required - set(metadata.keys())

    if missing:
        raise AssertionError(f"Missing metadata fields: {missing}")

    if not metadata["proposal_id"].startswith("FLD-"):
        raise AssertionError("Proposal ID format invalid.")

    print("Proposal metadata smoke test passed.")
    print(metadata)


if __name__ == "__main__":
    main()
