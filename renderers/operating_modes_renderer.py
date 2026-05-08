def build_operating_modes_html(manifold):
    modes = manifold["operating_modes"]["modes"]

    html = "<h2>Operating Mode Checks</h2>"
    html += "<table>"

    html += """
<tr>
<th>Mode</th>
<th>Passed</th>
<th>Branches</th>
<th>Total Flow</th>
<th>Pump PSI</th>
<th>Pump Utilization</th>
<th>Worst Branch</th>
<th>Worst Margin</th>
</tr>
"""

    for mode in modes:
        worst = mode.get("worst_branch")

        worst_branch_number = (
            worst["branch_number"]
            if worst else "N/A"
        )

        worst_margin = (
            f"{worst['pressure_margin_psi']:.2f} PSI"
            if worst else "N/A"
        )

        html += "<tr>"
        html += f"<td>{mode['mode_name']}</td>"
        html += f"<td>{mode['passed']}</td>"
        html += f"<td>{mode['branch_count']}</td>"
        html += f"<td>{mode['total_flow_gpm']:.2f} GPM</td>"
        html += f"<td>{mode.get('pump_operating_pressure_psi', 0):.2f} PSI</td>"
        html += f"<td>{mode.get('pump_flow_utilization_fraction', 0) * 100:.1f}%</td>"
        html += f"<td>{worst_branch_number}</td>"
        html += f"<td>{worst_margin}</td>"
        html += "</tr>"

    html += "</table>"

    return html
