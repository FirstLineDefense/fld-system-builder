def build_hydraulic_intelligence_html(primary):
    intelligence = primary.get("hydraulic_intelligence", {})

    html = "<h2>Hydraulic Intelligence</h2>"

    html += (
        f"<p><strong>Hydraulic Health:</strong> "
        f"{intelligence.get('health', 'Not Available')}</p>"
    )

    html += (
        f"<p><strong>Critical:</strong> "
        f"{intelligence.get('critical_count', 0)} | "
    )

    html += (
        f"<strong>Warnings:</strong> "
        f"{intelligence.get('warning_count', 0)} | "
    )

    html += (
        f"<strong>Info:</strong> "
        f"{intelligence.get('info_count', 0)}</p>"
    )

    html += "<h3>Priority Recommendations</h3>"
    html += "<table>"
    html += (
        "<tr>"
        "<th>Priority</th>"
        "<th>Title</th>"
        "<th>Recommendation</th>"
        "</tr>"
    )

    for item in intelligence.get("priority_recommendations", []):
        html += "<tr>"
        html += f"<td>{item['priority']}</td>"
        html += f"<td>{item['title']}</td>"
        html += f"<td>{item['recommendation']}</td>"
        html += "</tr>"

    html += "</table>"

    html += "<h3>Pipe Recommendations</h3>"
    html += "<table>"

    html += (
        "<tr>"
        "<th>Branch</th>"
        "<th>Current Pipe</th>"
        "<th>Recommended Pipe</th>"
        "<th>Reason</th>"
        "<th>Estimated Velocity</th>"
        "</tr>"
    )

    pipe_recs = intelligence.get("pipe_recommendations", [])

    if pipe_recs:
        for item in pipe_recs:
            html += "<tr>"
            html += f"<td>{item['branch_number']}</td>"
            html += f"<td>{item['current_pipe']}</td>"
            html += f"<td>{item['recommended_pipe']}</td>"
            html += f"<td>{item['reason']}</td>"
            html += (
                f"<td>{item['estimated_velocity_fps']:.2f} ft/s</td>"
            )
            html += "</tr>"
    else:
        html += (
            "<tr>"
            "<td colspan='5'>"
            "No pipe recommendations generated."
            "</td>"
            "</tr>"
        )

    html += "</table>"

    html += "<h3>Staging Recommendations</h3>"
    html += "<table>"
    html += "<tr><th>Title</th><th>Recommendation</th></tr>"

    for item in intelligence.get("staging_recommendations", []):
        html += "<tr>"
        html += f"<td>{item['title']}</td>"
        html += f"<td>{item['recommendation']}</td>"
        html += "</tr>"

    html += "</table>"

    html += "<h3>Branch Split Recommendations</h3>"
    html += "<table>"

    html += (
        "<tr>"
        "<th>Branch</th>"
        "<th>Reason</th>"
        "<th>Recommendation</th>"
        "</tr>"
    )

    split_recs = intelligence.get(
        "branch_split_recommendations",
        []
    )

    if split_recs:
        for item in split_recs:
            html += "<tr>"
            html += f"<td>{item['branch_number']}</td>"
            html += f"<td>{item['reason']}</td>"
            html += f"<td>{item['recommendation']}</td>"
            html += "</tr>"
    else:
        html += (
            "<tr>"
            "<td colspan='3'>"
            "No branch split recommendations generated."
            "</td>"
            "</tr>"
        )

    html += "</table>"

    html += "<h3>Hydraulic Warnings</h3>"
    html += "<table>"

    html += (
        "<tr>"
        "<th>Severity</th>"
        "<th>Category</th>"
        "<th>Message</th>"
        "<th>Recommendation</th>"
        "</tr>"
    )

    for item in intelligence.get("warnings", []):
        html += "<tr>"
        html += f"<td>{item['severity']}</td>"
        html += f"<td>{item['category']}</td>"
        html += f"<td>{item['message']}</td>"
        html += f"<td>{item['recommendation']}</td>"
        html += "</tr>"

    html += "</table>"

    html += "<h3>Branch Velocity Check</h3>"
    html += "<table>"

    html += (
        "<tr>"
        "<th>Branch</th>"
        "<th>Velocity ft/s</th>"
        "<th>Flow GPM</th>"
        "<th>Pressure Margin PSI</th>"
        "</tr>"
    )

    for branch in intelligence.get("branch_analyses", []):
        html += "<tr>"
        html += f"<td>{branch['branch_number']}</td>"
        html += f"<td>{branch['velocity_fps']:.2f}</td>"
        html += f"<td>{branch['flow_gpm']:.2f}</td>"
        html += (
            f"<td>{branch['pressure_margin_psi']:.2f}</td>"
        )
        html += "</tr>"

    html += "</table>"

    return html
