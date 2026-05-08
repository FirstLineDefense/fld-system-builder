from flask import Blueprint, request, Response
from urllib.parse import parse_qs

import app as legacy_app


legacy_builder_bp = Blueprint("legacy_builder", __name__)


def normalize_legacy_html(html):
    html = html.replace('action="/"', 'action="/builder-v27"')
    html = html.replace("action='/'", "action='/builder-v27'")
    html = html.replace('action=""', 'action="/builder-v27"')
    return html



@legacy_builder_bp.route("/builder-v27", methods=["GET", "POST"])
def builder_v27():
    if request.method == "GET":
        html = legacy_app.build_system_builder_page()
        html = normalize_legacy_html(html)
        return Response(html, mimetype="text/html")

    form = parse_qs(request.get_data(as_text=True))

    selected_control_lines = legacy_app.parse_multi_lines(form, "control", 3)
    selected_sensor_lines = legacy_app.parse_multi_lines(form, "sensor", 5)
    branches = legacy_app.parse_branches(form)

    input_data = {
        "branches": branches,
        "available_water_gallons": float(form.get("available_water_gallons", ["5000"])[0]),
        "required_runtime_minutes": float(form.get("required_runtime_minutes", ["60"])[0]),
        "minimum_pressure_margin_psi": float(form.get("minimum_pressure_margin_psi", ["20"])[0]),
        "max_simultaneous_ports": int(form.get("max_simultaneous_ports", ["1"])[0]),
        "max_budget": float(form.get("max_budget", ["4000"])[0]),
        "engine_name": form.get("engine_name", ["None"])[0],
        "motor_name": form.get("motor_name", ["None"])[0],
        "water_storage_name": form.get("water_storage_name", ["None"])[0],
        "fuel_storage_name": form.get("fuel_storage_name", ["None"])[0],
        "battery_name": form.get("battery_name", ["None"])[0],
        "generator_name": form.get("generator_name", ["None"])[0],
        "selected_controls": selected_control_lines,
        "selected_sensors": selected_sensor_lines,
    }

    accept_suggestion = form.get("accept_suggestion", [""])[0]
    update_section = form.get("update_section", [""])[0]

    if accept_suggestion:
        field_name, suggested_value = accept_suggestion.split(":", 1)
        input_data[field_name] = suggested_value
        input_data["last_updated_section"] = field_name
        input_data["section_update_changes"] = [
            f"Accepted suggestion for {field_name}: {suggested_value}"
        ]

    if update_section:
        input_data = legacy_app.apply_section_update_recommendation(
            input_data,
            update_section
        )

    result = legacy_app.run_system(input_data)

    input_data["builder_suggestions"] = result.get(
        "builder_suggestions",
        {}
    )

    export_paths = legacy_app.write_export_files(input_data, result)
    results_html = legacy_app.build_results_html(result, export_paths)
    html = legacy_app.build_system_builder_page(results_html, input_data)
    html = normalize_legacy_html(html)

    return Response(html, mimetype="text/html")
