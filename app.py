import csv
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, quote_plus, unquote_plus
from main import run_system, run_auto_update
from component_library import get_component_library
from export_utils import write_export_files
from pump_curve import build_curve_svg, get_pump_curve_points
from section_update_recommendations import apply_section_update_recommendation
from renderers.intelligence.design_readiness_renderer import build_design_readiness_html
from renderers.intelligence.design_direction_renderer import build_design_direction_html
from renderers.intelligence.architecture_recommendations_renderer import build_architecture_recommendations_html
from renderers.intelligence.bottleneck_intelligence_renderer import build_bottleneck_intelligence_html
from renderers.intelligence.scenario_comparison_renderer import build_scenario_comparison_html
from renderers.intelligence.section_readiness_renderer import build_section_readiness_html
from renderers.intelligence.guided_builder_summary_renderer import build_guided_builder_summary_html
from renderers.intelligence.auto_select_summary_renderer import build_auto_select_summary_html
from renderers.intelligence.overall_readiness_banner_renderer import build_overall_readiness_banner_html
from renderers.intelligence.design_maturity_renderer import build_design_maturity_html
from services.presentation.proposal_page_service import compose_project_report_page
from renderers.constraint_violation_renderer import build_constraint_violation_html as _build_constraint_violation_html
from renderers.intelligence.design_direction_renderer import build_design_direction_html
from renderers.intelligence.auto_select_summary_renderer import build_auto_select_summary_html
from renderers.intelligence.design_maturity_renderer import build_design_maturity_html
from renderers.intelligence.section_readiness_renderer import build_section_readiness_html
from renderers.intelligence.guided_builder_summary_renderer import build_guided_builder_summary_html
from renderers.intelligence.overall_readiness_banner_renderer import build_overall_readiness_banner_html
from renderers.intelligence.bottleneck_intelligence_renderer import build_bottleneck_intelligence_html
from renderers.intelligence.design_readiness_renderer import build_design_readiness_html
from renderers.intelligence.scenario_comparison_renderer import build_scenario_comparison_html
from renderers.intelligence.architecture_recommendations_renderer import build_architecture_recommendations_html
from renderers.auto_apply_renderer import build_auto_apply_html
from renderers.branch_results_renderer import build_branch_results_html
from renderers.operating_modes_renderer import build_operating_modes_html
from renderers.selected_components_renderer import build_selected_components_html
from renderers.storage_power_renderer import build_storage_power_html
from renderers.engineering_recommendations_renderer import build_engineering_recommendations_html
from renderers.optimizer_recommendation_renderer import build_optimizer_recommendation_html
from renderers.hydraulic_intelligence_renderer import build_hydraulic_intelligence_html
from renderers.system_curve_overlay_renderer import build_system_curve_overlay_html
from renderers.hydraulic_optimizer_renderer import build_hydraulic_optimizer_html
from renderers.system_builder_page_renderer import build_system_builder_page_html


def _legacy_to_dict(value):
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if hasattr(value, "__dict__"):
        return dict(value.__dict__)
    return value


def _normalize_primary_for_extracted_renderers(primary):
    if not isinstance(primary, dict):
        return primary

    normalized = dict(primary)

    for key in [
        "pump",
        "engine",
        "motor",
        "water_storage",
        "fuel_storage",
        "battery",
        "generator",
    ]:
        if key in normalized:
            normalized[key] = _legacy_to_dict(normalized[key])

    return normalized


def build_constraint_violation_html(primary):
    normalized_primary = _normalize_primary_for_extracted_renderers(primary)
    violations = (
        normalized_primary.get("constraint_violations")
        or normalized_primary.get("violations")
        or normalized_primary.get("constraint_violation_summary")
        or []
    )
    return _build_constraint_violation_html(normalized_primary, violations)




PORT = 8018
MAX_DEVICES_PER_BRANCH = 3
EXPORT_DIR = "exports"

