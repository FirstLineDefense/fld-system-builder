import csv


def safe_float(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def build_default_pump_curve(pump):
    max_flow = safe_float(getattr(pump, "max_flow_gpm", 0))
    max_pressure = safe_float(getattr(pump, "max_pressure_psi", 0))

    return [
        {"flow_gpm": 0, "pressure_psi": max_pressure},
        {"flow_gpm": max_flow * 0.25, "pressure_psi": max_pressure * 0.92},
        {"flow_gpm": max_flow * 0.50, "pressure_psi": max_pressure * 0.78},
        {"flow_gpm": max_flow * 0.75, "pressure_psi": max_pressure * 0.58},
        {"flow_gpm": max_flow, "pressure_psi": max_pressure * 0.35},
    ]


def get_saved_curve_points_for_pump(pump):
    try:
        from database import list_pump_curve_points

        pump_name = getattr(pump, "name", "")
        rows = list_pump_curve_points(pump_name)

        return [
            {
                "flow_gpm": safe_float(row["flow_gpm"]),
                "pressure_psi": safe_float(row["pressure_psi"]),
            }
            for row in rows
        ]

    except Exception:
        return []


def validate_curve_points(curve_points):
    warnings = []

    if not curve_points:
        warnings.append("No curve points exist.")
        return warnings

    points = sorted(curve_points, key=lambda point: safe_float(point.get("flow_gpm", 0)))

    if len(points) < 3:
        warnings.append("Pump curve has fewer than 3 points.")

    seen_flows = set()

    for point in points:
        flow = round(safe_float(point["flow_gpm"]), 4)

        if flow in seen_flows:
            warnings.append(f"Duplicate flow point detected near {flow} GPM.")

        seen_flows.add(flow)

    previous_flow = None
    previous_pressure = None

    for point in points:
        flow = safe_float(point["flow_gpm"])
        pressure = safe_float(point["pressure_psi"])

        if previous_flow is not None:
            if flow > previous_flow and pressure > previous_pressure:
                warnings.append(
                    f"Pressure increased from {previous_pressure:.2f} PSI to "
                    f"{pressure:.2f} PSI while flow increased."
                )

        previous_flow = flow
        previous_pressure = pressure

    if safe_float(points[0]["flow_gpm"]) > 5:
        warnings.append("Curve is missing a near-zero-flow shutoff pressure point.")

    if safe_float(points[-1]["flow_gpm"]) < 50:
        warnings.append("Curve may be missing a realistic high-flow endpoint.")

    return warnings


def get_pump_curve_points(pump):
    saved_points = get_saved_curve_points_for_pump(pump)

    if len(saved_points) >= 2:
        return {
            "curve_source": "saved_manufacturer_or_user_curve_points",
            "curve_points": saved_points,
            "validation_warnings": validate_curve_points(saved_points),
        }

    synthetic = build_default_pump_curve(pump)

    return {
        "curve_source": "synthetic_default_from_max_flow_and_max_pressure",
        "curve_points": synthetic,
        "validation_warnings": validate_curve_points(synthetic),
    }


def interpolate_pressure_from_curve(curve_points, flow_gpm):
    flow_gpm = safe_float(flow_gpm)

    if not curve_points:
        return 0

    points = sorted(curve_points, key=lambda point: safe_float(point.get("flow_gpm", 0)))

    if flow_gpm <= points[0]["flow_gpm"]:
        return safe_float(points[0]["pressure_psi"])

    if flow_gpm >= points[-1]["flow_gpm"]:
        return safe_float(points[-1]["pressure_psi"])

    for index in range(len(points) - 1):
        p1 = points[index]
        p2 = points[index + 1]

        f1 = safe_float(p1["flow_gpm"])
        f2 = safe_float(p2["flow_gpm"])
        psi1 = safe_float(p1["pressure_psi"])
        psi2 = safe_float(p2["pressure_psi"])

        if f1 <= flow_gpm <= f2:
            if f2 == f1:
                return psi1

            ratio = (flow_gpm - f1) / (f2 - f1)
            return psi1 + ratio * (psi2 - psi1)

    return safe_float(points[-1]["pressure_psi"])


def get_pump_pressure_at_flow(pump, flow_gpm):
    curve_data = get_pump_curve_points(pump)
    curve = curve_data["curve_points"]

    pressure = interpolate_pressure_from_curve(curve, flow_gpm)

    return {
        "flow_gpm": safe_float(flow_gpm),
        "pressure_psi": pressure,
        "curve_source": curve_data["curve_source"],
        "curve_points": curve,
        "validation_warnings": curve_data.get("validation_warnings", []),
    }


def analyze_pump_operating_point(pump, flow_gpm):
    max_flow = safe_float(getattr(pump, "max_flow_gpm", 0))
    max_pressure = safe_float(getattr(pump, "max_pressure_psi", 0))

    operating = get_pump_pressure_at_flow(pump, flow_gpm)

    utilization = flow_gpm / max_flow if max_flow > 0 else 0

    warnings = []

    if utilization > 1:
        warnings.append("Operating flow exceeds pump max flow.")
    elif utilization > 0.85:
        warnings.append("Pump is operating near the high end of its flow range.")
    elif utilization < 0.15:
        warnings.append("Pump is operating at very low flow relative to max flow.")

    if utilization > 0.9:
        warnings.append("Operating point is near the curve tail-off zone.")

    warnings.extend(operating.get("validation_warnings", []))

    return {
        "pump_name": getattr(pump, "name", "Unknown Pump"),
        "max_flow_gpm": max_flow,
        "max_pressure_psi": max_pressure,
        "operating_flow_gpm": safe_float(flow_gpm),
        "operating_pressure_psi": operating["pressure_psi"],
        "flow_utilization_fraction": utilization,
        "curve_source": operating["curve_source"],
        "curve_points": operating["curve_points"],
        "warnings": warnings,
    }


def export_curve_to_csv(pump_name, output_path):
    from database import list_pump_curve_points

    rows = list_pump_curve_points(pump_name)

    with open(output_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([
            "pump_name",
            "flow_gpm",
            "pressure_psi",
            "notes"
        ])

        for row in rows:
            writer.writerow([
                row["pump_name"],
                row["flow_gpm"],
                row["pressure_psi"],
                row["notes"],
            ])

    return output_path


def scale_point(flow, pressure, max_flow, max_pressure, width, height, padding):
    graph_width = width - (padding * 2)
    graph_height = height - (padding * 2)

    x = padding + (flow / max_flow) * graph_width
    y = height - padding - ((pressure / max_pressure) * graph_height)

    return x, y


def build_curve_svg(
    curve_points,
    width=800,
    height=400,
    operating_point=None,
    required_point=None
):
    if not curve_points:
        return "<p>No curve points available.</p>"

    points = sorted(curve_points, key=lambda point: safe_float(point["flow_gpm"]))

    max_flow = max(safe_float(point["flow_gpm"]) for point in points)
    max_pressure = max(safe_float(point["pressure_psi"]) for point in points)

    extra_flows = []
    extra_pressures = []

    if operating_point:
        extra_flows.append(safe_float(operating_point.get("flow_gpm", 0)))
        extra_pressures.append(safe_float(operating_point.get("pressure_psi", 0)))

    if required_point:
        extra_flows.append(safe_float(required_point.get("flow_gpm", 0)))
        extra_pressures.append(safe_float(required_point.get("pressure_psi", 0)))

    if extra_flows:
        max_flow = max(max_flow, max(extra_flows))

    if extra_pressures:
        max_pressure = max(max_pressure, max(extra_pressures))

    if max_flow <= 0:
        max_flow = 1

    if max_pressure <= 0:
        max_pressure = 1

    max_flow *= 1.10
    max_pressure *= 1.10

    padding = 60
    svg_points = []

    for point in points:
        flow = safe_float(point["flow_gpm"])
        pressure = safe_float(point["pressure_psi"])

        x, y = scale_point(
            flow,
            pressure,
            max_flow,
            max_pressure,
            width,
            height,
            padding
        )

        svg_points.append((x, y, flow, pressure))

    polyline = " ".join([f"{x},{y}" for x, y, _, _ in svg_points])

    svg = f"""
<svg width="{width}" height="{height}" style="border:1px solid #999;background:#fff;">

<line x1="{padding}" y1="{height-padding}" x2="{width-padding}" y2="{height-padding}" stroke="black" />
<line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height-padding}" stroke="black" />

<text x="{width/2}" y="{height-10}" text-anchor="middle" font-size="14">Flow (GPM)</text>
<text x="20" y="{height/2}" transform="rotate(-90 20,{height/2})" text-anchor="middle" font-size="14">Pressure (PSI)</text>

<text x="{padding}" y="{height-padding+20}" font-size="11">0</text>
<text x="{width-padding-40}" y="{height-padding+20}" font-size="11">{max_flow:.0f} GPM</text>
<text x="5" y="{padding+5}" font-size="11">{max_pressure:.0f} PSI</text>

<polyline fill="none" stroke="#1976d2" stroke-width="3" points="{polyline}" />
"""

    for x, y, flow, pressure in svg_points:
        svg += f"""
<circle cx="{x}" cy="{y}" r="5" fill="#d32f2f" />
<text x="{x+8}" y="{y-8}" font-size="12">{flow:.0f} / {pressure:.0f}</text>
"""

    if required_point:
        req_flow = safe_float(required_point.get("flow_gpm", 0))
        req_pressure = safe_float(required_point.get("pressure_psi", 0))

        x, y = scale_point(
            req_flow,
            req_pressure,
            max_flow,
            max_pressure,
            width,
            height,
            padding
        )

        svg += f"""
<line x1="{x}" y1="{padding}" x2="{x}" y2="{height-padding}" stroke="#f9a825" stroke-width="2" stroke-dasharray="6,4" />
<line x1="{padding}" y1="{y}" x2="{width-padding}" y2="{y}" stroke="#f9a825" stroke-width="2" stroke-dasharray="6,4" />
<circle cx="{x}" cy="{y}" r="7" fill="#f9a825" />
<text x="{x+10}" y="{y+18}" font-size="13">Required: {req_flow:.0f} GPM / {req_pressure:.0f} PSI</text>
"""

    if operating_point:
        op_flow = safe_float(operating_point.get("flow_gpm", 0))
        op_pressure = safe_float(operating_point.get("pressure_psi", 0))

        x, y = scale_point(
            op_flow,
            op_pressure,
            max_flow,
            max_pressure,
            width,
            height,
            padding
        )

        svg += f"""
<circle cx="{x}" cy="{y}" r="9" fill="#2e7d32" stroke="black" stroke-width="2" />
<text x="{x+12}" y="{y-12}" font-size="14">Operating: {op_flow:.0f} GPM / {op_pressure:.0f} PSI</text>
"""

    svg += """
<rect x="610" y="20" width="170" height="75" fill="white" stroke="#ccc" />
<circle cx="625" cy="40" r="5" fill="#d32f2f" /><text x="638" y="44" font-size="12">Curve point</text>
<circle cx="625" cy="60" r="7" fill="#f9a825" /><text x="638" y="64" font-size="12">Required point</text>
<circle cx="625" cy="80" r="8" fill="#2e7d32" stroke="black" /><text x="638" y="84" font-size="12">Operating point</text>
</svg>
"""

    return svg