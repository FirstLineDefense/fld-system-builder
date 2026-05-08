def generate_pricing_presentation(
    proposal_pricing=None,
):
    proposal_pricing = proposal_pricing or {}

    return f"""
<div class="pricing-grid">

<div class="pricing-card">
    <h2>Base System Cost</h2>
    <div class="pricing-value">
        ${proposal_pricing.get("base_cost", 0):,.2f}
    </div>
</div>

<div class="pricing-card">
    <h2>Equipment Markup</h2>
    <div class="pricing-value">
        ${proposal_pricing.get("product_markup", 0):,.2f}
    </div>

    <div class="pricing-subtext">
        {proposal_pricing.get("markup_percent", 0):.1f}% markup
    </div>
</div>

<div class="pricing-card">
    <h2>Client Equipment Price</h2>
    <div class="pricing-value">
        ${proposal_pricing.get("product_client_price", 0):,.2f}
    </div>
</div>

<div class="pricing-card">
    <h2>Design Services</h2>
    <div class="pricing-value">
        ${proposal_pricing.get("design_total", 0):,.2f}
    </div>
</div>

<div class="pricing-card">
    <h2>Maintenance Plan</h2>
    <div class="pricing-value">
        ${proposal_pricing.get("maintenance_plan_fee", 0):,.2f}
    </div>
</div>

<div class="pricing-card">
    <h2>Subscription Services</h2>
    <div class="pricing-value">
        ${proposal_pricing.get("subscription_fee", 0):,.2f}
    </div>
</div>

</div>

<div class="proposal-total-box">

<div class="proposal-total-label">
Estimated Client Proposal Total
</div>

<div class="proposal-total-value">
${proposal_pricing.get("proposal_total", 0):,.2f}
</div>

</div>
"""