COMPONENT_CONFIG = {
    "pumps": {"title": "Pumps", "path": "data/pumps.csv", "fields": ["name", "component_type", "unit_cost", "notes", "max_flow_gpm", "max_pressure_psi", "pump_type", "inlet_size_in", "outlet_size_in"], "defaults": {"component_type": "pump"}},
   "pipes": {
    "title": "Pipes",
    "path": "data/pipes.csv",
    "fields": [
        "name",
        "component_type",
        "unit_cost",
        "notes",
        "diameter_in",
        "internal_diameter_in",
        "wall_type",
        "pressure_rating_psi",
        "c_factor",
        "material",
    ],
    "defaults": {
        "component_type": "pipe",
        "c_factor": "150",
        "wall_type": "Sch40"
    },
},
    "devices": {"title": "Sprinklers / Terminal Devices", "path": "data/devices.csv", "fields": ["name", "component_type", "unit_cost", "notes", "flow_gpm", "required_pressure_psi", "nozzle_size", "throw_diameter_ft"], "defaults": {"component_type": "terminal"}},
    "engines": {"title": "Engines", "path": "data/engines.csv", "fields": ["name", "component_type", "unit_cost", "notes", "fuel_type", "horsepower", "fuel_burn_gph"], "defaults": {"component_type": "engine"}},
    "motors": {"title": "Motors", "path": "data/motors.csv", "fields": ["name", "component_type", "unit_cost", "notes", "horsepower", "voltage", "phase", "efficiency"], "defaults": {"component_type": "motor"}},
    "water_storage": {"title": "Water Storage", "path": "data/water_storage.csv", "fields": ["name", "component_type", "unit_cost", "notes", "capacity_gallons", "storage_type"], "defaults": {"component_type": "water_storage"}},
    "fuel_storage": {"title": "Fuel Storage", "path": "data/fuel_storage.csv", "fields": ["name", "component_type", "unit_cost", "notes", "capacity_gallons", "fuel_type"], "defaults": {"component_type": "fuel_storage"}},
    "batteries": {"title": "Batteries", "path": "data/batteries.csv", "fields": ["name", "component_type", "unit_cost", "notes", "capacity_kwh", "usable_fraction"], "defaults": {"component_type": "battery", "usable_fraction": "0.8"}},
    "generators": {"title": "Generators", "path": "data/generators.csv", "fields": ["name", "component_type", "unit_cost", "notes", "continuous_kw", "surge_kw", "fuel_type"], "defaults": {"component_type": "generator"}},
    "controls": {"title": "Controls", "path": "data/controls.csv", "fields": ["name", "component_type", "unit_cost", "notes", "control_type"], "defaults": {"component_type": "control"}},
    "sensors": {"title": "Sensors", "path": "data/sensors.csv", "fields": ["name", "component_type", "unit_cost", "notes", "sensor_type"], "defaults": {"component_type": "sensor"}},
}


def build_nav():
    return """
    <p>
        <a href="/">System Builder</a> |
        <a href="/components">Component Manager</a>
    </p>
    """


def read_csv_rows(path):
    from database import rows_for_path
    return rows_for_path(path)


def write_csv_rows(path, rows, fieldnames):
    from database import write_rows_for_path
    write_rows_for_path(path, rows, fieldnames)


def get_config(category):
    return COMPONENT_CONFIG.get(category)


def add_row(category, form):
    config = get_config(category)
    rows, fieldnames = read_csv_rows(config["path"])
    new_row = {}

    for field in config["fields"]:
        if field in config.get("defaults", {}):
            new_row[field] = config["defaults"][field]
        else:
            new_row[field] = form.get(field, [""])[0]

    rows.append(new_row)
    write_csv_rows(config["path"], rows, fieldnames)

    return new_row["name"]


def update_row(category, original_name, form):
    config = get_config(category)
    rows, fieldnames = read_csv_rows(config["path"])

    for row in rows:
        if row["name"] == original_name:
            for field in config["fields"]:
                if field in config.get("defaults", {}):
                    row[field] = config["defaults"][field]
                else:
                    row[field] = form.get(field, [row.get(field, "")])[0]

    write_csv_rows(config["path"], rows, fieldnames)


def delete_row(category, item_name):
    config = get_config(category)
    rows, fieldnames = read_csv_rows(config["path"])
    rows = [row for row in rows if row["name"] != item_name]
    write_csv_rows(config["path"], rows, fieldnames)


def get_row(category, item_name):
    config = get_config(category)
    rows, _ = read_csv_rows(config["path"])

    for row in rows:
        if row["name"] == item_name:
            return row

    return None


def field_label(field):
    return field.replace("_", " ").title()


def build_form_fields(config, row=None, include_original=False):
    html = ""

    if include_original and row:
        html += f'<input type="hidden" name="original_name" value="{row["name"]}">'

    for field in config["fields"]:
        if field in config.get("defaults", {}):
            continue

        value = row.get(field, "") if row else ""
        required = "required" if field in ["name", "unit_cost"] else ""

        input_type = "text"
        step = ""

        if field not in [
            "name", "notes", "component_type", "pump_type", "material",
            "nozzle_size", "fuel_type", "phase", "storage_type",
            "control_type", "sensor_type"
        ]:
            input_type = "number"
            step = ' step="0.01"'

        html += f"<label>{field_label(field)}</label>"
        html += f'<input type="{input_type}"{step} name="{field}" value="{value}" {required}>'

    return html


def build_branch_suggestion_html(builder_suggestions):
    manifold_data = builder_suggestions.get(
        "manifold_branches",
        {}
    )

    branch_suggestions = manifold_data.get(
        "branch_suggestions",
        []
    )

    if not branch_suggestions:
        return ""

    confidence_icons = {
        "green": "✅",
        "yellow": "⚠️",
        "red": "❌",
    }

    html = '<div class="branch-suggestion-wrapper">'

    for branch in branch_suggestions:
        confidence = branch.get("confidence", "red")
        icon = confidence_icons.get(confidence, "❔")

        title = branch.get("title", "")
        reason = branch.get("reason", "")

        html += f"""
        <div class="field-suggestion suggestion-{confidence}">
            <div class="suggestion-header">
                <span class="suggestion-icon">{icon}</span>
                <strong>{title}</strong>
    div>

            <p>{reason}</p>
        </div>
        """

    html += "</div>"

    return html


