def build_design_direction_html(primary):
    direction = primary.get("design_direction", {})

    if not direction:
        return ""

    html = "<h2>Design Direction</h2>"
    html += f"<p><strong>Current Design Mode:</strong> {direction.get('direction', '')}</p>"
    html += f"<p><strong>Summary:</strong> {direction.get('summary', '')}</p>"
    html += f"<p><strong>Next Action:</strong> {direction.get('next_action', '')}</p>"

    missing = direction.get("missing", [])

    if missing:
        html += "<p><strong>Missing / Needed:</strong></p>"
        html += "<ul>"
        for item in missing:
            html += f"<li>{item}</li>"
        html += "</ul>"

    html += "<table>"
    html += "<tr><th>Check</th><th>Status</th></tr>"
    html += f"<tr><td>Hydraulic Demand Defined</td><td>{direction.get('has_hydraulic_demand')}</td></tr>"
    html += f"<tr><td>Pipe Layout Defined</td><td>{direction.get('has_pipe_layout')}</td></tr>"
    html += f"<tr><td>Supply Architecture Defined</td><td>{direction.get('has_supply_architecture')}</td></tr>"
    html += f"<tr><td>Runtime Target Defined</td><td>{direction.get('has_runtime_target')}</td></tr>"
    html += "</table>"

    return html

