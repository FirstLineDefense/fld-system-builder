from io import StringIO
from pathlib import Path
import csv

from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    send_file,
    Response,
)

from services.project_storage_service import (
    delete_saved_project,
    list_saved_projects,
    load_saved_project,
)

project_bp = Blueprint("projects", __name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SAVE_DIR = PROJECT_ROOT / "data" / "saved_projects"


@project_bp.route("/projects")
def projects():
    saved_projects = list_saved_projects()
    return render_template("projects.html", saved_projects=saved_projects)


@project_bp.route("/projects/<filename>")
def project_detail(filename):
    project = load_saved_project(filename)
    return render_template(
        "project_detail.html",
        project=project,
        filename=filename,
    )


@project_bp.route("/projects/<filename>/json")
def project_json(filename):
    project = load_saved_project(filename)

    if not project:
        return jsonify({"error": "project not found"}), 404

    return jsonify(project)


@project_bp.route("/projects/<filename>/download")
def project_download(filename):
    safe_name = Path(filename).name
    path = SAVE_DIR / safe_name

    if not path.exists():
        return jsonify({"error": "project not found"}), 404

    return send_file(
        str(path),
        as_attachment=True,
        download_name=safe_name,
    )


@project_bp.route("/projects/<filename>/delete", methods=["POST"])
def project_delete(filename):
    delete_saved_project(filename)
    return redirect("/projects")


@project_bp.route("/projects/<filename>/bom.csv")
def project_bom_csv(filename):
    project = load_saved_project(filename)

    if not project:
        return jsonify({"error": "project not found"}), 404

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Item",
        "Qty",
        "Internal Unit Cost",
        "Internal Total",
        "Client Unit Price",
        "Client Total",
        "Notes",
    ])

    for row in project.get("bom", []):
        writer.writerow([
            row.get("item", ""),
            row.get("qty", ""),
            row.get("unit_cost", ""),
            row.get("internal_total", ""),
            row.get("client_unit_price", ""),
            row.get("client_total", ""),
            row.get("notes", ""),
        ])

    csv_name = Path(filename).stem + "_bom.csv"

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={csv_name}"
        },
    )


@project_bp.route("/projects/<filename>/proposal.csv")
def project_proposal_csv(filename):
    project = load_saved_project(filename)

    if not project:
        return jsonify({"error": "project not found"}), 404

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(["Field", "Value"])
    writer.writerow(["Project Name", project.get("project_name", "")])
    writer.writerow(["Client Name", project.get("client_name", "")])
    writer.writerow(["Client BOM Total", f"${project.get('client_bom_total', 0):,.2f}"])
    writer.writerow(["Design Total", f"${project.get('design_total', 0):,.2f}"])
    writer.writerow(["Maintenance Plan Fee", f"${project.get('maintenance_plan_fee', 0):,.2f}"])
    writer.writerow(["Subscription Cost", f"${project.get('subscription_cost', 0):,.2f}"])
    writer.writerow(["Estimated Client Proposal Total", f"${project.get('client_proposal_total', 0):,.2f}"])
    writer.writerow(["Recommended Tier", project.get("optimizer_recommendation", {}).get("tier", "")])

    csv_name = Path(filename).stem + "_proposal.csv"

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={csv_name}"
        },
    )


@project_bp.route("/projects/<filename>/proposal")
def project_proposal(filename):
    project = load_saved_project(filename)
    if not project:
        return "Project not found", 404

    return render_template(
        "proposal.html",
        project=project,
        filename=filename,
    )
