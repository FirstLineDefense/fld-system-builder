def build_auto_select_summary_html(primary):
    auto_selected = primary.get("auto_selected", {})

    if not auto_selected:
        return ""

    active = []

    for key, value in auto_selected.items():
        if value:
            active.append(key.replace("_", " ").title())

    if not active:
        return ""

    html = "<h2>Auto Select Summary</h2>"
    html += "<p>The following items were automatically selected or evaluated by the system:</p>"
    html += "<ul>"

    for item in active:
        html += f"<li>{item}</li>"

    html += "</ul>"
    html += "<p>Auto Select means the tool is using current hydraulic demand, runtime targets, and available component data to recommend or validate a matching component.</p>"

    return html

