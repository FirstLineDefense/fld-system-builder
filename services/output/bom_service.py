from collections import defaultdict


def generate_bom(cut_list):
    items = cut_list.get("items", []) or []

    grouped = defaultdict(lambda: {
        "quantity": 0,
        "unit": "",
        "locations": set(),
        "notes": set(),
        "category": ""
    })

    for item in items:
        key = (
            item.get("category"),
            item.get("item"),
            item.get("unit"),
        )

        grouped[key]["quantity"] += float(item.get("quantity") or 0)
        grouped[key]["unit"] = item.get("unit") or ""
        grouped[key]["category"] = item.get("category") or ""
        grouped[key]["locations"].add(item.get("location") or "")
        grouped[key]["notes"].add(item.get("notes") or "")

    bom_items = []

    for (category, item_name, unit), data in grouped.items():
        bom_items.append({
            "category": category,
            "item": item_name,
            "quantity": round(data["quantity"], 2),
            "unit": unit,
            "locations": sorted(list(data["locations"])),
            "notes": sorted(list(data["notes"]))
        })

    bom_items = sorted(
        bom_items,
        key=lambda x: (x["category"], x["item"])
    )

    category_totals = defaultdict(int)

    for item in bom_items:
        category_totals[item["category"]] += 1

    return {
        "status": "ok",
        "item_count": len(bom_items),
        "category_totals": dict(category_totals),
        "items": bom_items
    }
