from flask import Flask, request, send_from_directory

flask_app = Flask(__name__)


def system_builder_get():
    return """
    <h1>FLD System Builder</h1>
    <ul>
        <li><a href="/project-report">Project Report</a></li>
        <li><a href="/pump-curves">Pump Curves</a></li>
        <li><a href="/optimizer/run">Optimizer</a></li>
        <li><a href="/components">Components</a></li>
        <li><a href="/projects">Projects</a></li>
    </ul>
    """

from services.output.project_report_model import ProjectReport

def _inject_pricing_html(report):
    pricing = report.get("pricing", {})
    if not pricing:
        return ""

    internal = pricing.get("internal", {})
    client = pricing.get("client", {})

    return f'''
    <div class="pricing-block">
        <h2>Pricing Summary</h2>

        
        <ul>
            <li>Base: {internal.get("base_cost", 0)}</li>
            <li>Labor: {internal.get("labor_cost", 0)}</li>
            <li>Total: {internal.get("total_internal_cost", 0)}</li>
        </ul>

        
        <ul>
            <li>Markup: {client.get("markup_percent", 0)}%</li>
            <li>Final Price: {client.get("final_price", 0)}</li>
        </ul>
    </div>
'''

from flask import Flask, request, send_from_directory
import json
from pathlib import Path
from config.proposal_profiles import get_default_proposal_profile, flatten_proposal_profile

from flask import render_template

from services.output.cut_list_service import generate_cut_list
from services.output.bom_service import generate_bom
from services.output.cost_estimation_service import estimate_project_cost
from services.output.owner_summary_service import generate_owner_summary
from services.output.installer_report_service import (
    generate_installer_report,
)
from services.output.html_report_service import generate_html_report
from services.output.project_report_pipeline import generate_project_report_package

from renderers.pump_curve_renderer import build_pump_curve_page
from services.system_builder_service import (
    build_project_metadata,
    build_saved_stub,
)

from services.system_execution_service import (
    execute_system_pipeline,
)

from services.system_persistence_service import (
    persist_system_if_requested,
)

from main import run_system
from export_utils import write_export_files
from pump_curve import (
    export_curve_to_csv,
    validate_curve_points,
    build_curve_svg,
    get_pump_curve_points,
)
from database import (
    save_system_design,
    list_saved_systems,
    get_saved_system,
    delete_saved_system,
    add_pump_curve_point,
    list_pump_curve_points,
    delete_pump_curve_point,
    clear_pump_curve_points,
)
from component_library import get_component_library
from optimizer_service import (
    run_optimizer_service,
)

from services.form_parser_service import (
    build_input_data_from_form,
)

from renderers.page_renderer import (
    enhance_nav,
    build_standalone_page,
)

from renderers.project_renderer import (
    build_saved_projects_page,
    build_saved_project_detail_page,
)

from renderers.optimizer_renderer import (
    build_optimizer_page,
)

from renderers.pump_curve_renderer import (
    build_curve_preview_section,
)

from services.pump_curve_parser_service import (
    parse_bulk_curve_text,
)

from renderers.proposal.snapshot_index_renderer import build_snapshot_index_html
from services.presentation.pdf_export_service import detect_pdf_engine
from services.presentation.proposal_page_service import compose_project_report_page

from services.presentation.proposal_storage_service import (
    save_proposal_html,
    save_proposal_json,
    list_proposal_snapshots,
)









