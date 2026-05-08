def build_design_readiness_html(primary):
    readiness = primary.get("design_readiness", {})

    if not readiness:
        return ""

    status = readiness.get("overall_status", "missing")

    status_label = {
        "ready": "READY",
        "partial": "PARTIAL",
        "missing": "MISSING"
    }.get(status, status.upper())

    html = "<h2>Design Readiness</h2>"
    html += f"<p><strong>Overall Status:</strong> {status_label}</p>"
    html += f"<p><strong>Summary:</strong> {readiness.get('summary', '')}</p>"
    html += f"<p><strong>Ready:</strong> {readiness.get('ready_count', 0)} | "
    html += f"<strong>Partial:</strong> {readiness.get('partial_count', 0)} | "
    html += f"<strong>Missing:</strong> {readiness.get('missing_count', 0)}</p>"

    html += "<table>"
    html += "<tr><th>Design Area</th><th>Status</th><th>Meaning</th><th>Missing / Needed</th></tr>"

    for item in readiness.get("items", []):
        missing = item.get("missing", [])
        missing_text = "<br>".join(missing) if missing else ""

        html += "<tr>"
        html += f"<td>{item.get('name')}</td>"
        html += f"<td>{item.get('status')}</td>"
        html += f"<td>{item.get('message')}</td>"
        html += f"<td>{missing_text}</td>"
        html += "</tr>"

    html += "</table>"

    return html

