from flask import Blueprint, render_template, request

from services.report_service import build_project_report

optimizer_bp = Blueprint("optimizer", __name__)


@optimizer_bp.route("/optimizer", methods=["GET", "POST"])
def optimizer():
    project = None

    if request.method == "POST":
        project = build_project_report(request.form)

    return render_template("optimizer.html", project=project)