def build_add_form(category):
    config = get_config(category)

    return f"""
<h2>Add New {config["title"]}</h2>

<form method="POST" action="/add">
<input type="hidden" name="category" value="{category}">
{build_form_fields(config)}
<br><br>
<button type="submit">Add {config["title"]}</button>
</form>
"""


def build_edit_form(category, row):
    config = get_config(category)

    if not row:
        return "<p>Item not found.</p>"

    return f"""
<h2>Edit {config["title"]}: {row["name"]}</h2>

<form method="POST" action="/update">
<input type="hidden" name="category" value="{category}">
{build_form_fields(config, row=row, include_original=True)}
<br><br>
<button type="submit">Save Changes</button>
</form>

<p><a href="/components">Cancel</a></p>
"""


def build_component_table(category, items):
    config = get_config(category)

    html = f"<h2>{config['title']}</h2>"
    html += build_add_form(category)
    html += "<table><tr>"

    for field in config["fields"]:
        html += f"<th>{field_label(field)}</th>"

    html += "<th>Actions</th></tr>"

    for item in items:
        row = item.__dict__
        html += "<tr>"

        for field in config["fields"]:
            html += f"<td>{row.get(field, '')}</td>"

        edit_url = f"/edit?category={quote_plus(category)}&name={quote_plus(item.name)}"

        html += "<td>"
        html += f'<a href="{edit_url}">Edit</a> '
        html += f"""
<form style="display:inline;" method="POST" action="/delete">
<input type="hidden" name="category" value="{category}">
<input type="hidden" name="name" value="{item.name}">
<button type="submit">Delete</button>
</form>
"""
        html += "</td></tr>"

    html += "</table>"
    return html


def build_options(items, include_none=True, selected_name=None):
    html = ""

    if include_none:
        selected = "selected" if selected_name in [None, "", "None"] else ""
        html += f'<option value="None" {selected}>None</option>'

    for item in items:
        selected = "selected" if item.name == selected_name else ""
        html += f'<option value="{item.name}" {selected}>{item.name}</option>'

    return html


def get_selected_line(selected_items, index):
    if not selected_items or index >= len(selected_items):
        return {"name": "None", "quantity": 0}

    return selected_items[index]


def build_line_item_rows(items, field_prefix, default_rows=3, selected_items=None):
    html = ""

    for i in range(default_rows):
        selected_line = get_selected_line(selected_items, i)
        selected_name = selected_line.get("name", "None")
        selected_qty = selected_line.get("quantity", 0)

        html += "<div style='margin-bottom: 10px;'>"
        html += f"<select name='{field_prefix}_name_{i}'>"
        html += build_options(items, selected_name=selected_name)
        html += "</select>"
        html += f"<input style='width: 100px; margin-left: 10px;' type='number' name='{field_prefix}_qty_{i}' value='{selected_qty}'>"
        html += "</div>"

    return html


def parse_multi_lines(form, prefix, max_rows=3):
    lines = []

    for i in range(max_rows):
        name = form.get(f"{prefix}_name_{i}", ["None"])[0]
        quantity = int(form.get(f"{prefix}_qty_{i}", ["0"])[0])

        if name != "None" and quantity > 0:
            lines.append({
                "name": name,
                "quantity": quantity
            })

    return lines


def parse_branches(form):
    branch_count = int(form.get("branch_count", ["1"])[0])
    branches = []

    for branch_index in range(1, branch_count + 1):
        exists = form.get(
            f"branch_{branch_index}_exists",
            ["no"]
        )[0] == "yes"

        if not exists:
            continue

        active = form.get(
            f"branch_{branch_index}_active",
            ["off"]
        )[0] == "on"

        devices = []

        for device_index in range(1, MAX_DEVICES_PER_BRANCH + 1):

            device_name = form.get(
                f"branch_{branch_index}_device_{device_index}_name",
                ["None"]
            )[0]

            quantity = int(
                form.get(
                    f"branch_{branch_index}_device_{device_index}_qty",
                    ["0"]
                )[0]
            )

            if device_name != "None" and quantity > 0:
                devices.append({
                    "name": device_name,
                    "quantity": quantity
                })

        branch = {
            "branch_number": branch_index,

            "active": active,

            "role": form.get(
                f"branch_{branch_index}_role",
                ["first_line"]
            )[0],

            "priority": int(
                form.get(
                    f"branch_{branch_index}_priority",
                    ["2"]
                )[0]
            ),

            "pipe_name": form.get(
                f"branch_{branch_index}_pipe_name",
                ["None"]
            )[0],

            "pipe_length_ft": float(
                form.get(
                    f"branch_{branch_index}_pipe_length_ft",
                    ["0"]
                )[0]
            ),

            "elevation_change_ft": float(
                form.get(
                    f"branch_{branch_index}_elevation_change_ft",
                    ["0"]
                )[0]
            ),

            "elbow_90_qty": int(
                form.get(
                    f"branch_{branch_index}_elbow_90_qty",
                    ["0"]
                )[0]
            ),

            "elbow_45_qty": int(
                form.get(
                    f"branch_{branch_index}_elbow_45_qty",
                    ["0"]
                )[0]
            ),

            "sweep_bend_qty": int(
                form.get(
                    f"branch_{branch_index}_sweep_bend_qty",
                    ["0"]
                )[0]
            ),

            "tee_qty": int(
                form.get(
                    f"branch_{branch_index}_tee_qty",
                    ["0"]
                )[0]
            ),

            "valve_qty": int(
                form.get(
                    f"branch_{branch_index}_valve_qty",
                    ["0"]
                )[0]
            ),

            "other_equivalent_length_ft": float(
                form.get(
                    f"branch_{branch_index}_other_equivalent_length_ft",
                    ["0"]
                )[0]
            ),

            "devices": devices
        }

        branches.append(branch)

    return branches


