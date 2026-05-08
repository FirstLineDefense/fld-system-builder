def build_section_readiness_html(primary):
    readiness = primary.get("section_readiness", {})

    if not readiness:
        return ""

    html = "<h2>Section Readiness</h2>"
    html += f"<p><strong>Overall:</strong> {readiness.get('overall_status', '').upper()}</p>"

    counts = readiness.get("counts", {})
    html += f"<p><strong>Green:</strong> {counts.get('green', 0)} | "
    html += f"<strong>Yellow:</strong> {counts.get('yellow', 0)} | "
    html += f"<strong>Red:</strong> {counts.get('red', 0)}</p>"

    html += "<table>"
    html += "<tr><th>Section</th><th>Status</th><th>Summary</th><th>Suggested Next Inputs</th></tr>"

    for section in readiness.get("sections", []):
        suggestions = section.get("suggested_inputs", [])
        suggestions_html = "<br>".join(suggestions)

        status = section.get("status", "")

        status_style = ""

        if status == "green":
            status_style = "background:#d7f7d7; font-weight:bold;"
        elif status == "yellow":
            status_style = "background:#fff3bf; font-weight:bold;"
        elif status == "red":
            status_style = "background:#ffd6d6; font-weight:bold;"

        html += "<tr>"
        html += f"<td>{section.get('section')}</td>"
        html += f"<td style='{status_style}'>{status.upper()}</td>"
        html += f"<td>{section.get('summary')}</td>"
        html += f"<td>{suggestions_html}</td>"
        html += "</tr>"

    html += "</table>"

    return html