def load_latest_design_for_report():
    path = Path("exports/latest_design.json")

    if not path.exists():
        return None

    raw = json.loads(path.read_text())

    pump = raw.get("pump", {}) or {}
    motor = raw.get("motor", {}) or {}
    raw_branches = raw.get("branches", []) or []

    branches = []
    for index, branch in enumerate(raw_branches, start=1):
        pipe_diameter = branch.get("pipe_diameter_in") or branch.get("pipe_size") or 1
        pipe_size = f"{pipe_diameter:g} inch" if isinstance(pipe_diameter, (int, float)) else str(pipe_diameter)

        branches.append(
            {
                "name": branch.get("name") or f"Live Branch {branch.get('branch_number', index)}",
                "role": branch.get("role"),
                "priority": branch.get("priority"),
                "pipe_name": branch.get("pipe_name"),
                "pipe_size": pipe_size,
                "pipe_type": branch.get("pipe_type", "Schedule 80 PVC"),
                "length_ft": branch.get("pipe_length_ft") or branch.get("length_ft", 0),
                "pipe_length_ft": branch.get("pipe_length_ft") or branch.get("length_ft", 0),
                "elevation_change_ft": branch.get("elevation_change_ft"),
                "sprinkler_count": branch.get("sprinkler_count", 0),
                "elbow_90_qty": branch.get("elbow_90_qty", 0),
                "tee_qty": branch.get("tee_qty", 0),
                "valve_qty": branch.get("valve_qty", 1),
                "target_gpm": branch.get("target_gpm"),
                "final_pressure_psi": branch.get("final_pressure_psi"),
                "required_terminal_pressure_psi": branch.get("required_terminal_pressure_psi"),
                "pressure_margin_psi": branch.get("pressure_margin_psi"),
                "velocity_fps": branch.get("velocity_fps"),
                "passed": branch.get("passed"),
            }
        )

    return {
        "primary": {
            "pump": {
                "name": pump.get("name", f"Live Pump ({pump.get('gpm', 'unknown')} GPM)"),
                "gpm": pump.get("gpm"),
            },
            "motor": {
                "name": motor.get("name", f"Live Motor ({motor.get('hp', 'unknown')} HP)"),
                "hp": motor.get("hp"),
            },
            "branches": branches,
        },
        "summary": raw.get("summary", {}) or {},
        "optimizer_result": raw.get("optimizer_result"),
    }


def project_report_data():
    project = load_latest_design_for_report() or {}
    return json.dumps(project, indent=2, default=str)


def build_project_report_package_from_latest():
    project = load_latest_design_for_report()

    if project is None:
        project = {
            "primary": {
                "pump": {"name": "GX390 Fire Pump"},
                "motor": {"name": "Honda GX390"},
                "branches": []
            },
            "summary": {}
        }

    pricing = {
        "1 inch Schedule 80 PVC": 3.25,
        "1.25 inch Schedule 80 PVC": 4.75,
        "1 inch 90° elbow": 4.50,
        "1.25 inch 90° elbow": 6.25,
        "1 inch tee": 6.25,
        "1.25 inch tee": 8.75,
        "1 inch valve": 28.00,
        "1.25 inch valve": 42.00,
        "Sprinkler / nozzle head": 42.00,
        "GX390 Fire Pump": 1450.00,
        "Honda GX390": 899.00,
    }

    primary = project.get("primary", {}) or {}
    branches = primary.get("branches", []) or []
    summary = project.get("summary", {}) or {}

    total_flow = summary.get("total_flow_gpm")
    installed_flow = summary.get("total_installed_flow_gpm")
    runtime_minutes = summary.get("runtime_minutes")
    total_cost = summary.get("total_cost")
    system_passed = summary.get("system_passed")

    branch_flows = [(branch.get("target_gpm") or 0) for branch in branches]
    branch_velocities = [(branch.get("velocity_fps") or 0) for branch in branches]

    total_target_gpm = total_flow or sum(branch_flows)
    max_velocity = max(branch_velocities or [0])

    best_pressure_margin = max([(branch.get("pressure_margin_psi") or -999999) for branch in branches] or [0])
    worst_pressure_margin = min([(branch.get("pressure_margin_psi") or 0) for branch in branches] or [0])

    hydraulic_summary = {
        "Total Active Flow": f"{total_target_gpm:g} GPM" if total_target_gpm else "Pending live hydraulic flow",
        "Total Installed Flow": f"{installed_flow:g} GPM" if installed_flow is not None else "Pending installed flow",
        "Runtime": f"{runtime_minutes:.1f} minutes" if runtime_minutes is not None else "Pending runtime",
        "System Passed": str(system_passed) if system_passed is not None else "Pending pass/fail",
        "Worst Pressure Margin": f"{worst_pressure_margin:.2f} PSI" if branches else "Pending pressure margin",
        "Best Pressure Margin": f"{best_pressure_margin:.2f} PSI" if branches else "Pending pressure margin",
        "Max Branch Velocity": f"{max_velocity:.2f} FPS" if max_velocity else "Pending velocity data",
        "Estimated Material Cost": f"${total_cost:.2f}" if total_cost is not None else "Pending cost",
    }

    warnings = list(summary.get("warnings", []) or [])

    if max_velocity and max_velocity > 6:
        warnings.append(f"Max branch velocity is {max_velocity:.2f} FPS. Review pipe sizing.")

    if not warnings:
        warnings.append("No live warnings generated yet.")

    recommendations = [
        "Connect full hydraulic pressure and TDH output into report pipeline",
        "Connect optimizer recommendation output into report pipeline",
    ]

    profile = get_default_proposal_profile()
    proposal_inputs = flatten_proposal_profile(profile)

    return generate_project_report_package(
        project=project,
        pricing=pricing,
        hydraulic_summary=hydraulic_summary,
        warnings=warnings,
        recommendations=recommendations,
        cost_override=summary.get("total_cost"),
        proposal_inputs=proposal_inputs,
    )


