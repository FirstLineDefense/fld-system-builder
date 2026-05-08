def generate_executive_summary(
    project=None,
    hydraulic_summary=None,
    cost_summary=None,
    multi_scenario_proposals=None,
):
    project = project or {}
    hydraulic_summary = hydraulic_summary or {}
    cost_summary = cost_summary or {}
    multi_scenario_proposals = multi_scenario_proposals or {}

    project_name = project.get("name") or project.get("project_name") or "this property"
    base_cost = float(cost_summary.get("total_cost", 0) or 0)

    scenario_count = len(multi_scenario_proposals)

    html = f"""
<div class="summary-block">

<p>
This report summarizes the proposed First Line Defense wildfire resiliency
system for <strong>{project_name}</strong>.
</p>

<p>
The system is being evaluated as layered wildfire protection infrastructure,
not simply as a sprinkler package.
</p>

<p>
The design combines water delivery, off-grid operation,
system maintainability, and future upgrade paths into one coordinated
protection strategy.
</p>

<p>
<strong>Current estimated base material / system cost:</strong>
${base_cost:.2f}
</p>
"""

    if scenario_count:
        html += f"""
<p>
This report currently includes
<strong>{scenario_count} proposal scenarios</strong>
so the client can compare budget, resilient,
and enterprise-level deployment options from the same core system design.
</p>
"""

    html += """
<h2>Key Presentation Goals</h2>

<ul>
    <li>Show the client what is being protected.</li>
    <li>Explain why the system is designed this way.</li>
    <li>Compare proposal tiers clearly.</li>
    <li>Preserve future V2 / V3 / V4 upgrade paths.</li>
    <li>Support responder-facing infrastructure planning.</li>
</ul>

</div>
"""

    return html
