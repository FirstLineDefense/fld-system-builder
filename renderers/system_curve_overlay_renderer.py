from pump_curve import build_curve_svg


def build_system_curve_overlay_html(primary):
    pump = primary.get("pump")

    if not pump:
        return ""

    manifold = primary.get("manifold", {})

    curve_data = primary.get("pump_curve_analysis", {})

    operating_flow = manifold.get("total_flow_gpm", 0)

    operating_pressure = manifold.get(
        "pump_operating_pressure_psi",
        0
    )

    required_pressure = manifold.get(
        "required_pump_pressure_psi",
        operating_pressure
    )

    pump_analysis = primary.get("pump_analysis", {})

    operating_point = {
        "flow_gpm": operating_flow,
        "pressure_psi": operating_pressure
    }

    required_point = {
        "flow_gpm": operating_flow,
        "pressure_psi": required_pressure
    }

    svg = build_curve_svg(
        curve_data.get("curve_points", []),
        operating_point=operating_point,
        required_point=required_point
    )

    pressure_surplus = (
        operating_pressure - required_pressure
    )

    html = "<h2>System Operating Point Overlay</h2>"

    html += (
        "<p>This chart shows the selected system’s "
        "operating point against the pump curve.</p>"
    )

    html += f"<p><strong>Pump:</strong> {pump.name}</p>"

    html += (
        f"<p><strong>Curve Source:</strong> "
        f"{curve_data.get('curve_source')}</p>"
    )

    html += (
        f"<p><strong>Operating Flow:</strong> "
        f"{operating_flow:.2f} GPM</p>"
    )

    html += (
        f"<p><strong>Operating Pump Pressure:</strong> "
        f"{operating_pressure:.2f} PSI</p>"
    )

    html += (
        f"<p><strong>Estimated Required Pump Pressure:"
        f"</strong> {required_pressure:.2f} PSI</p>"
    )

    html += (
        f"<p><strong>Estimated Pump Pressure Surplus:"
        f"</strong> {pressure_surplus:.2f} PSI</p>"
    )

    if pressure_surplus < 0:
        html += (
            "<p><strong>Overlay Warning:</strong> "
            "Operating pressure is below estimated "
            "required pump pressure.</p>"
        )

    elif pressure_surplus < 10:
        html += (
            "<p><strong>Overlay Warning:</strong> "
            "Operating pressure surplus is thin.</p>"
        )

    if (
        pump_analysis.get(
            "flow_utilization_fraction",
            0
        ) > 0.85
    ):
        html += (
            "<p><strong>Overlay Warning:</strong> "
            "Pump is operating near the high end "
            "of its flow range.</p>"
        )

    html += svg

    return html