def get_branch(initial_data, branch_index):
    branches = []

    if initial_data:
        branches = initial_data.get("branches", [])

    for branch in branches:
        if int(branch.get("branch_number", 0)) == branch_index:
            return branch

    return None


def selected_attr(value, target):
    return "selected" if str(value) == str(target) else ""


def build_branch_box(library, branch_index, initial_data=None):

    branch = get_branch(initial_data, branch_index)

    active = branch.get("active", True) if branch else True

    role = branch.get("role", "first_line") if branch else "first_line"

    priority = branch.get("priority", 2) if branch else 2

    pipe_name = branch.get("pipe_name", "None") if branch else "None"

    pipe_length = branch.get("pipe_length_ft", 0) if branch else 0

    elevation = branch.get("elevation_change_ft", 0) if branch else 0

    elbow_90_qty = branch.get("elbow_90_qty", 0) if branch else 0

    elbow_45_qty = branch.get("elbow_45_qty", 0) if branch else 0

    sweep_bend_qty = branch.get("sweep_bend_qty", 0) if branch else 0

    tee_qty = branch.get("tee_qty", 0) if branch else 0

    valve_qty = branch.get("valve_qty", 0) if branch else 0

    other_equivalent_length_ft = (
        branch.get("other_equivalent_length_ft", 0)
        if branch else 0
    )

    devices = branch.get("devices", []) if branch else []

    checked = "checked" if active else ""

    html = f"""
<div class="branch-box"
     id="branch_box_{branch_index}"
     data-branch-index="{branch_index}">

<input type="hidden"
       name="branch_{branch_index}_exists"
       value="yes">

<h3>Manifold Port / Branch {branch_index}</h3>

<label>
<input style="width: auto;"
       type="checkbox"
       name="branch_{branch_index}_active"
       {checked}>
Active Branch
</label>

<label>Branch Role</label>

<select name="branch_{branch_index}_role">

<option value="first_line"
{selected_attr(role, "first_line")}>
First Line Defense / Property Hydration
</option>

<option value="last_line"
{selected_attr(role, "last_line")}>
Last Line Defense
</option>

<option value="structure_eaves"
{selected_attr(role, "structure_eaves")}>
Structure / Eaves High Pressure
</option>

<option value="foam"
{selected_attr(role, "foam")}>
Foam Deployment
</option>

<option value="manual_hose"
{selected_attr(role, "manual_hose")}>
Manual / Firefighter Hose
</option>

<option value="auxiliary"
{selected_attr(role, "auxiliary")}>
Auxiliary
</option>

</select>

<label>Priority</label>

<select name="branch_{branch_index}_priority">

<option value="1"
{selected_attr(priority, 1)}>
1 Critical
</option>

<option value="2"
{selected_attr(priority, 2)}>
2 Standard
</option>

<option value="3"
{selected_attr(priority, 3)}>
3 Auxiliary
</option>

</select>

<label>Branch Pipe Size</label>

<select name="branch_{branch_index}_pipe_name">
{build_options(library["pipes"], selected_name=pipe_name)}
</select>

<label>Branch Pipe Length (ft)</label>

<input type="number"
       name="branch_{branch_index}_pipe_length_ft"
       value="{pipe_length}">

<label>Branch Elevation Change (ft)</label>

<input type="number"
       name="branch_{branch_index}_elevation_change_ft"
       value="{elevation}">

<hr>

<h4>Fittings / Equivalent Length</h4>

<label>90° Elbows</label>

<input type="number"
       name="branch_{branch_index}_elbow_90_qty"
       value="{elbow_90_qty}"
       min="0">

<label>45° Elbows</label>

<input type="number"
       name="branch_{branch_index}_elbow_45_qty"
       value="{elbow_45_qty}"
       min="0">

<label>Sweep / Flex Bends</label>

<input type="number"
       name="branch_{branch_index}_sweep_bend_qty"
       value="{sweep_bend_qty}"
       min="0">

<label>Tees</label>

<input type="number"
       name="branch_{branch_index}_tee_qty"
       value="{tee_qty}"
       min="0">

<label>Valves</label>

<input type="number"
       name="branch_{branch_index}_valve_qty"
       value="{valve_qty}"
       min="0">

<label>Other Equivalent Length (ft)</label>

<input type="number"
       step="0.1"
       name="branch_{branch_index}_other_equivalent_length_ft"
       value="{other_equivalent_length_ft}"
       min="0">

<h4>Devices on Branch {branch_index}</h4>
"""

    for device_index in range(1, MAX_DEVICES_PER_BRANCH + 1):

        selected_line = get_selected_line(
            devices,
            device_index - 1
        )

        selected_device = selected_line.get(
            "name",
            "None"
        )

        selected_qty = selected_line.get(
            "quantity",
            0
        )

        html += f"""
<div style="margin-bottom: 10px;">

<select name="branch_{branch_index}_device_{device_index}_name">

{build_options(
    library["devices"],
    selected_name=selected_device
)}

</select>

<input style="width: 100px; margin-left: 10px;"
       type="number"
       name="branch_{branch_index}_device_{device_index}_qty"
       value="{selected_qty}">

</div>
"""

    html += f"""
<button type="button"
        class="remove-branch-button"
        onclick="removeBranch({branch_index})">

Remove Branch

</button>

</div>
"""

    return html


