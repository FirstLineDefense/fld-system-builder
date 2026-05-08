def parse_bulk_curve_text(
    raw_text
):
    curves = []

    current_curve = None

    for raw_line in raw_text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("PUMP:"):
            if current_curve:
                curves.append(current_curve)

            current_curve = {
                "pump_name":
                    line.replace(
                        "PUMP:",
                        ""
                    ).strip(),

                "points": [],
            }

            continue

        if current_curve is None:
            continue

        if "," not in line:
            continue

        parts = [
            p.strip()
            for p in line.split(",")
        ]

        if len(parts) < 2:
            continue

        try:
            gpm = float(parts[0])
            psi = float(parts[1])

        except Exception:
            continue

        current_curve[
            "points"
        ].append(
            {
                "gpm": gpm,
                "psi": psi,
            }
        )

    if current_curve:
        curves.append(current_curve)

    return curves
