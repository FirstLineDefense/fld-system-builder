def build_design_maturity_html(design_maturity):
    if not design_maturity:
        return ""

    html = "<div class='section'>"
    html += "<h2>Design Maturity</h2>"

    html += f"<p><strong>Version:</strong> {design_maturity.get('version', 'v1')}</p>"
    html += f"<p><strong>Grade:</strong> {design_maturity.get('grade', 'Unknown')}</p>"

    if "score" in design_maturity:
        html += f"<p><strong>Score:</strong> {design_maturity.get('score', 0)} / {design_maturity.get('max_score', 0)} ({design_maturity.get('score_percent', 0)}%)</p>"
    else:
        html += f"<p><strong>Score:</strong> {design_maturity.get('passed_count', 0)} / {design_maturity.get('total_count', 0)}</p>"

    html += f"<p>{design_maturity.get('summary', '')}</p>"

    categories = design_maturity.get("categories", [])
    if categories:
        html += "<h3>Maturity Categories</h3>"
        html += "<ul>"

        for category in categories:
            status = "PASS" if category.get("passed") else "NEEDS WORK"
            html += (
                f"<li><strong>{status}: {category.get('name', '')}</strong><br>"
                f"Score: {category.get('score', 0)} / {category.get('max_score', 0)}<br>"
                f"{category.get('note', '')}</li>"
            )

        html += "</ul>"

    checks = design_maturity.get("checks", [])
    if checks:
        html += "<h3>Maturity Checks</h3>"
        html += "<ul>"

        for check in checks:
            status = "PASS" if check.get("passed") else "NEEDS WORK"
            html += (
                f"<li><strong>{status}: {check.get('name', '')}</strong><br>"
                f"{check.get('note', '')}</li>"
            )

        html += "</ul>"

    hard_gates = design_maturity.get("hard_gates", [])
    if hard_gates:
        html += "<h3>Hard Gates</h3>"
        html += "<ul>"

        for gate in hard_gates:
            html += f"<li>{gate}</li>"

        html += "</ul>"

    critical_warnings = design_maturity.get("critical_warnings", [])
    if critical_warnings:
        html += "<h3>Critical Warnings</h3>"
        html += "<ul>"

        for warning in critical_warnings:
            html += f"<li>{warning}</li>"

        html += "</ul>"

    soft_warnings = design_maturity.get("soft_warnings", [])
    if soft_warnings:
        html += "<h3>Soft Warnings</h3>"
        html += "<ul>"

        for warning in soft_warnings:
            html += f"<li>{warning}</li>"

        html += "</ul>"

    hydraulic_status = design_maturity.get("hydraulic_status", {})
    if hydraulic_status:
        html += "<h3>Hydraulic Status</h3>"
        html += f"<p><strong>Active Branches:</strong> {hydraulic_status.get('active_branch_count', 0)}</p>"
        html += f"<p><strong>Passing Branches:</strong> {hydraulic_status.get('passing_branch_count', 0)}</p>"
        html += f"<p><strong>Failing Branches:</strong> {hydraulic_status.get('failing_branch_count', 0)}</p>"
        html += f"<p><strong>Hydraulic Passed:</strong> {hydraulic_status.get('hydraulic_passed', False)}</p>"

    mode_status = design_maturity.get("mode_status", {})
    if mode_status:
        html += "<h3>Operating Mode Status</h3>"
        html += f"<p><strong>First Line Passed:</strong> {mode_status.get('first_line_passed', False)}</p>"
        html += f"<p><strong>Last Line Passed:</strong> {mode_status.get('last_line_passed', False)}</p>"
        html += f"<p><strong>Foam Passed:</strong> {mode_status.get('foam_passed', False)}</p>"

    html += "</div>"

    return html

