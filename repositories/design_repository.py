import json
from pathlib import Path

from domain.design_state import (
    normalize_primary,
)


DEFAULT_EXPORT_DIR = Path("exports")


def ensure_export_dir():
    DEFAULT_EXPORT_DIR.mkdir(
        exist_ok=True
    )


def save_primary_design(
    primary,
    filename="latest_design.json"
):
    ensure_export_dir()

    primary = normalize_primary(primary)

    path = DEFAULT_EXPORT_DIR / filename

    path.write_text(
        json.dumps(
            primary,
            indent=2
        )
    )

    return str(path)


def load_primary_design(
    filename="latest_design.json"
):
    ensure_export_dir()

    path = DEFAULT_EXPORT_DIR / filename

    if not path.exists():
        return None

    return normalize_primary(
        json.loads(
            path.read_text()
        )
    )
