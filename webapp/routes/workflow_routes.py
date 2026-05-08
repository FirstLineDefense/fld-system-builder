import os
import json
from flask import Blueprint, render_template

workflow_bp = Blueprint("workflow", __name__)


def _load_projects():
    projects_dir = os.path.join(os.getcwd(), "projects")
    items = []

    if not os.path.exists(projects_dir):
        return items

    for f in os.listdir(projects_dir):
        if f.endswith(".json"):
            try:
                with open(os.path.join(projects_dir, f), "r") as fp:
                    data = json.load(fp)
                    data["_filename"] = f
                    items.append(data)
            except:
                continue

    return items


def _load_reports():
    projects_dir = os.path.join(os.getcwd(), "projects")
    reports = []

    if not os.path.exists(projects_dir):
        return reports

    for f in os.listdir(projects_dir):
        if f.endswith(".json"):
            try:
                with open(os.path.join(projects_dir, f), "r") as fp:
                    data = json.load(fp)

                if "saved_path" in data:
                    reports.append({
                        "name": data.get("project_name", "Unnamed"),
                        "path": data["saved_path"],
                        "_filename": f
                    })
            except:
                continue

    return reports


@workflow_bp.route("/workflow")
def workflow_home():

    projects = _load_projects()
    reports = _load_reports()

    return render_template(
        "workflow_home.html",
        projects=projects,
        reports=reports
    )
