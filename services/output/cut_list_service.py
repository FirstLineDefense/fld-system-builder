def generate_cut_list(project):
    primary = project.get("primary", {}) or {}
    branches = primary.get("branches", []) or []

    items = []

    for index, branch in enumerate(branches, start=1):
        name = branch.get("name") or f"Branch {index}"
        pipe_size = branch.get("pipe_size") or branch.get("pipe_diameter") or "unknown"
        pipe_type = branch.get("pipe_type") or "pipe"
        length_ft = float(branch.get("length_ft") or branch.get("length") or 0)

        if length_ft > 0:
            items.append({
                "category": "Pipe",
                "item": f"{pipe_size} {pipe_type}",
                "quantity": round(length_ft, 2),
                "unit": "ft",
                "location": name,
                "notes": "Branch pipe run"
            })

        sprinkler_count = int(branch.get("sprinkler_count") or branch.get("sprinklers") or 0)
        if sprinkler_count > 0:
            items.append({
                "category": "Sprinklers",
                "item": "Sprinkler / nozzle head",
                "quantity": sprinkler_count,
                "unit": "each",
                "location": name,
                "notes": "Verify final head type from design"
            })

        fittings = [
            ("90° elbow", branch.get("elbow_90_qty")),
            ("45° elbow", branch.get("elbow_45_qty")),
            ("tee", branch.get("tee_qty")),
            ("coupling", branch.get("coupling_qty")),
            ("union", branch.get("union_qty")),
            ("adapter", branch.get("adapter_qty")),
            ("valve", branch.get("valve_qty")),
        ]

        for fitting_name, qty in fittings:
            qty = int(qty or 0)
            if qty > 0:
                items.append({
                    "category": "Fittings",
                    "item": f"{pipe_size} {fitting_name}",
                    "quantity": qty,
                    "unit": "each",
                    "location": name,
                    "notes": "Installer verify material and pressure rating"
                })

    pump = primary.get("pump", {}) or {}
    if pump:
        items.append({
            "category": "Pump",
            "item": pump.get("name") or pump.get("model") or "Pump",
            "quantity": 1,
            "unit": "each",
            "location": "System",
            "notes": "Selected/recommended pump"
        })

    motor = primary.get("motor", {}) or {}
    if motor:
        items.append({
            "category": "Motor / Engine",
            "item": motor.get("name") or motor.get("model") or "Motor / Engine",
            "quantity": 1,
            "unit": "each",
            "location": "System",
            "notes": "Selected/recommended drive source"
        })

    return {
        "status": "ok",
        "item_count": len(items),
        "items": items
    }