def build_branch_inputs(library, initial_data=None):
    branches = initial_data.get("branches", []) if initial_data else []

    if branches:
        branch_numbers = [
            int(branch.get("branch_number", index + 1))
            for index, branch in enumerate(branches)
        ]
    else:
        branch_numbers = [1]

    html = """
<div id="branches_container">
"""

    for branch_number in branch_numbers:
        html += build_branch_box(library, branch_number, initial_data)

    html += """
</div>
<button type="button" onclick="addBranch()">+ Add Branch</button>
"""

    return html


def build_branch_template(library):
    template = build_branch_box(library, "__INDEX__", None)
    template = template.replace("\n", "")
    template = template.replace("'", "\\'")
    return template


def build_export_links(export_paths):
    if not export_paths:
        return ""

    return f"""
<h2>Exports</h2>
<p>
    <a href="{export_paths['report']}">Download TXT Report</a><br>
    <a href="{export_paths['bom']}">Download BOM CSV</a><br>
    <a href="{export_paths['branches']}">Download Branch Results CSV</a><br>
    <a href="{export_paths['modes']}">Download Operating Modes CSV</a>
</p>
"""










def build_results_html(result, export_paths=None):
    primary = result["primary"]
    design_maturity = result.get("design_maturity", {})
    engineering_recommendations = result.get("engineering_recommendations", {})
    optimizer_result = result.get("optimizer_result", {})
    manifold = primary["manifold"]
    
    html = "<div class='result'>"

    if optimizer_result:
        summary = optimizer_result.get("summary", {})
        history = optimizer_result.get("history", [])

        html += build_optimizer_recommendation_html(optimizer_result)
        html += build_optimizer_explanation_html(optimizer_result)

        html += "<h2>Evolutionary Optimizer Result</h2>"
        html += "<p>The optimizer ran against this live System Builder design and searched for stronger hydraulic candidates.</p>"

        html += "<table>"
        html += "<tr><th>Metric</th><th>Value</th></tr>"

        for key, value in summary.items():
            html += f"<tr><td>{key}</td><td>{value}</td></tr>"

        html += "</table>"

        html += "<h3>Optimizer Generation History</h3>"
        html += "<table>"
        html += """
<tr>
<th>Generation</th>
<th>Best Score</th>
<th>Best Seen</th>
<th>Stagnant Generations</th>
<th>Mutation Scale</th>
<th>Best Pump</th>
<th>Best Branch</th>
</tr>
"""

        for row in history:
            candidate = row.get("best_candidate", {}) or {}
            opt_primary = candidate.get("primary", {}) or {}
            branches = opt_primary.get("branches", []) or []
            branch = branches[0] if branches else {}

            html += "<tr>"
            html += f"<td>{row.get('generation')}</td>"
            html += f"<td>{row.get('best_score')}</td>"
            html += f"<td>{row.get('best_score_seen')}</td>"
            html += f"<td>{row.get('stagnant_generations')}</td>"
            html += f"<td>{row.get('mutation_scale')}</td>"
            html += f"<td>{opt_primary.get('pump', {})}</td>"
            html += f"<td>{branch}</td>"
            html += "</tr>"

        html += "</table>"
    html += build_overall_readiness_banner_html(primary)
    html += "<h2>Primary System Result</h2>"
    html += f"<p><strong>System Passed:</strong> {primary['summary']['system_passed']}</p>"
    html += build_design_maturity_html(design_maturity)
    html += build_engineering_recommendations_html(engineering_recommendations)

    auto_selected = primary.get("auto_selected", {})

    if primary["pump"]:
        auto_text = ""

        if auto_selected.get("pump"):
            auto_text = " (Auto Selected)"

        html += f"<p><strong>Selected Pump:</strong> {primary['pump'].name}{auto_text}</p>"
        html += f"<p><strong>Pump Inlet:</strong> {primary['pump'].inlet_size_in} in</p>"
        html += f"<p><strong>Pump Outlet:</strong> {primary['pump'].outlet_size_in} in</p>"

    html += f"<p><strong>Active Branches:</strong> {manifold['active_branch_count']}</p>"
    html += f"<p><strong>Max Simultaneous Ports:</strong> {manifold['max_simultaneous_ports']}</p>"
    html += f"<p><strong>Total Installed Flow:</strong> {manifold['total_installed_flow_gpm']:.2f} GPM</p>"
    html += f"<p><strong>Active Operating Flow:</strong> {manifold['total_flow_gpm']:.2f} GPM</p>"
    html += f"<p><strong>Pump Operating Pressure:</strong> {manifold.get('pump_operating_pressure_psi', 0):.2f} PSI</p>"
    html += f"<p><strong>Pump Flow Utilization:</strong> {manifold.get('pump_flow_utilization_fraction', 0) * 100:.1f}%</p>"
    html += f"<p><strong>Runtime:</strong> {primary['runtime']['runtime_minutes']:.2f} minutes</p>"
    html += f"<p><strong>Total Cost:</strong> ${primary['cost']['total_cost']:.2f}</p>"
    html += f"<p><strong>Within Budget:</strong> {primary['summary']['within_budget']}</p>"

    html += build_guided_builder_summary_html(primary)
    html += build_auto_select_summary_html(primary)
    html += build_design_direction_html(primary)
    html += build_design_readiness_html(primary)
    html += build_constraint_violation_html(primary)
    html += build_section_readiness_html(primary)
    html += build_architecture_recommendations_html(primary)
    html += build_bottleneck_intelligence_html(primary)
    html += build_scenario_comparison_html(primary)
    html += build_system_curve_overlay_html(primary)
    html += build_hydraulic_intelligence_html(primary)
    html += build_hydraulic_optimizer_html(primary)

    html += "<h2>Warnings</h2>"

    if primary["summary"]["warnings"]:
        html += "<ul>"
        for warning in primary["summary"]["warnings"]:
            html += f"<li>{warning}</li>"
        html += "</ul>"
    else:
        html += "<p>No warnings.</p>"

    html += build_branch_results_html(manifold)

    html += build_operating_modes_html(manifold)

    html += build_selected_components_html(primary)

    html += build_storage_power_html(primary)
    html += "</div>"

    return html


