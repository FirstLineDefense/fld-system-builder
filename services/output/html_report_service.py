from services.output.installer_report_service import (
    generate_installer_report,
)
from services.output.owner_summary_service import (
    generate_owner_summary,
)


def generate_html_report(
    installer_report,
    owner_summary,
    executive_summary="",
    system_capability_summary="",
    scenario_comparison_summary="",
    recommendation_summary="",
    scenario_matrix=None,
    next_steps_section="",
    pricing_presentation="",
    proposal_pricing=None,
    multi_scenario_proposals=None,
):
    proposal_pricing = proposal_pricing or {{}}
    multi_scenario_proposals = multi_scenario_proposals or {{}}
    scenario_matrix = scenario_matrix or []

    proposal_section = ""

    multi_scenario_section = ""

    scenario_matrix_section = ""


    scenario_card_section = ""

    if scenario_matrix:
        cards = []

        for row in scenario_matrix:
            badge = row.get("badge", "")
            label = row.get("label", "")
            total = row.get("proposal_total", 0)

            card_class = "proposal-tier-card"

            if badge == "Recommended":
                card_class += " recommended-tier"

            cards.append(
                f"""
<div class="{{card_class}}">
    <div class="tier-label">{{label}}</div>
    <div class="tier-badge">{{badge}}</div>

    <div class="tier-price">
        ${{total:,.2f}}
    </div>

    <ul>
        <li><strong>Automation:</strong> {{row.get("automation_level", "")}}</li>
        <li><strong>Resilience:</strong> {{row.get("resilience_level", "")}}</li>
        <li><strong>Off-Grid:</strong> {{row.get("off_grid_capability", "")}}</li>
    </ul>
</div>
"""
            )

        scenario_card_section = f"""
    <div class="section proposal-card technical-section">
        <h1>FLD Proposal Tier Overview</h1>

        <div class="proposal-tier-grid">
            {{"".join(cards)}}
        </div>
    </div>
"""

    if scenario_matrix:
        rows = []
        for row in scenario_matrix:
            row_class = ""

            if row.get("badge") == "Recommended":
                row_class = "matrix-recommended"

            rows.append(
                f"""
<tr class="{{row_class}}">
    <td>{{row.get("label", "")}}</td>
    <td><strong>{{row.get("badge", "")}}</strong></td>
    <td>${{row.get("proposal_total", 0):.2f}}</td>
    <td>{{row.get("automation_level", "")}}</td>
    <td>{{row.get("resilience_level", "")}}</td>
    <td>{{row.get("off_grid_capability", "")}}</td>
    <td>{{row.get("sensor_support", "")}}</td>
    <td>{{row.get("responder_integration", "")}}</td>
    <td>{{row.get("maintenance_support", "")}}</td>
    <td>{{row.get("upgrade_path", "")}}</td>
</tr>
"""
            )

        scenario_matrix_rows = "\n".join(rows)

        scenario_matrix_section = f"""
    <div class="section proposal-card technical-section">
        <h1>FLD Scenario Matrix</h1>

        <div class="scenario-matrix-wrapper">

        <table>
            <tr>
                <th>Tier</th>
                <th>Badge</th>
                <th>Total</th>
                <th>Automation</th>
                <th>Resilience</th>
                <th>Off-Grid Capability</th>
                <th>Sensor Support</th>
                <th>Responder Integration</th>
                <th>Maintenance</th>
                <th>Upgrade Path</th>
            </tr>
            {{scenario_matrix_rows}}
        </table>

        </div>

    </div>
"""

    if multi_scenario_proposals:
        scenario_lines = []

        for scenario_key, scenario in multi_scenario_proposals.items():
            pricing = scenario.get("proposal_pricing", {})

            scenario_lines.append(
                f"""
{{scenario.get("profile_name")}}
------------------------------------------------------------
Base Cost: ${{pricing.get("base_cost", 0):.2f}}
Markup: {{pricing.get("markup_percent", 0):.1f}}%
Client Price: ${{pricing.get("product_client_price", 0):.2f}}
Design Total: ${{pricing.get("design_total", 0):.2f}}
Maintenance: ${{pricing.get("maintenance_plan_fee", 0):.2f}}
Subscription: ${{pricing.get("subscription_fee", 0):.2f}}

TOTAL PROPOSAL: ${{pricing.get("proposal_total", 0):.2f}}
"""
            )

        scenario_text = "\n".join(scenario_lines)

        multi_scenario_section = f"""
    <div class="section proposal-card technical-section">
        <div class="section-label">Scenario Comparison</div><h1>FLD Proposal Scenario Comparison</h1><div class="section-divider"></div>
        <pre>{{scenario_text}}</pre>
    </div>
"""
    if proposal_pricing:
        proposal_section = f"""
    <div class="section proposal-card technical-section">
        <div class="section-label">Pricing</div><h1>FLD Client Proposal Pricing</h1><div class="section-divider"></div>
        {pricing_presentation}
    </div>
"""


    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>FLD Report</title>

    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 50px;
            background: #eef2f6;
            color: #222;
        }}

        .container {{
            max-width: 1280px;
            margin: 0 auto;
            background: white;
            padding: 70px;
            border-radius: 20px;
            box-shadow: 0 15px 50px rgba(0,0,0,0.08);
        }}

        h1 {{
            border-bottom: 2px solid #ddd;
            padding-bottom: 10px;
        }}

        pre {{
            white-space: pre-wrap;
            word-wrap: break-word;
            background: #fafafa;
            padding: 20px;
            border-radius: 6px;
            border: 1px solid #ddd;
            overflow-x: auto;
        }}

        

        .proposal-card {{
            background: #ffffff;
            border: 1px solid #e5e9ef;
            border-radius: 18px;
            padding: 34px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.05);
        }}

        .proposal-card h1 {{
            margin-top: 0;
            margin-bottom: 22px;
            font-size: 30px;
            color: #102a43;
        }}

        .proposal-card pre {{

        .executive-section {{
            background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
            border-left: 6px solid #1d4e89;
        }}

        .executive-section h1 {{
            font-size: 34px;
            color: #0f2744;
        }}

        .technical-section {{
            background: #fcfcfd;
            border-left: 6px solid #9aa5b1;
        }}

        .pricing-section {{
            background: linear-gradient(180deg, #fffdf7 0%, #fff8e8 100%);
            border-left: 6px solid #d9822b;
        }}

        .pricing-section h1 {{

        .next-steps-section {{
            background: linear-gradient(180deg, #f8fbff 0%, #eef4fa 100%);
            border-left: 6px solid #1d4e89;
        }}

        .next-steps-list {{
            margin-top: 20px;
            padding-left: 22px;
        }}

        .next-steps-list li {{

        

        .visual-block {{
            margin-top: 28px;
            background: #f8fafc;
            border: 2px dashed #bcccdc;
            border-radius: 18px;
            padding: 40px;
            text-align: center;
        }}

        .visual-placeholder-title {{
            font-size: 22px;
            font-weight: 700;
            color: #334e68;
            margin-bottom: 12px;
        }}

        .visual-placeholder-sub {{

        .appendix-section {{
            background: linear-gradient(180deg, #fcfcfd 0%, #f7f9fb 100%);
            border-left: 6px solid #7b8794;
        }}

        .appendix-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 18px;
            margin-top: 24px;
        }}

        .appendix-card {{
            background: white;
            border-radius: 14px;
            padding: 24px;
            border: 1px solid #d9e2ec;
        }}

        .appendix-card-title {{
            font-size: 16px;
            font-weight: 700;
            color: #334e68;
            margin-bottom: 10px;
        }}

        .appendix-card-sub {{
            color: #7b8794;
            line-height: 1.6;
            font-size: 14px;
        }}


            color: #7b8794;
            line-height: 1.7;
            max-width: 700px;
            margin: 0 auto;
        }}


        .proposal-footer {{
            margin-top: 80px;
            padding-top: 30px;
            border-top: 1px solid #d9e2ec;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: #7b8794;
            font-size: 13px;
        }}

        .footer-brand {{
            font-weight: 700;
            color: #486581;
            letter-spacing: 1px;
        }}

        .footer-meta {{
            text-align: right;
            line-height: 1.7;
        }}


            margin-bottom: 16px;
            line-height: 1.7;
            color: #334e68;
        }}



        .section-label {{
            display: inline-block;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: #7b8794;
            margin-bottom: 16px;
        }}

        .executive-section .section-label {{
            color: #1d4e89;
        }}

        .pricing-section .section-label {{
            color: #b95f17;
        }}

        .section-divider {{

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 18px;
            margin-bottom: 50px;
        }}

        .metric-card {{
            background: white;
            border-radius: 18px;
            padding: 24px;
            border: 1px solid #e5e9ef;
            box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        }}

        .metric-label {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #7b8794;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        .metric-value {{
            font-size: 30px;
            font-weight: 800;
            color: #102a43;
            line-height: 1.1;
        }}

        .metric-sub {{

            .container {{
                box-shadow: none;
                border-radius: 0;
                max-width: 100%;
            }}

            .proposal-card {{
                box-shadow: none;
                break-inside: avoid;
            }}

            .metric-card {{
                box-shadow: none;
            }}

            .hero {{
                box-shadow: none;
            }}
        }}


            margin-top: 8px;
            color: #52606d;
            font-size: 14px;
        }}


            height: 1px;
            background: linear-gradient(
                90deg,
                rgba(0,0,0,0.08),
                rgba(0,0,0,0)
            );
            margin: 22px 0 30px 0;
        }}


            color: #b95f17;
        }}


            margin: 0;
            background: transparent;
            border: none;
            padding: 0;
            font-size: 15px;
            line-height: 1.8;
        }}


        .section {{
            margin-bottom: 70px;
        }}
    

        .fld-logo {{
            width: 48px !important;
            height: 48px !important;
            max-width: 48px !important;
            max-height: 48px !important;
            min-width: 48px !important;
            min-height: 48px !important;
            object-fit: contain !important;
            display: inline-block !important;
            vertical-align: middle !important;
        }}


