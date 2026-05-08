def build_guided_builder_summary_html(primary):
    section_readiness = primary.get("section_readiness", {})
    bottleneck_data = primary.get("bottleneck_intelligence", {})
    architecture = primary.get("architecture_recommendations", {})

    if not section_readiness:
        return ""

    overall = section_readiness.get("overall_status", "").upper()
    counts = section_readiness.get("counts", {})

    html = "<h2>Guided Builder Summary</h2>"
    html += f"<p><strong>Builder Status:</strong> {overall}</p>"
    html += f"<p><strong>Section Readiness:</strong> Green {counts.get('green', 0)} | Yellow {counts.get('yellow', 0)} | Red {counts.get('red', 0)}</p>"

    if bottleneck_data.get("summary"):
        html += f"<p><strong>Primary Bottleneck:</strong> {bottleneck_data.get('summary')}</p>"

    recommendations = architecture.get("recommendations", [])

    if recommendations:
        top = recommendations[0]
        html += f"<p><strong>Top Architecture Action:</strong> {top.get('title')} — {top.get('recommendation')}</p>"

    html += "<p><strong>Suggested Next Step:</strong> Review any red or yellow sections below before treating this as proposal-grade.</p>"

    return html