def build_page(title, body, branch_template=""):
    return f"""
<!DOCTYPE html>
<html>
<head>
<title>{title}</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 40px; max-width: 1500px; }}
label {{ display: block; margin-top: 12px; font-weight: bold; }}
input, select {{ width: 420px; padding: 8px; margin-top: 4px; }}
button {{ padding: 8px 12px; margin-top: 8px; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 15px; margin-bottom: 50px; }}
td, th {{ border: 1px solid #ccc; padding: 8px; text-align: left; vertical-align: top; }}
th {{ background: #eee; }}
.message {{ background: #e8f5e9; padding: 12px; border: 1px solid #999; margin-bottom: 20px; }}
.result {{ margin-top: 30px; padding: 20px; border: 1px solid #ccc; background: #f7f7f7; }}
.section {{ margin-top: 30px; padding-top: 10px; border-top: 2px solid #ddd; }}
.branch-box {{ border: 1px solid #ccc; padding: 18px; margin: 20px 0; background: #fafafa; }}
.remove-branch-button {{ background: #eee; }}
.field-suggestion {{
    margin: 10px 0 18px 0;
    padding: 12px;
    border-radius: 8px;
    border: 1px solid #ccc;
    font-size: 14px;
}}

.suggestion-header {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 15px;
}}

.suggestion-icon {{
    font-size: 20px;
}}

.suggestion-green {{
    background: #eef8ee;
    border-color: #3c9b3c;
    color: #145c14;
}}

.suggestion-yellow {{
    background: #fff8e6;
    border-color: #d99a00;
    color: #7a5200;
}}

.suggestion-red {{
    background: #fdecec;
    border-color: #c62828;
    color: #8a1111;
}}

.accept-suggestion-button {{
    margin-top: 8px;
    padding: 8px 12px;
    border-radius: 6px;
    border: 1px solid #2f7d32;
    background: white;
    color: #2f7d32;
    font-weight: bold;
    cursor: pointer;
}}

.accept-suggestion-button:hover {{
    background: #eef8ee;
}}
</style>
<script>
let nextBranchIndex = 1;

function syncBranchCount() {{
    const boxes = document.querySelectorAll(".branch-box");
    let maxIndex = 0;

    boxes.forEach(function(box) {{
        const index = parseInt(box.getAttribute("data-branch-index"));
        if (index > maxIndex) {{
            maxIndex = index;
        }}
    }});

    const branchCount = document.getElementById("branch_count");
    if (branchCount) {{
        branchCount.value = maxIndex;
    }}

    nextBranchIndex = maxIndex + 1;
}}

function addBranch() {{
    syncBranchCount();

    const container = document.getElementById("branches_container");
    let template = '{branch_template}';
    template = template.replaceAll("__INDEX__", nextBranchIndex);

    container.insertAdjacentHTML("beforeend", template);
    syncBranchCount();
}}

function removeBranch(index) {{
    const box = document.getElementById("branch_box_" + index);
    if (box) {{
        box.remove();
    }}
    syncBranchCount();
}}

document.addEventListener("DOMContentLoaded", function() {{
    syncBranchCount();
}});
</script>
</head>
<body>
<h1>{title}</h1>
{build_nav()}
{body}
</body>
</html>
"""

