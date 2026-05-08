import json
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from services.system_execution_service import (
    normalize_and_validate_system_input,
)


def stable_hash(data):
    serialized = json.dumps(
        data,
        sort_keys=True,
    )

    return hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()


def run():
    sample = {
        "project_name": "Optimizer Snapshot Regression",
        "water_source": "pool",
        "pump": {
            "model": "GX390",
            "gpm": 120,
        },
        "motor": {
            "hp": 13,
        },
        "branches": [
            {
                "zone": "A",
                "flow_gpm": 55,
            },
            {
                "zone": "B",
                "flow_gpm": 45,
            },
        ],
    }

    dto = normalize_and_validate_system_input(sample)

    snapshot_hash = stable_hash(dto)

    expected_hash = stable_hash({
        'project_name': 'Optimizer Snapshot Regression',
        'water_source': 'pool',
        'pump': {'model': 'GX390', 'gpm': 120},
        'motor': {'hp': 13},
        'manifold': {},
        'branches': [
            {'zone': 'A', 'flow_gpm': 55},
            {'zone': 'B', 'flow_gpm': 45},
        ],
        'constraints': {},
        'metadata': {},
    })

    print("\nSNAPSHOT HASH:")
    print(snapshot_hash)

    assert snapshot_hash == expected_hash

    print("\nOptimizer snapshot regression passed")


if __name__ == "__main__":
    run()
