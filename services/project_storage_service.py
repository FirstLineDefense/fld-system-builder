import json
import re
from datetime import datetime
from pathlib import Path


SAVE_DIR = Path("data/saved_projects")


def slugify(value):
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_") or "project"


def save_project(project):
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    project_name = project.get("project_name", "project")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{slugify(project_name)}.json"
    path = SAVE_DIR / filename

    with path.open("w") as f:
        json.dump(project, f, indent=2)

    return str(path)


def list_saved_projects():
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    projects = []
    for path in sorted(SAVE_DIR.glob("*.json"), reverse=True):
        projects.append({
            "filename": path.name,
            "path": str(path),
            "modified": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        })

    return projects


def load_saved_project(filename):
    safe_name = Path(filename).name
    path = SAVE_DIR / safe_name

    if not path.exists():
        return None

    with path.open("r") as f:
        return json.load(f)


def delete_saved_project(filename):
    safe_name = Path(filename).name
    path = SAVE_DIR / safe_name

    if not path.exists():
        return False

    path.unlink()
    return True
