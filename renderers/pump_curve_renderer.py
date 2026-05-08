from component_library import get_component_library
from database import list_pump_curve_points

from renderers.page_renderer import build_standalone_page
from renderers.pump_curve_components import build_curve_preview_section, build_pump_select_options


def build_pump_curve_page(message="", warning="", selected_pump_name=""):
    library = get_component_library()
    pumps = library.get("pumps", [])
    points = list_pump_curve_points()

    if not selected_pump_name and pumps:
        selected_pump_name = pumps[0].name

    body = ""

    if message:
        body += f'<div class="message">{message}</div>'

    if warning:
        body += f'<div class="warning">{warning}</div>'

    body += build_curve_preview_section(selected_pump_name)

    body += """
<h2>Add Single Pump Curve Point</h2>
<p>Add one real manufacturer or field-tested pump curve point.</p>

<form method="POST" action="/pump-curves/add">

<label>Pump</label>
<select name="pump_name">
"""

    body += build_pump_select_options(pumps, selected_pump_name)

    body += """
</select>

<label>Flow GPM</label>
<input type="number" step="0.01" name="flow_gpm" required>

<label>Pressure PSI</label>
<input type="number" step="0.01" name="pressure_psi" required>

<label>Notes</label>
<textarea name="notes"></textarea>

<br>
<button type="submit">Add Curve Point</button>
</form>

<h2>Bulk Import Pump Curve Points</h2>
<p>Paste multiple pump curve points at once. Use one row per point.</p>

<div class="codehint">
flow_gpm, pressure_psi<br>
0, 120<br>
50, 110<br>
100, 95<br>
150, 70<br>
200, 45
</div>

<form method="POST" action="/pump-curves/bulk-import">

<label>Pump</label>
<select name="pump_name">
"""

    body += build_pump_select_options(pumps, selected_pump_name)

    body += """
</select>

<label>
<input style="width:auto;" type="checkbox" name="clear_existing" value="yes">
Clear existing curve points for this pump before importing
</label>

<label>Bulk Curve Data</label>
<textarea name="bulk_curve_data" style="height:180px;" required></textarea>

<br>
<button type="submit">Import Curve Points</button>
</form>

<h2>Curve Validation + Export</h2>

<form method="POST" action="/pump-curves/validate">

<label>Pump</label>
<select name="pump_name">
"""

    body += build_pump_select_options(pumps, selected_pump_name)

    body += """
</select>

<br>
<button type="submit">Validate Pump Curve</button>
</form>

<form method="POST" action="/pump-curves/export">

<label>Pump</label>
<select name="pump_name">
"""

    body += build_pump_select_options(pumps, selected_pump_name)

    body += """
</select>

<br>
<button type="submit">Export Curve CSV</button>
</form>

<h2>Saved Pump Curve Points</h2>
<table>
<tr>
<th>ID</th>
<th>Pump</th>
<th>Flow GPM</th>
<th>Pressure PSI</th>
<th>Notes</th>
<th>Actions</th>
</tr>
"""

    if points:
        for point in points:
            body += "<tr>"
            body += f"<td>{point['id']}</td>"
            body += f"<td>{point['pump_name']}</td>"
            body += f"<td>{point['flow_gpm']:.2f}</td>"
            body += f"<td>{point['pressure_psi']:.2f}</td>"
            body += f"<td>{point['notes']}</td>"
            body += f"""
<td>
<form style="display:inline;" method="POST" action="/pump-curves/delete">
<input type="hidden" name="point_id" value="{point['id']}">
<button type="submit">Delete</button>
</form>
</td>
"""
            body += "</tr>"
    else:
        body += "<tr><td colspan='6'>No pump curve points saved yet.</td></tr>"

    body += "</table>"

    body += """
<h2>Clear Curve Points For Pump</h2>
<form method="POST" action="/pump-curves/clear">

<label>Pump</label>
<select name="pump_name">
"""

    body += build_pump_select_options(pumps, selected_pump_name)

    body += """
</select>

<br>
<button type="submit">Clear This Pump Curve</button>
</form>
"""

    return build_standalone_page("FLD Pump Curve Manager", body)
