def build_overall_readiness_banner_html(primary):
    readiness = primary.get("section_readiness", {})

    if not readiness:
        return ""

    overall = readiness.get("overall_status", "yellow")

    background = "#fff3bf"
    text = "PARTIAL"

    if overall == "green":
        background = "#d7f7d7"
        text = "READY"
    elif overall == "red":
        background = "#ffd6d6"
        text = "INSUFFICIENT"

    counts = readiness.get("counts", {})
    bottleneck_data = primary.get("bottleneck_intelligence", {})
    primary_bottleneck = bottleneck_data.get("summary", "")

    architecture = primary.get("architecture_recommendations", {})
    recommendations = architecture.get("recommendations", [])

    top_action = ""

    if recommendations:
        top = recommendations[0]
        top_action = f"{top.get('title')}: {top.get('recommendation')}"

    html = f"""
<div style="
    background:{background};
    padding:20px;
    border-radius:10px;
    margin-bottom:20px;
    border:2px solid #999;
">
    <h2 style="margin-top:0;">Design Readiness: {text}</h2>

    <p>
    Green Sections: {counts.get('green', 0)} |
    Yellow Sections: {counts.get('yellow', 0)} |
    Red Sections: {counts.get('red', 0)}
    </p>

    <p>
    This reflects how complete and trustworthy the current design state is.
    </p>

    <p>
    <strong>Primary Bottleneck:</strong> {primary_bottleneck}
    </p>

    <p>
    <strong>Top Suggested Action:</strong> {top_action}
    </p>
</div>
"""

    return html