def project_report_package():
    package = build_project_report_package_from_latest()
    safe_package = {
        "status": package.get("status"),
        "cost_summary": package.get("cost_summary"),
        "proposal_pricing": package.get("proposal_pricing"),
        "project": package.get("project"),
    }
    return json.dumps(safe_package, indent=2, default=str)


def project_report():

    project = load_latest_design_for_report()

    if project is None:
        project = {
            "primary": {
                "pump": {"name": "GX390 Fire Pump"},
                "motor": {"name": "Honda GX390"},
                "branches": []
            }
        }

    pricing = {
        "1 inch Schedule 80 PVC": 3.25,
        "1.25 inch Schedule 80 PVC": 4.75,
        "1 inch 90° elbow": 4.50,
        "1.25 inch 90° elbow": 6.25,
        "1 inch tee": 6.25,
        "1.25 inch tee": 8.75,
        "1 inch valve": 28.00,
        "1.25 inch valve": 42.00,
        "Sprinkler / nozzle head": 42.00,
        "GX390 Fire Pump": 1450.00,
        "Honda GX390": 899.00,
    }

    primary = project.get("primary", {}) or {}
    branches = primary.get("branches", []) or []
    summary = project.get("summary", {}) or {}

    total_flow = summary.get("total_flow_gpm")
    installed_flow = summary.get("total_installed_flow_gpm")
    runtime_minutes = summary.get("runtime_minutes")
    total_cost = summary.get("total_cost")
    system_passed = summary.get("system_passed")

    branch_flows = [(branch.get("target_gpm") or 0) for branch in branches]
    branch_velocities = [(branch.get("velocity_fps") or 0) for branch in branches]

    total_target_gpm = total_flow or sum(branch_flows)
    max_velocity = max(branch_velocities or [0])

    best_pressure_margin = max([(branch.get("pressure_margin_psi") or -999999) for branch in branches] or [0])
    worst_pressure_margin = min([(branch.get("pressure_margin_psi") or 0) for branch in branches] or [0])

    hydraulic_summary = {
        "Total Active Flow": f"{total_target_gpm:g} GPM" if total_target_gpm else "Pending live hydraulic flow",
        "Total Installed Flow": f"{installed_flow:g} GPM" if installed_flow is not None else "Pending installed flow",
        "Runtime": f"{runtime_minutes:.1f} minutes" if runtime_minutes is not None else "Pending runtime",
        "System Passed": str(system_passed) if system_passed is not None else "Pending pass/fail",
        "Worst Pressure Margin": f"{worst_pressure_margin:.2f} PSI" if branches else "Pending pressure margin",
        "Best Pressure Margin": f"{best_pressure_margin:.2f} PSI" if branches else "Pending pressure margin",
        "Max Branch Velocity": f"{max_velocity:.2f} FPS" if max_velocity else "Pending velocity data",
        "Estimated Material Cost": f"${total_cost:.2f}" if total_cost is not None else "Pending cost",
    }

    warnings = list(summary.get("warnings", []) or [])

    if max_velocity and max_velocity > 6:
        warnings.append(f"Max branch velocity is {max_velocity:.2f} FPS. Review pipe sizing.")

    if not warnings:
        warnings.append("No live warnings generated yet.")

    recommendations = [
        "Connect full hydraulic pressure and TDH output into report pipeline",
        "Connect optimizer recommendation output into report pipeline",
    ]

    profile = get_default_proposal_profile()
    proposal_inputs = flatten_proposal_profile(profile)

    package = generate_project_report_package(
        project=project,
        pricing=pricing,
        hydraulic_summary=hydraulic_summary,
        warnings=warnings,
        recommendations=recommendations,
        cost_override=summary.get("total_cost"),
        proposal_inputs=proposal_inputs,
    )

    final_html = compose_project_report_page(
        title="FLD Project Report",
        body_html=package.html_report,
    )

    html_snapshot_path = save_proposal_html(
        "project_report",
        final_html,
    )

    save_proposal_json(
        "project_report",
        {
            "project": project,
            "package": package,
            "html_snapshot_path": html_snapshot_path,
        },
    )

    return final_html

