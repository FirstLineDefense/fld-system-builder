def estimate_project_cost(bom, pricing=None):
    pricing = pricing or {}

    items = bom.get("items", []) or []

    estimated_items = []

    total_cost = 0.0

    for item in items:
        name = item.get("item") or ""
        quantity = float(item.get("quantity") or 0)

        unit_cost = float(pricing.get(name, 0))

        extended_cost = round(quantity * unit_cost, 2)

        total_cost += extended_cost

        estimated_items.append({
            "category": item.get("category"),
            "item": name,
            "quantity": quantity,
            "unit": item.get("unit"),
            "unit_cost": round(unit_cost, 2),
            "extended_cost": extended_cost,
        })

    return {
        "status": "ok",
        "total_cost": round(total_cost, 2),
        "items": estimated_items,
    }
