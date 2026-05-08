def build_selected_components_html(primary):
    html = "<h2>Selected Components / Cut Sheet Starter</h2>"

    html += "<table>"

    html += (
        "<tr>"
        "<th>Component</th>"
        "<th>Type</th>"
        "<th>Quantity</th>"
        "<th>Unit Cost</th>"
        "<th>Line Cost</th>"
        "</tr>"
    )

    auto_selected = primary.get("auto_selected", {})

    for item in primary["selected_components"]:
        component = item["component"]
        quantity = item["quantity"]

        line_cost = component.unit_cost * quantity

        component_name = component.name

        if (
            component.component_type == "pump"
            and auto_selected.get("pump")
        ):
            component_name += " (Auto Selected)"

        if (
            component.component_type == "water_storage"
            and auto_selected.get("water_storage")
        ):
            component_name += " (Auto Selected)"

        html += "<tr>"
        html += f"<td>{component_name}</td>"
        html += f"<td>{component.component_type}</td>"
        html += f"<td>{quantity}</td>"
        html += f"<td>${component.unit_cost:.2f}</td>"
        html += f"<td>${line_cost:.2f}</td>"
        html += "</tr>"

    html += "</table>"

    return html
