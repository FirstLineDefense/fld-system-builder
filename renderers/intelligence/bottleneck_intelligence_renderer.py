def build_bottleneck_intelligence_html(primary):
    bottleneck_data = primary.get("bottleneck_intelligence", {})
    bottlenecks = bottleneck_data.get("bottlenecks", [])

    if not bottlenecks:
        return ""

    html = "<h2>Bottleneck Intelligence</h2>"
    html += f"<p><strong>Summary:</strong> {bottleneck_data.get('summary', '')}</p>"

    html += "<table>"
    html += "<tr><th>Priority</th><th>Type</th><th>Title</th><th>Finding</th><th>Recommended Action</th><th>Evidence</th></tr>"

    for item in bottlenecks:
        evidence = item.get("evidence", [])
        evidence_html = "<br>".join(evidence)

        html += "<tr>"
        html += f"<td>{item.get('priority')}</td>"
        html += f"<td>{item.get('type')}</td>"
        html += f"<td>{item.get('title')}</td>"
        html += f"<td>{item.get('finding')}</td>"
        html += f"<td>{item.get('recommended_action')}</td>"
        html += f"<td>{evidence_html}</td>"
        html += "</tr>"

    html += "</table>"

    return html

