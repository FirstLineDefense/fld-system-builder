def build_architecture_recommendations_html(primary):
    architecture = primary.get("architecture_recommendations", {})
    recommendations = architecture.get("recommendations", [])

    if not recommendations:
        return ""

    html = "<h2>Architecture Recommendations</h2>"
    html += "<table>"
    html += "<tr><th>Priority</th><th>Category</th><th>Title</th><th>Recommendation</th><th>Reasoning</th></tr>"

    for item in recommendations:
        reasoning = item.get("reasoning", [])
        reasoning_html = "<br>".join(reasoning)

        html += "<tr>"
        html += f"<td>{item.get('priority')}</td>"
        html += f"<td>{item.get('category')}</td>"
        html += f"<td>{item.get('title')}</td>"
        html += f"<td>{item.get('recommendation')}</td>"
        html += f"<td>{reasoning_html}</td>"
        html += "</tr>"

    html += "</table>"

    return html