def test_report():

    sample = {
        "primary": {
            "pump": {"name": "GX390 Fire Pump"},
            "motor": {"name": "Honda GX390"},
            "branches": [
                {
                    "name": "Zone 1",
                    "pipe_size": "1 inch",
                    "pipe_type": "Schedule 80 PVC",
                    "length_ft": 120,
                    "sprinkler_count": 6,
                    "elbow_90_qty": 4,
                    "tee_qty": 1,
                    "valve_qty": 1
                }
            ]
        }
    }

    pricing = {
        "1 inch Schedule 80 PVC": 3.25,
        "1 inch 90° elbow": 4.50,
        "1 inch tee": 6.25,
        "1 inch valve": 28.00,
        "Sprinkler / nozzle head": 42.00,
        "GX390 Fire Pump": 1450.00,
        "Honda GX390": 899.00,
    }

    hydraulic_summary = {
        "Total Flow": "120 GPM",
        "Estimated Pressure": "110 PSI",
        "Estimated TDH": "245 ft"
    }

    warnings = [
        "Velocity exceeds recommended threshold on Branch 1"
    ]

    recommendations = [
        "Increase Branch 1 to 1.25 inch pipe"
    ]

    cut_list = generate_cut_list(sample)

    bom = generate_bom(cut_list)

    cost_summary = estimate_project_cost(
        bom=bom,
        pricing=pricing,
    )

    installer_report = generate_installer_report(
        project=sample,
        hydraulic_summary=hydraulic_summary,
        cut_list=cut_list,
        bom=bom,
        warnings=warnings,
        recommendations=recommendations,
    )

    owner_summary = generate_owner_summary(
        project=sample,
        hydraulic_summary=hydraulic_summary,
        cost_summary=cost_summary,
        warnings=warnings,
    )

    html = generate_html_report(
        installer_report=installer_report,
        owner_summary=owner_summary,
    )

    html += _inject_pricing_html(report)
    return html







def proposal_snapshots():
    snapshots = list_proposal_snapshots()
    return build_snapshot_index_html(snapshots)




def download_proposal_html(filename):
    return send_from_directory(
        "exports/proposals/html",
        filename,
        as_attachment=True,
    )


def download_proposal_json(filename):
    return send_from_directory(
        "exports/proposals/json",
        filename,
        as_attachment=True,
    )




def download_proposal_pdf(filename):
    return send_from_directory(
        "exports/proposals/pdf",
        filename,
        as_attachment=True,
    )




def pdf_engine_status():
    return detect_pdf_engine()


def project_report_pdf():
    return {
        "status": "pending",
        "message": "PDF export route established. Rendering engine not connected yet."
    }



    

def components_get():
    return enhance_nav(build_component_manager_page())


def edit_get():
    category = request.args.get("category", "")
    item_name = request.args.get("name", "")
    return enhance_nav(build_edit_page(category, item_name))


def add_post():
    form = flask_form_as_lists()
    category = form.get("category", [""])[0]
    name = add_row(category, form)
    return enhance_nav(build_component_manager_page(f"Added {name}"))


def update_post():
    form = flask_form_as_lists()
    category = form.get("category", [""])[0]
    original_name = form.get("original_name", [""])[0]
    update_row(category, original_name, form)
    updated_name = form.get("name", [original_name])[0]
    return enhance_nav(build_component_manager_page(f"Updated {updated_name}"))


def delete_post():
    form = flask_form_as_lists()
    category = form.get("category", [""])[0]
    name = form.get("name", [""])[0]
    delete_row(category, name)
    return enhance_nav(build_component_manager_page(f"Deleted {name}"))


def pump_curves_get():
    selected_pump_name = request.args.get("pump_name", "")
    return build_pump_curve_page(selected_pump_name=selected_pump_name)


def pump_curves_add_post():
    form = flask_form_as_lists()

    pump_name = form.get("pump_name", [""])[0]
    flow_gpm = form.get("flow_gpm", ["0"])[0]
    pressure_psi = form.get("pressure_psi", ["0"])[0]
    notes = form.get("notes", [""])[0]

    add_pump_curve_point(pump_name, flow_gpm, pressure_psi, notes)

    return build_pump_curve_page(
        message=f"Added curve point for {pump_name}.",
        selected_pump_name=pump_name
    )


