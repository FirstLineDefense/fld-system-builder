from flask import Blueprint, request

from main import run_system, run_auto_update
from export_utils import write_export_files
from app import build_system_builder_page
from renderers.system_builder_page_renderer import build_system_builder_page_html

legacy_builder_bp = Blueprint("legacy_builder", __name__)


def normalize_legacy_html(html):
    html = html.replace('<form method="post">', '<form method="post" action="/builder-v27">')
    html = html.replace("<form method='post'>", "<form method='post' action=\"/builder-v27\">")
    html = html.replace('<form method="POST">', '<form method="POST" action="/builder-v27">')
    html = html.replace('action="/"', 'action="/builder-v27"')
    html = html.replace("action='/'", "action='/builder-v27'")
    html = html.replace('action=""', 'action="/builder-v27"')
    html = html.replace('action="/builder-v27/builder-v27"', 'action="/builder-v27"')
    return html


def _form_to_dict(form):
    return {
        k: form.getlist(k)[0] if isinstance(form.getlist(k), list) else form.get(k)
        for k in form.keys()
    }


def _normalize_types(data):
    """
    80/20 type safety layer so legacy engine receives correct types.
    """

    def to_int(v):
        try:
            return int(v)
        except Exception:
            return 0

    def to_float(v):
        try:
            return float(v)
        except Exception:
            return 0.0

    if "required_runtime_minutes" in data:
        data["required_runtime_minutes"] = to_int(data["required_runtime_minutes"])

    if "available_water_gallons" in data:
        data["available_water_gallons"] = to_int(data["available_water_gallons"])

    if "max_budget" in data:
        data["max_budget"] = to_float(data["max_budget"])

    if "minimum_pressure_margin_psi" in data:
        data["minimum_pressure_margin_psi"] = to_float(data["minimum_pressure_margin_psi"])

    if "preferred_velocity_fps" in data:
        data["preferred_velocity_fps"] = to_float(data["preferred_velocity_fps"])

    if "maximum_velocity_fps" in data:
        data["maximum_velocity_fps"] = to_float(data["maximum_velocity_fps"])

    if "max_simultaneous_ports" in data:
        data["max_simultaneous_ports"] = to_int(data["max_simultaneous_ports"])

    return data


@legacy_builder_bp.route("/builder-v27", methods=["GET", "POST"])
def builder_v27():
    resume_file = request.args.get("resume")

    if request.method == "GET":

        # optional resume hook (lightweight, safe, non-invasive)
        if resume_file:
            try:
                import json, os
                path = os.path.join(os.getcwd(), "projects", resume_file)
                with open(path, "r") as f:
                    resume_data = json.load(f)

                html = build_system_builder_page(
                    initial_data=resume_data
                )
                return normalize_legacy_html(html)
            except:
                pass

        html = build_system_builder_page()
        return normalize_legacy_html(html)

    form_data = _form_to_dict(request.form)
    form_data = _normalize_types(form_data)

    update_section = form_data.get("update_section")

    if update_section:
        from section_update_recommendations import apply_section_update_recommendation
        form_data = apply_section_update_recommendation(
            form_data,
            update_section
        )

    result = run_system(form_data)

    form_data["builder_suggestions"] = result.get(
        "builder_suggestions",
        {}
    )

    form_data["section_statuses"] = result.get(
        "section_statuses",
        {}
    )

    if form_data.get("action_code"):
        auto = run_auto_update(
            input_data=form_data,
            action_code=form_data.get("action_code")
        )
        result = auto.get("result", result)

    render_result = result.get("primary", result)

    if isinstance(render_result, dict):
        render_result["engineering_recommendations"] = result.get(
            "engineering_recommendations",
            render_result.get("engineering_recommendations", [])
        )

    export_paths = write_export_files(form_data, result)
    result["export_paths"] = export_paths

    html = build_system_builder_page(
        results=render_result,
        initial_data=form_data
    )

    return normalize_legacy_html(html)