def get_section_class(initial_data, section_key):
    section_statuses = initial_data.get("section_statuses", {})

    status = section_statuses.get(section_key, "")

    if not status:
        if section_key == "system_drive":
            has_pump = initial_data.get("pump_name", "None") not in ["None", ""]
            has_engine = initial_data.get("engine_name", "None") not in ["None", ""]
            has_motor = initial_data.get("motor_name", "None") not in ["None", ""]

            if has_pump and (has_engine or has_motor):
                status = "green"
            elif has_pump or has_engine or has_motor:
                status = "yellow"
            else:
                status = "red"

        elif section_key == "water_runtime":
            has_water = initial_data.get("water_storage_name", "None") not in ["None", ""]
            has_available_water = float(initial_data.get("available_water_gallons", 0) or 0) > 0
            has_runtime = float(initial_data.get("required_runtime_minutes", 0) or 0) > 0

            if has_water and has_available_water and has_runtime:
                status = "green"
            elif has_available_water or has_runtime:
                status = "yellow"
            else:
                status = "red"

        elif section_key == "manifold_branches":
            branches = initial_data.get("branches", [])
            active_branches = [branch for branch in branches if branch.get("active")]

            if active_branches:
                status = "green"
            elif branches:
                status = "yellow"
            else:
                status = "red"

        elif section_key == "controls":
            if initial_data.get("selected_controls"):
                status = "green"
            else:
                status = "yellow"

        elif section_key == "sensors":
            if initial_data.get("selected_sensors"):
                status = "green"
            else:
                status = "yellow"

        elif section_key == "budget":
            budget = float(initial_data.get("max_budget", 0) or 0)

            if budget >= 100000:
                status = "green"
            elif budget > 0:
                status = "yellow"
            else:
                status = "red"

    if status == "green":
        return "section section-green"

    if status == "yellow":
        return "section section-yellow"

    if status == "red":
        return "section section-red"

    return "section"


def build_section_update_button(section_key):
    labels = {
        "system_drive": "Update Drive Suggestions",
        "water_runtime": "Update Water Suggestions",
        "manifold_branches": "Update Branch Suggestions",
        "controls": "Update Control Suggestions",
        "sensors": "Update Sensor Suggestions",
        "budget": "Update Budget Suggestion",
    }

    label = labels.get(section_key, "Update This Section")

    return f"""
    <button
        type="submit"
        name="update_section"
        value="{section_key}"
        class="section-update-button"
    >
        {label}
    </button>
    """

def build_field_suggestion_html(builder_suggestions, field_name):
    suggestion = builder_suggestions.get(field_name, {})

    if not suggestion:
        return ""

    suggested_value = suggestion.get("suggested_value", "")
    confidence = suggestion.get("confidence", "red")
    reason = suggestion.get("reason", "")

    confidence_labels = {
        "green": "High Confidence",
        "yellow": "Medium Confidence",
        "red": "Low Confidence",
    }

    confidence_icons = {
        "green": "✅",
        "yellow": "⚠️",
        "red": "❌",
    }

    confidence_label = confidence_labels.get(confidence, "Unknown Confidence")
    confidence_icon = confidence_icons.get(confidence, "❔")

    if not suggested_value:
        return f"""
        <div class="field-suggestion suggestion-{confidence}">
            <div class="suggestion-header">
                <span class="suggestion-icon">{confidence_icon}</span>
                <strong>No suggestion yet</strong>
            </div>
            <p><strong>{confidence_label}</strong></p>
            <p>{reason}</p>
        </div>
        """

    return f"""
    <div class="field-suggestion suggestion-{confidence}">
        <div class="suggestion-header">
            <span class="suggestion-icon">{confidence_icon}</span>
            <strong>Suggested:</strong> {suggested_value}
        </div>

        <p><strong>{confidence_label}</strong></p>
        <p>{reason}</p>

        <button
            type="submit"
            name="accept_suggestion"
            value="{field_name}:{suggested_value}"
            class="accept-suggestion-button"
        >
            Accept Suggestion
        </button>
    </div>
    """


def build_system_builder_page(results="", initial_data=None):
    library = get_component_library()

    if initial_data is None:
        initial_data = {}

    branches = initial_data.get("branches", [])

    builder_suggestions = initial_data.get(
        "builder_suggestions",
        {}
    )

    branch_count = max(
        [int(b.get("branch_number", 1)) for b in branches],
        default=1
    )

    branch_template = build_branch_template(library)

    last_updated_section = initial_data.get(
        "last_updated_section",
        ""
    )

    section_update_changes = initial_data.get(
        "section_update_changes",
        []
    )

    update_message = ""

    if last_updated_section:
        changes_html = ""

        if section_update_changes:
            changes_html = "<ul>"

            for change in section_update_changes:
                changes_html += f"<li>{change}</li>"

            changes_html += "</ul>"

        update_message = f"""
        <div class="section section-yellow">
            <h2>Section Update Applied</h2>
            <p>Updated section: <strong>{last_updated_section}</strong></p>
            {changes_html}
        </div>
        """

    body = build_system_builder_page_html(
        library=library,
        initial_data=initial_data,
        results=results,
        branch_template=branch_template,
        branch_count=branch_count,
        update_message=update_message,
        builder_suggestions=builder_suggestions,
        get_section_class=get_section_class,
        build_section_update_button=build_section_update_button,
        build_field_suggestion_html=build_field_suggestion_html,
        build_options=build_options,
        build_branch_inputs=build_branch_inputs,
        build_line_item_rows=build_line_item_rows,
    )

    return build_page(
        "FLD Operating Mode System Builder V2.7",
        body,
        branch_template
    )