def pump_curves_bulk_import_post():
    form = flask_form_as_lists()

    pump_name = form.get("pump_name", [""])[0]
    bulk_text = form.get("bulk_curve_data", [""])[0]
    clear_existing = form.get("clear_existing", ["no"])[0] == "yes"

    rows, errors = parse_bulk_curve_text(bulk_text)

    if clear_existing:
        clear_pump_curve_points(pump_name)

    for row in rows:
        add_pump_curve_point(
            pump_name,
            row["flow_gpm"],
            row["pressure_psi"],
            row["notes"]
        )

    message = f"Imported {len(rows)} curve point(s) for {pump_name}."

    warning = ""
    if errors:
        warning = "Some rows were skipped: " + " | ".join(errors)

    return build_pump_curve_page(
        message,
        warning,
        selected_pump_name=pump_name
    )


def pump_curves_delete_post():
    form = flask_form_as_lists()
    point_id = int(form.get("point_id", ["0"])[0])

    delete_pump_curve_point(point_id)

    return build_pump_curve_page(f"Deleted pump curve point ID {point_id}.")


def pump_curves_clear_post():
    form = flask_form_as_lists()
    pump_name = form.get("pump_name", [""])[0]

    clear_pump_curve_points(pump_name)

    return build_pump_curve_page(
        f"Cleared curve points for {pump_name}.",
        selected_pump_name=pump_name
    )


def pump_curves_validate_post():
    form = flask_form_as_lists()
    pump_name = form.get("pump_name", [""])[0]

    rows = list_pump_curve_points(pump_name)

    points = [
        {
            "flow_gpm": row["flow_gpm"],
            "pressure_psi": row["pressure_psi"],
        }
        for row in rows
    ]

    warnings = validate_curve_points(points)

    if warnings:
        warning_text = " | ".join(warnings)
        return build_pump_curve_page(
            warning=f"Validation warnings for {pump_name}: {warning_text}",
            selected_pump_name=pump_name
        )

    return build_pump_curve_page(
        message=f"Pump curve validation passed for {pump_name}.",
        selected_pump_name=pump_name
    )


def pump_curves_export_post():
    form = flask_form_as_lists()
    pump_name = form.get("pump_name", [""])[0]

    safe_name = pump_name.replace(" ", "_").replace("/", "_")
    filename = f"{safe_name}_curve.csv"
    output_path = f"exports/{filename}"

    export_curve_to_csv(
        pump_name,
        output_path
    )

    return send_from_directory(
        "exports",
        filename,
        as_attachment=True
    )


def optimizer_get():
    return build_optimizer_page()


def optimizer_run_post():
    form = flask_form_as_lists()

    generations = int(form.get("generations", ["20"])[0])
    population_size = int(form.get("population_size", ["20"])[0])

    input_data = {
        "available_water_gallons": float(
            form.get("available_water_gallons", ["5000"])[0]
        ),
        "required_runtime_minutes": float(
            form.get("required_runtime_minutes", ["60"])[0]
        ),
        "pump_gpm": float(
            form.get("pump_gpm", ["300"])[0]
        ),
        "motor_hp": float(
            form.get("motor_hp", ["10"])[0]
        ),
        "branches": [
            {
                "target_gpm": float(
                    form.get("branch_target_gpm", ["120"])[0]
                ),
                "velocity_fps": float(
                    form.get("branch_velocity_fps", ["9"])[0]
                ),
                "pipe_diameter_in": float(
                    form.get("branch_pipe_diameter_in", ["1.0"])[0]
                )
            }
        ]
    }

    result = run_optimizer_service(
        input_data=input_data,
        generations=generations,
        population_size=population_size
    )

    return build_optimizer_page(result)



def projects_get():
    return build_saved_projects_page()


def project_detail_get(system_id):
    return build_saved_project_detail_page(system_id)


def project_load_get(system_id):
    saved = get_saved_system(system_id)

    if not saved:
        return build_saved_projects_page("Saved project not found.")

    next_version = saved["version_label"] + " Revised" if saved["version_label"] else "Revised"

    saved_for_form = saved.copy()
    saved_for_form["version_label"] = next_version

    message = f'<div class="message">Loaded saved project: {saved["project_name"]} {saved["version_label"]}. Edit and save as a new version.</div>'

    return render_system_builder(message, saved["input_data"], saved["project_name"], saved_for_form)


def project_delete_post(system_id):
    delete_saved_system(system_id)
    return build_saved_projects_page(f"Deleted saved project ID {system_id}.")


def exports_get(filename):
    return send_from_directory("exports", filename, as_attachment=True)




if __name__ == "__main__":
    flask_app.run(
        host="127.0.0.1",
        port=5010,
        debug=False,
        use_reloader=False
    )






































@flask_app.route("/")
def home():
    return "FLD SYSTEM ONLINE - ROOT IS WORKING"

