def generate_recommendation_summary(
    multi_scenario_proposals=None,
):
    multi_scenario_proposals = multi_scenario_proposals or {}

    better = multi_scenario_proposals.get("better", {})
    better_pricing = better.get("proposal_pricing", {})

    recommended_total = better_pricing.get("proposal_total", 0)

    return f"""
<div class="recommendation-content">

<p>
FLD currently recommends the
<strong>BETTER / Resilient Install</strong>
tier as the strongest balance between deployment cost,
resiliency expansion capability,
and long-term operational flexibility.
</p>

<h2>Why This Tier Is Recommended</h2>

<ul>
    <li>Stronger off-grid readiness pathway</li>
    <li>Better long-term upgrade flexibility</li>
    <li>Improved operational resilience</li>
    <li>Balanced infrastructure planning</li>
    <li>Better alignment with future V3 / V4 architecture expansion</li>
</ul>

<p>
<strong>Current estimated recommended deployment total:</strong>
${recommended_total:.2f}
</p>

<h2>Future Recommendation Intelligence</h2>

<ul>
    <li>Property slope analysis</li>
    <li>Vegetation density analysis</li>
    <li>Water source classification</li>
    <li>Runtime objective modeling</li>
    <li>Power redundancy planning</li>
    <li>Responder integration planning</li>
</ul>

</div>
"""
