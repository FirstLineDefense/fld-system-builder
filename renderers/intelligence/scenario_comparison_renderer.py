def build_scenario_comparison_html(primary):
    manifold = primary.get("manifold", {})
    operating_modes = manifold.get("operating_modes", {})
    modes = operating_modes.get("modes", [])

    if not modes:
        return ""

    html = "<h2>Scenario / Operating Mode Comparison</h2>"
    html += "<p>This compares how the system performs when different zones or operating groups are active.</p>"

    html += "<table>"
    html += """
<tr>
<th>Scenario</th>
<th>Passed</th>
<th>Branches Active</th>
<th>Total Flow</th>
<th>Pump PSI</th>
<th>Pump Utilization</th>
<th>Worst Branch</th>
<th>Worst Margin</th>
<th>Meaning</th>
</tr>
"""

    for mode in modes:
        worst = mode.get("worst_branch")
        worst_branch_number = worst.get("branch_number") if worst else "N/A"
        worst_margin = f"{worst.get('pressure_margin_psi', 0):.2f} PSI" if worst else "N/A"

        mode_name = mode.get("mode_name", "")

        meaning = ""

        if "All Active" in mode_name:
            meaning = "Stress test with all active zones running."
        elif "First Line" in mode_name:
            meaning = "Property hydration / first-line defensive operation."
        elif "Last Line" in mode_name:
            meaning = "Structure-defense or last-line survival mode."
        elif "Foam" in mode_name:
            meaning = "Foam-specific branch operation if configured."
        elif "Max Simultaneous" in mode_name:
            meaning = "Tests the selected number of manifold ports running at once."
        else:
            meaning = "Operating scenario comparison."

        html += "<tr>"
        html += f"<td>{mode_name}</td>"
        html += f"<td>{mode.get('passed')}</td>"
        html += f"<td>{mode.get('branch_count')}</td>"
        html += f"<td>{mode.get('total_flow_gpm', 0):.2f} GPM</td>"
        html += f"<td>{mode.get('pump_operating_pressure_psi', 0):.2f} PSI</td>"
        html += f"<td>{mode.get('pump_flow_utilization_fraction', 0) * 100:.1f}%</td>"
        html += f"<td>{worst_branch_number}</td>"
        html += f"<td>{worst_margin}</td>"
        html += f"<td>{meaning}</td>"
        html += "</tr>"

    html += "</table>"

    return html