</style>
</head>

<body>
<div class="page">


    <div class="metrics-grid">

        <div class="metric-card">
            <div class="metric-label">Estimated Flow</div>
            <div class="metric-value">295 GPM</div>
            <div class="metric-sub">Projected system output</div>
        </div>

        <div class="metric-card">
            <div class="metric-label">Estimated Pressure</div>
            <div class="metric-value">120 PSI</div>
            <div class="metric-sub">Target operating pressure</div>
        </div>

        <div class="metric-card">
            <div class="metric-label">Proposal Total</div>
            <div class="metric-value">$5.6K</div>
            <div class="metric-sub">Initial proposal scenario</div>
        </div>

        <div class="metric-card">
            <div class="metric-label">Protection Level</div>
            <div class="metric-value">V2</div>
            <div class="metric-sub">Upgradeable FLD architecture</div>
        </div>

    </div>

<div class="hero">

    <div class="hero-top">

        <div class="hero-brand">
            <img src="/static/assets/fld_logo.png" class="fld-logo" width="48" height="48">

            <div class="brand-text">
                <div class="brand-name">
                    FIRST LINE DEFENSE
                </div>

                <div class="brand-tagline">
                    Wildfire Resiliency Systems
                </div>
            </div>
        </div>

        <div class="proposal-meta">
            <div><strong>Proposal Type:</strong> Wildfire Resiliency Proposal</div>
            <div><strong>Status:</strong> Preliminary System Design</div>
            <div><strong>Prepared By:</strong> FLD Systems</div>
        </div>

    </div>

    <div class="hero-divider"></div>

    <h1>FLD Wildfire Resiliency Proposal</h1>

    <p>
        Layered wildfire protection infrastructure and operational resiliency planning.
    </p>

</div>

<div class="container">

    <div class="section proposal-card technical-section">
        <div class="section-label">Executive Summary</div><h1>FLD Executive Summary</h1><div class="section-divider"></div>
        {{executive_summary}}
    </div>

    <div class="section proposal-card technical-section">
        <h1>FLD System Capability Summary</h1>
        <pre>{{system_capability_summary}}</pre>
    </div>

    <div class="section proposal-card technical-section">
        <h1>FLD Scenario Comparison Summary</h1>
        {{scenario_comparison_summary}}
    </div>

    <div class="recommendation-box">
        <h1>FLD Recommended Deployment Strategy</h1>
        {{recommendation_summary}}
    </div>

    <div class="section proposal-card technical-section">
        <h1>FLD Next Steps</h1>
        {next_steps_section}
    </div>

    <div class="section proposal-card technical-section">
        <h1>FLD Owner Summary</h1>
        {owner_summary}
    </div>

    {proposal_section}

    {scenario_card_section}

    {scenario_matrix_section}

    {multi_scenario_section}

    <div class="section proposal-card technical-section">
        <h1>FLD Installer Report</h1>
        <pre>{{installer_report}}</pre>
    </div>

</div>

</div>

</body>
</html>
"""

    return html
