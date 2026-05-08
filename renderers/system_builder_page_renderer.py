def build_system_builder_page_html(
    library,
    initial_data,
    results,
    branch_template,
    branch_count,
    update_message,
    builder_suggestions,
    get_section_class,
    build_section_update_button,
    build_field_suggestion_html,
    build_options,
    build_branch_inputs,
    build_line_item_rows,
):
    body = f"""
<form method="POST" action="/">

{update_message}

<div class="{get_section_class(initial_data, "system_drive")}">
<h2>System Drive</h2>
{build_section_update_button("system_drive")}

<label>Pump</label>
<select name="pump_name">
<option value="Auto Select Pump" {"selected" if initial_data.get("pump_name", "Auto Select Pump") == "Auto Select Pump" else ""}>Auto Select Pump</option>
{build_options(library["pumps"], include_none=False, selected_name=initial_data.get("pump_name", "Auto Select Pump"))}
</select>

{build_field_suggestion_html(builder_suggestions, "pump_name")}

<label>Engine</label>
<select name="engine_name">
<option value="Auto Select Engine" {"selected" if initial_data.get("engine_name", "None") == "Auto Select Engine" else ""}>Auto Select Engine</option>
{build_options(library["engines"], selected_name=initial_data.get("engine_name", "None"))}
</select>

{build_field_suggestion_html(builder_suggestions, "engine_name")}

<label>Motor</label>
<select name="motor_name">
<option value="Auto Select Motor" {"selected" if initial_data.get("motor_name", "None") == "Auto Select Motor" else ""}>Auto Select Motor</option>
{build_options(library["motors"], selected_name=initial_data.get("motor_name", "None"))}
</select>

{build_field_suggestion_html(builder_suggestions, "motor_name")}

<label>Fuel Storage</label>
<select name="fuel_storage_name">
<option value="Auto Select Fuel Storage" {"selected" if initial_data.get("fuel_storage_name", "None") == "Auto Select Fuel Storage" else ""}>Auto Select Fuel Storage</option>
{build_options(library["fuel_storage"], selected_name=initial_data.get("fuel_storage_name", "None"))}
</select>

{build_field_suggestion_html(builder_suggestions, "fuel_storage_name")}

<label>Generator</label>
<select name="generator_name">
<option value="Auto Select Generator" {"selected" if initial_data.get("generator_name", "None") == "Auto Select Generator" else ""}>Auto Select Generator</option>
{build_options(library["generators"], selected_name=initial_data.get("generator_name", "None"))}
</select>

{build_field_suggestion_html(builder_suggestions, "generator_name")}

<label>Battery</label>
<select name="battery_name">
<option value="Auto Select Battery" {"selected" if initial_data.get("battery_name", "None") == "Auto Select Battery" else ""}>Auto Select Battery</option>
{build_options(library["batteries"], selected_name=initial_data.get("battery_name", "None"))}
</select>

{build_field_suggestion_html(builder_suggestions, "battery_name")}

<div class="{get_section_class(initial_data, "water_runtime")}">
<h2>Water + Runtime</h2>
{build_section_update_button("water_runtime")}

<label>Available Water (gallons)</label>
<input type="number" name="available_water_gallons" value="{initial_data.get("available_water_gallons", 5000)}">

<label>Required Runtime (minutes)</label>
<input type="number" name="required_runtime_minutes" value="{initial_data.get("required_runtime_minutes", 60)}">

<label>Water Storage</label>
<select name="water_storage_name">
<option value="Auto Select Water Storage" {"selected" if initial_data.get("water_storage_name", "None") == "Auto Select Water Storage" else ""}>Auto Select Water Storage</option>
{build_options(library["water_storage"], selected_name=initial_data.get("water_storage_name", "None"))}
</select>

{build_field_suggestion_html(builder_suggestions, "water_storage_name")}
</div>

<div class="{get_section_class(initial_data, "manifold_branches")}">
<h2>Manifold + Branches</h2>
{build_section_update_button("manifold_branches")}

<input type="hidden" id="branch_count" name="branch_count" value="{branch_count}">

<label>Maximum Manifold Ports Intended to Run at Once</label>
<input type="number" name="max_simultaneous_ports" value="{initial_data.get("max_simultaneous_ports", 1)}">

<label>Minimum Pressure Margin (PSI)</label>
<input type="number" name="minimum_pressure_margin_psi" value="{initial_data.get("minimum_pressure_margin_psi", 20)}">

<label>Preferred Velocity Target (ft/s)</label>
<input type="number" step="0.1" name="preferred_velocity_fps" value="{initial_data.get("preferred_velocity_fps", 8)}">

<label>Maximum Velocity Warning (ft/s)</label>
<input type="number" step="0.1" name="maximum_velocity_fps" value="{initial_data.get("maximum_velocity_fps", 10)}">

{build_branch_inputs(library, initial_data)}
</div>

<div class="{get_section_class(initial_data, "controls")}">
<h2>Controls</h2>
{build_section_update_button("controls")}

{build_field_suggestion_html(
    builder_suggestions,
    "selected_controls"
)}

<p>Select up to three controls for now.</p>

{build_line_item_rows(
    library["controls"],
    "control",
    3,
    initial_data.get("selected_controls", [])
)}
</div>

<div class="{get_section_class(initial_data, "sensors")}">
<h2>Sensors</h2>
{build_section_update_button("sensors")}

{build_field_suggestion_html(
    builder_suggestions,
    "selected_sensors"
)}

<p>Select up to five sensor types for now.</p>

{build_line_item_rows(
    library["sensors"],
    "sensor",
    5,
    initial_data.get("selected_sensors", [])
)}
</div>

<div class="{get_section_class(initial_data, "budget")}">
<h2>Budget</h2>
{build_section_update_button("budget")}

<label>Max Budget ($)</label>
<input type="number" name="max_budget" value="{initial_data.get("max_budget", 4000)}">
</div>

<br>

<button type="submit">Run System Builder</button>

</form>

{results}
"""

    return body
