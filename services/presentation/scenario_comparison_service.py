def generate_scenario_comparison_summary(
    multi_scenario_proposals=None,
):
    multi_scenario_proposals = multi_scenario_proposals or {}

    descriptions = {
        "good": {
            "title": "GOOD / Budget Install",
            "focus": "Core wildfire sprinkler protection with simplified deployment costs.",
            "best_for": "Clients prioritizing foundational property protection and future upgradeability.",
        },
        "better": {
            "title": "BETTER / Resilient Install",
            "focus": "Balanced resiliency architecture with stronger long-term operational flexibility.",
            "best_for": "Clients seeking stronger off-grid readiness and system resilience.",
        },
        "best": {
            "title": "BEST / Enterprise Autonomous Install",
            "focus": "High-resiliency architecture with expanded automation and infrastructure planning.",
            "best_for": "Large estates, high-risk WUI properties, or clients prioritizing maximum operational survivability.",
        },
    }

    html = """
<div class="scenario-summary-block">

<p>
This section compares the intended deployment philosophy of each proposal tier.
</p>
"""

    for key, scenario in multi_scenario_proposals.items():
        pricing = scenario.get("proposal_pricing", {})
        description = descriptions.get(key, {})

        html += f"""
<div class="scenario-card">

<h2>{description.get("title", key.upper())}</h2>

<p>
<strong>Focus:</strong>
{description.get("focus", "")}
</p>

<p>
<strong>Best For:</strong>
{description.get("best_for", "")}
</p>

<p>
<strong>Estimated Proposal Total:</strong>
${pricing.get("proposal_total", 0):.2f}
</p>

</div>
"""

    html += """
<div class="scenario-footer">

<h2>Important</h2>

<p>
All proposal tiers are generated from the same core engineering design foundation.
</p>

<p>
Proposal tiers primarily adjust resiliency philosophy,
operational redundancy,
automation pathways,
and long-term infrastructure planning.
</p>

</div>

</div>
"""

    return html
