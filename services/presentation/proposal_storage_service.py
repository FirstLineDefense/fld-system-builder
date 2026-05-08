from pathlib import Path
import json
from datetime import datetime


EXPORT_ROOT = Path("exports/proposals")


def ensure_proposal_storage():
    (EXPORT_ROOT / "html").mkdir(parents=True, exist_ok=True)
    (EXPORT_ROOT / "pdf").mkdir(parents=True, exist_ok=True)
    (EXPORT_ROOT / "json").mkdir(parents=True, exist_ok=True)
    (EXPORT_ROOT / "assets").mkdir(parents=True, exist_ok=True)


def build_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_proposal_json(name, payload):
    ensure_proposal_storage()

    timestamp = build_timestamp()

    path = EXPORT_ROOT / "json" / f"{timestamp}_{name}.json"

    path.write_text(
        json.dumps(payload, indent=2, default=str)
    )

    return str(path)


def save_proposal_html(name, html):
    ensure_proposal_storage()

    timestamp = build_timestamp()

    path = EXPORT_ROOT / "html" / f"{timestamp}_{name}.html"

    path.write_text(html)

    return str(path)


def list_proposal_snapshots():
    ensure_proposal_storage()

    html_files = sorted(
        str(path) for path in (EXPORT_ROOT / "html").glob("*.html")
    )

    json_files = sorted(
        str(path) for path in (EXPORT_ROOT / "json").glob("*.json")
    )

    pdf_files = sorted(
        str(path) for path in (EXPORT_ROOT / "pdf").glob("*.pdf")
    )

    return {
        "html": html_files,
        "json": json_files,
        "pdf": pdf_files,
    }
