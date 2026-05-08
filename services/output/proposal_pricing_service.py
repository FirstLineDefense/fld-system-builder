def generate_proposal_pricing(
    cost_summary,
    markup_percent=35,
    design_hours=0,
    design_hourly_rate=0,
    maintenance_plan_fee=0,
    subscription_fee=0,
):
    cost_summary = cost_summary or {}

    base_cost = float(cost_summary.get("total_cost", 0) or 0)
    markup_rate = float(markup_percent or 0) / 100

    product_markup = round(base_cost * markup_rate, 2)
    product_client_price = round(base_cost + product_markup, 2)

    design_total = round(float(design_hours or 0) * float(design_hourly_rate or 0), 2)
    maintenance_total = round(float(maintenance_plan_fee or 0), 2)
    subscription_total = round(float(subscription_fee or 0), 2)

    proposal_total = round(
        product_client_price
        + design_total
        + maintenance_total
        + subscription_total,
        2
    )

    return {
        "status": "ok",
        "base_cost": round(base_cost, 2),
        "markup_percent": float(markup_percent or 0),
        "product_markup": product_markup,
        "product_client_price": product_client_price,
        "design_hours": float(design_hours or 0),
        "design_hourly_rate": float(design_hourly_rate or 0),
        "design_total": design_total,
        "maintenance_plan_fee": maintenance_total,
        "subscription_fee": subscription_total,
        "proposal_total": proposal_total,
    }