def build_component_manager_page(message=""):
    library = get_component_library()
    body = ""

    if message:
        body += f'<div class="message">{message}</div>'

    for category in COMPONENT_CONFIG.keys():
        body += build_component_table(category, library.get(category, []))

    return build_page("FLD Component Manager V2.7", body)


def build_edit_page(category, item_name):
    row = get_row(category, item_name)
    config = get_config(category)
    body = build_edit_form(category, row)

    return build_page(f"Edit {config['title']}", body)


class FLDRequestHandler(BaseHTTPRequestHandler):

    def send_html(self, page):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(page.encode("utf-8"))

    def serve_export_file(self):
        requested_path = unquote_plus(self.path.replace("/exports/", ""))
        safe_name = os.path.basename(requested_path)
        file_path = os.path.join(EXPORT_DIR, safe_name)

        if not os.path.exists(file_path):
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Export file not found.")
            return

        content_type = "text/csv" if file_path.endswith(".csv") else "text/plain"

        with open(file_path, "rb") as f:
            data = f.read()

        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.send_header("Content-Disposition", f'attachment; filename="{safe_name}"')
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path.startswith("/exports/"):
            self.serve_export_file()
            return

        if self.path.startswith("/edit"):
            query = self.path.split("?", 1)[1] if "?" in self.path else ""
            params = parse_qs(query)

            category = unquote_plus(params.get("category", [""])[0])
            item_name = unquote_plus(params.get("name", [""])[0])

            page = build_edit_page(category, item_name)

        elif self.path == "/components":
            page = build_component_manager_page()

        else:
            page = build_system_builder_page()

        self.send_html(page)

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        form = parse_qs(post_data)
        update_section = form.get("update_section", [""])[0]
        accept_suggestion = form.get("accept_suggestion", [""])[0]

        if self.path == "/add":
            category = form.get("category", [""])[0]
            name = add_row(category, form)
            page = build_component_manager_page(f"Added {name}")
            self.send_html(page)
            return

        if self.path == "/update":
            category = form.get("category", [""])[0]
            original_name = form.get("original_name", [""])[0]
            update_row(category, original_name, form)
            updated_name = form.get("name", [original_name])[0]
            page = build_component_manager_page(f"Updated {updated_name}")
            self.send_html(page)
            return

        if self.path == "/delete":
            category = form.get("category", [""])[0]
            name = form.get("name", [""])[0]
            delete_row(category, name)
            page = build_component_manager_page(f"Deleted {name}")
            self.send_html(page)
            return

        if self.path == "/auto_update":

            action_code = form.get("action_code", [""])[0]

            selected_control_lines = parse_multi_lines(form, "control", 3)
            selected_sensor_lines = parse_multi_lines(form, "sensor", 5)

            branches = parse_branches(form)

            input_data = {
                "branches": branches,
                "selected_controls": selected_control_lines,
                "selected_sensors": selected_sensor_lines,
                "pump_name": form.get("pump_name", ["Auto Select"])[0],
                "water_storage_name": form.get("water_storage_name", ["None"])[0],
                "fuel_storage_name": form.get("fuel_storage_name", ["None"])[0],
                "battery_name": form.get("battery_name", ["None"])[0],
                "generator_name": form.get("generator_name", ["None"])[0],
                "engine_name": form.get("engine_name", ["None"])[0],
                "budget": float(form.get("budget", [0])[0] or 0),
                "max_simultaneous_ports": int(
                    form.get("max_simultaneous_ports", [1])[0] or 1
                ),
            }

            auto_update_result = run_auto_update(
                input_data=input_data,
                action_code=action_code
            )

            updated_result = auto_update_result["result"]

            export_paths = write_export_files(
                input_data,
                updated_result
            )

            results_html = build_results_html(
                updated_result,
                export_paths
            )

            page = build_system_builder_page(
                results_html,
                input_data
            )

            self.send_html(page)
            return

        selected_control_lines = parse_multi_lines(form, "control", 3)
        selected_sensor_lines = parse_multi_lines(form, "sensor", 5)
        branches = parse_branches(form)

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

        if accept_suggestion:
            field_name, suggested_value = accept_suggestion.split(":", 1)
            input_data[field_name] = suggested_value
            input_data["last_updated_section"] = field_name
            input_data["section_update_changes"] = [
                f"Accepted suggestion for {field_name}: {suggested_value}"
            ]

        if update_section:
            input_data = apply_section_update_recommendation(
                input_data,
                update_section
            )


        result = run_system(input_data)

        input_data["builder_suggestions"] = result.get(
            "builder_suggestions",
            {}
        )

        export_paths = write_export_files(input_data, result)
        results_html = build_results_html(result, export_paths)
        page = build_system_builder_page(results_html, input_data)

        self.send_html(page)


def run_web_app():
    server_address = ("localhost", PORT)
    httpd = HTTPServer(server_address, FLDRequestHandler)

    print("FLD System Builder web app running.")
    print("Open this in your browser:")
    print(f"http://localhost:{PORT}")

    httpd.serve_forever()


if __name__ == "__main__":
    run_web_app()
