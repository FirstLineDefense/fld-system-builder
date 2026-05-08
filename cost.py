def estimate_cost_from_components(selected_components):
    total_cost = 0
    missing_cost_items = []

    for item in selected_components:
        quantity = item.get("quantity", 0)
        component = item.get("component")

        if not component:
            continue

        if component.unit_cost is None:
            missing_cost_items.append(component.name)
            continue

        total_cost += quantity * component.unit_cost

    return {
        "component_count": len(selected_components),
        "total_cost": total_cost,
        "missing_cost_items": missing_cost_items,
        "notes": "Cost derived from selected component library."
    }