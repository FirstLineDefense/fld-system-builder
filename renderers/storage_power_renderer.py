def build_storage_power_html(primary):
    html = "<h2>Storage / Power Checks</h2>"

    html += "<table>"

    html += (
        "<tr>"
        "<th>Check</th>"
        "<th>Status</th>"
        "<th>Details</th>"
        "</tr>"
    )

    auto_selected = primary.get("auto_selected", {})

    water = primary["water_storage_analysis"]

    water_label = "Water Storage"

    if auto_selected.get("water_storage"):
        water_label = "Water Storage (Auto Selected)"

    html += (
        f"<tr>"
        f"<td>{water_label}</td>"
        f"<td>{water['passed']}</td>"
        f"<td>"
        f"Capacity: {water['capacity_gallons']} gal | "
        f"Required: {water['required_gallons']} gal | "
        f"Margin: {water['margin_gallons']}"
        f"</td>"
        f"</tr>"
    )

    fuel = primary["fuel_runtime_analysis"]

    html += (
        f"<tr>"
        f"<td>Fuel Runtime</td>"
        f"<td>{fuel['passed']}</td>"
        f"<td>"
        f"Runtime: {fuel['runtime_hours']} hr | "
        f"Required: {fuel['required_runtime_hours']:.2f} hr"
        f"</td>"
        f"</tr>"
    )

    battery = primary["battery_runtime_analysis"]

    html += (
        f"<tr>"
        f"<td>Battery Runtime</td>"
        f"<td>{battery['passed']}</td>"
        f"<td>"
        f"Runtime: {battery['runtime_hours']} hr | "
        f"Required: {battery['required_runtime_hours']:.2f} hr | "
        f"Motor kW: {battery['motor_kw_required']}"
        f"</td>"
        f"</tr>"
    )

    generator = primary["generator_analysis"]

    html += (
        f"<tr>"
        f"<td>Generator Support</td>"
        f"<td>{generator['passed']}</td>"
        f"<td>"
        f"Generator kW: {generator['generator_kw']} | "
        f"Motor kW Required: {generator['motor_kw_required']}"
        f"</td>"
        f"</tr>"
    )

    html += "</table>"

    return html
