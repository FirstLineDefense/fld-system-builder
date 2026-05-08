def build_branch_results_html(manifold):
    html = "<h2>Branch Results</h2>"
    html += "<table>"

    html += """
<tr>
<th>Branch</th>
<th>Role</th>
<th>Priority</th>
<th>Pipe</th>
<th>Base Length</th>
<th>Fitting Eq. Length</th>
<th>Total Effective Length</th>
<th>Fittings</th>
<th>Elevation</th>
<th>Flow</th>
<th>Velocity</th>
<th>Friction Loss</th>
<th>Total TDH</th>
<th>Pump PSI</th>
<th>Final PSI</th>
<th>Required PSI</th>
<th>Margin</th>
<th>Passed</th>
</tr>
"""

    for branch in manifold["branch_results"]:
        pump_operating = branch.get("pump_operating_point", {})

        fittings_text = (
            f"90s: {branch.get('elbow_90_qty', 0)}<br>"
            f"45s: {branch.get('elbow_45_qty', 0)}<br>"
            f"Sweeps: {branch.get('sweep_bend_qty', 0)}<br>"
            f"Tees: {branch.get('tee_qty', 0)}<br>"
            f"Valves: {branch.get('valve_qty', 0)}<br>"
            f"Other: {branch.get('other_equivalent_length_ft', 0)} ft"
        )

        html += "<tr>"
        html += f"<td>{branch['branch_number']}</td>"
        html += f"<td>{branch['role']}</td>"
        html += f"<td>{branch['priority']}</td>"
        html += f"<td>{branch['pipe_name']}</td>"
        html += f"<td>{branch.get('base_pipe_length_ft', branch.get('pipe_length_ft', 0)):.2f} ft</td>"
        html += f"<td>{branch.get('equivalent_length_ft', 0):.2f} ft</td>"
        html += f"<td>{branch.get('effective_pipe_length_ft', branch.get('pipe_length_ft', 0)):.2f} ft</td>"
        html += f"<td>{fittings_text}</td>"
        html += f"<td>{branch['elevation_change_ft']} ft</td>"
        html += f"<td>{branch['flow']['total_flow_gpm']:.2f} GPM</td>"
        html += f"<td>{branch.get('velocity_fps', 0):.2f} ft/s</td>"
        html += f"<td>{branch.get('friction_loss_psi', 0):.2f} PSI</td>"
        html += f"<td>{branch.get('total_dynamic_head_ft', 0):.2f} ft</td>"
        html += f"<td>{pump_operating.get('pressure_psi', 0):.2f} PSI</td>"
        html += f"<td>{branch['final_pressure_psi']:.2f}</td>"
        html += f"<td>{branch['required_terminal_pressure_psi']:.2f}</td>"
        html += f"<td>{branch['pressure_margin_psi']:.2f}</td>"
        html += f"<td>{branch['passed']}</td>"
        html += "</tr>"

    html += "</table>"

    return html
