import json

from services.output.project_report_pipeline import generate_project_report_package


def test_project_report_package_accepts_live_cost_override():
    project = {
        "primary": {
            "pump": {"name": "Pump B"},
            "motor": {"name": "Unknown Motor"},
            "branches": [
                {
                    "name": "first_line",
                    "pipe_size": "1 inch",
                    "pipe_type": "Schedule 80 PVC",
                    "length_ft": 187,
                    "sprinkler_count": 0,
                    "elbow_90_qty": 5,
                    "tee_qty": 2,
                    "valve_qty": 1,
                }
            ],
        }
    }

    package = generate_project_report_package(
        project=project,
        pricing={},
        hydraulic_summary={"Total Active Flow": "175 GPM"},
        warnings=[],
        recommendations=[],
        cost_override=4180,
        proposal_inputs={
            "markup_percent": 35,
            "design_hours": 10,
            "design_hourly_rate": 150,
            "maintenance_plan_fee": 1200,
            "subscription_fee": 600,
        },
    )

    assert package["status"] == "ok"
    assert package["cost_summary"]["total_cost"] == 4180.0
    assert package["proposal_pricing"]["proposal_total"] == 8943.0
    assert "FLD OWNER SUMMARY" in package["owner_summary"]
    assert "Estimated Material Cost: $4180.00" in package["owner_summary"]
    assert "FLD INSTALLER REPORT" in package["installer_report"]
    assert "FLD Client Proposal Pricing" in package["html_report"]
    assert "CLIENT PROPOSAL PRICING" in package["html_report"]
    assert "Client Product Price: $5643.00" in package["html_report"]
    assert "Estimated Client Proposal Total: $8943.00" in package["html_report"]


def test_project_report_package_is_json_safe():
    project = {
        "primary": {
            "pump": {"name": "Pump B"},
            "motor": {"name": "Unknown Motor"},
            "branches": [],
        }
    }

    package = generate_project_report_package(
        project=project,
        pricing={},
        hydraulic_summary={},
        warnings=[],
        recommendations=[],
        cost_override=0,
    )

    json.dumps(package, default=str)
