from flask import Blueprint, render_template, request

from services.project_storage_service import save_project
from services.report_service import build_project_report

report_bp = Blueprint("reports", __name__)


@report_bp.route("/project-report", methods=["GET", "POST"])
def project_report():
    project = None

    if request.method == "POST":
        project = build_project_report(request.form)
        project["saved_path"] = save_project(project)

    return render_template("project_report.html", project=project)
