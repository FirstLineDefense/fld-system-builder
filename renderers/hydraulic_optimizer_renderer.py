def build_hydraulic_optimizer_html(primary):
    optimizer = primary.get("hydraulic_optimizer", {})

    html = "<h2>Hydraulic Optimizer</h2>"

    html += (
        f"<p><strong>Status:</strong> "
        f"{optimizer.get('status', 'Not Available')}</p>"
    )

    html += (
        f"<p><strong>Summary:</strong> "
        f"{optimizer.get('summary', '')}</p>"
    )

    governing = optimizer.get("governing_branch")

    if governing:
        html += (
            f"<p><strong>Governing Branch:</strong> "
            f"{governing}</p>"
        )

    html += "<h3>Pipe Upgrade Trials</h3>"

    html += "<table>"

    html += (
        "<tr>"
        "<th>Branch</th>"
        "<th>Current Pipe</th>"
        "<th>Recommended Pipe</th>"
        "<th>Baseline Margin</th>"
        "<th>Trial Margin</th>"
        "<th>Margin Gain</th>"
        "<th>Baseline Velocity</th>"
        "<th>Trial Velocity</th>"
        "<th>Passed</th>"
        "<th>Best</th>"
        "<th>Engineering Reasoning</th>"
        "<th>Recommendation</th>"
        "</tr>"
    )

    trials = optimizer.get("pipe_upgrade_trials", [])

    if trials:
        for item in trials:
            reasoning_items = item.get(
                "engineering_reasoning",
                []
            )

            reasoning_html = "<br>".join(reasoning_items)

            best_value = (
                "Yes"
                if item.get("minimum_viable")
                else ""
            )

            html += "<tr>"

            html += (
                f"<td>{item.get('branch_number')}</td>"
            )

            html += (
                f"<td>{item.get('current_pipe')}</td>"
            )

            html += (
                f"<td>{item.get('recommended_pipe')}</td>"
            )

            html += (
                f"<td>{item.get('baseline_margin_psi'):.2f}</td>"
            )

            html += (
                f"<td>{item.get('trial_margin_psi'):.2f}</td>"
            )

            html += (
                f"<td>{item.get('margin_gain_psi'):.2f}</td>"
            )

            html += (
                f"<td>{item.get('baseline_velocity_fps'):.2f}</td>"
            )

            html += (
                f"<td>{item.get('trial_velocity_fps'):.2f}</td>"
            )

            html += (
                f"<td>{item.get('trial_passed')}</td>"
            )

            html += f"<td>{best_value}</td>"

            html += f"<td>{reasoning_html}</td>"

            html += (
                f"<td>{item.get('recommendation')}</td>"
            )

            html += "</tr>"

    else:
        html += (
            "<tr>"
            "<td colspan='12'>"
            "No pipe upgrade trials generated."
            "</td>"
            "</tr>"
        )

    html += "</table>"

    html += "<h3>Combined Pipe Upgrade Trial</h3>"

    combined = optimizer.get(
        "combined_pipe_upgrade_trial"
    )

    if combined:
        html += (
            f"<p><strong>Passed:</strong> "
            f"{combined.get('passed')}</p>"
        )

        html += (
            f"<p><strong>Last-Line Passed:</strong> "
            f"{combined.get('last_line_passed')}</p>"
        )

        html += (
            f"<p><strong>Trial Total Flow:</strong> "
            f"{combined.get('trial_total_flow_gpm'):.2f} GPM</p>"
        )

        html += (
            f"<p><strong>Failing Branch Count:</strong> "
            f"{combined.get('trial_failing_branch_count')}</p>"
        )

        html += (
            f"<p><strong>Recommendation:</strong> "
            f"{combined.get('recommendation')}</p>"
        )

        html += "<table>"

        html += (
            "<tr>"
            "<th>Branch</th>"
            "<th>Current Pipe</th>"
            "<th>Recommended Pipe</th>"
            "</tr>"
        )

        for change in combined.get("changes", []):
            html += "<tr>"

            html += (
                f"<td>{change.get('branch_number')}</td>"
            )

            html += (
                f"<td>{change.get('current_pipe')}</td>"
            )

            html += (
                f"<td>{change.get('recommended_pipe')}</td>"
            )

            html += "</tr>"

        html += "</table>"

    else:
        html += (
            "<p>No combined pipe upgrade "
            "trial generated.</p>"
        )

    return html
