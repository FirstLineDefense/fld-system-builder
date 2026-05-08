from services.auto_apply_service import (
    get_auto_apply_result,
)


def build_auto_apply_html(primary):
    result = get_auto_apply_result(primary)

    section_class = "section section-yellow"

    if result.get("improvement", 0) > 0:
        section_class = "section section-green"

    elif result.get("improvement", 0) < 0:
        section_class = "section section-red"

    html = f"""
    <div class="{section_class}">
    <h2>Safe Auto-Apply Candidate</h2>
    <p><strong>Status:</strong> {result.get("status")}</p>
    <p><strong>Original Score:</strong> {result.get("original_score")}</p>
    <p><strong>Auto-Applied Score:</strong> {result.get("auto_applied_score")}</p>
    <p><strong>Improvement:</strong> {result.get("improvement")}</p>
    <p>This does not overwrite the original design. It only shows what a safe candidate correction would do.</p>
    """

    changes = result.get("changes", [])

    if changes:
        html += "<h3>Candidate Changes</h3><ul>"

        for change in changes:
            html += f"<li>{change}</li>"

        html += "</ul>"

    else:
        html += "<p>No safe auto-apply changes were generated.</p>"

    html += "</div>"

    return html
