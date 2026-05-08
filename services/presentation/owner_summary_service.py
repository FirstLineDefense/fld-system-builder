def generate_owner_summary(
    hydraulic_summary=None,
    recommendations=None,
):
    hydraulic_summary = hydraulic_summary or {}
    recommendations = recommendations or {}

    pump = recommendations.get("pump") or "Unknown Pump"
    motor = recommendations.get("motor") or "Unknown Motor"

    total_gpm = hydraulic_summary.get("total_gpm", 0)
    pressure = hydraulic_summary.get("system_pressure_psi", 0)

    return f"""
<div class="owner-summary-block">

<p>
This section summarizes the currently proposed operational system characteristics.
</p>

<div class="owner-summary-grid">

<div class="owner-summary-card">
    <h2>Pump Recommendation</h2>
    <div class="summary-value">{pump}</div>
</div>

<div class="owner-summary-card">
    <h2>Motor Recommendation</h2>
    <div class="summary-value">{motor}</div>
</div>

<div class="owner-summary-card">
    <h2>Total Estimated Flow</h2>
    <div class="summary-value">{total_gpm} GPM</div>
</div>

<div class="owner-summary-card">
    <h2>Estimated Pressure</h2>
    <div class="summary-value">{pressure} PSI</div>
</div>

</div>

</div>
"""
