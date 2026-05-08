from services.constraint_render_service import (
    build_recommendation_section,
    build_auto_apply_section,
)

from engines.constraint_summary_engine import (
    build_constraint_summary,
)

def build_constraint_violation_html(
    primary,
    violations
):
    summary = build_constraint_summary(
        violations
    )

    violations = summary.get(
        "violations",
        []
    )

    html = """
    <div class="section section-red">
    <h2>Constraint Violations</h2>
    <table>
    <tr>
    <th>Constraint</th>
    <th>Severity</th>
    <th>Message</th>
    </tr>
    """

    for violation in violations:
        html += "<tr>"

        html += (
            f"<td>{violation.get('constraint')}</td>"
        )

        html += (
            f"<td>{violation.get('severity')}</td>"
        )

        html += (
            f"<td>{violation.get('message')}</td>"
        )

        html += "</tr>"

    html += """
    </table>
    </div>
    """

    html += build_recommendation_section(
        violations,
        primary
    )

    html += build_auto_apply_section(
        primary
    )

    return html
