from services.output.proposal_pricing_service import generate_proposal_pricing


def test_proposal_pricing_calculates_client_total():
    result = generate_proposal_pricing(
        cost_summary={"total_cost": 10000},
        markup_percent=35,
        design_hours=10,
        design_hourly_rate=150,
        maintenance_plan_fee=1200,
        subscription_fee=600,
    )

    assert result["status"] == "ok"
    assert result["base_cost"] == 10000.0
    assert result["product_markup"] == 3500.0
    assert result["product_client_price"] == 13500.0
    assert result["design_total"] == 1500.0
    assert result["maintenance_plan_fee"] == 1200.0
    assert result["subscription_fee"] == 600.0
    assert result["proposal_total"] == 16800.0


def test_proposal_pricing_handles_empty_inputs():
    result = generate_proposal_pricing({})

    assert result["status"] == "ok"
    assert result["base_cost"] == 0.0
    assert result["proposal_total"] == 0.0
