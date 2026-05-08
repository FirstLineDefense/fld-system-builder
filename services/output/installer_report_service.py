from datetime import datetime


def _line():
    return "-" * 72


def _section(title):
    return f"\n{_line()}\n{title}\n{_line()}\n"


def generate_installer_report(
    project,
    hydraulic_summary=None,
    cut_list=None,
    bom=None,
    warnings=None,
    recommendations=None,
):
    hydraulic_summary = hydraulic_summary or {}
    cut_list = cut_list or {}
    bom = bom or {}
    warnings = warnings or []
    recommendations = recommendations or []

    primary = project.get("primary", {}) or {}

    report = []

    report.append(_line())
    report.append("FLD INSTALLER REPORT")
    report.append(_line())

    report.append(
        f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"
    )

    report.append("")

    pump = primary.get("pump", {}) or {}
    motor = primary.get("motor", {}) or {}

    report.append(_section("SYSTEM OVERVIEW"))

    report.append(
        f"Pump: {pump.get('name') or pump.get('model') or 'Not selected'}"
    )

    report.append(
        f"Motor/Engine: {motor.get('name') or motor.get('model') or 'Not selected'}"
    )

    branches = primary.get("branches", []) or []

    report.append(f"Zones/Branches: {len(branches)}")

    report.append(_section("HYDRAULIC SUMMARY"))

    for key, value in hydraulic_summary.items():
        report.append(f"{key}: {value}")

    report.append(_section("BILL OF MATERIALS"))

    bom_items = bom.get("items", []) or []

    for item in bom_items:
        report.append(
            f"[{item['category']}] "
            f"{item['item']} | "
            f"{item['quantity']} {item['unit']}"
        )

    report.append(_section("CUT LIST"))

    cut_items = cut_list.get("items", []) or []

    for item in cut_items:
        report.append(
            f"{item['location']} | "
            f"{item['item']} | "
            f"{item['quantity']} {item['unit']}"
        )

    report.append(_section("WARNINGS"))

    if warnings:
        for warning in warnings:
            report.append(f"- {warning}")
    else:
        report.append("No active warnings.")

    report.append(_section("RECOMMENDATIONS"))

    if recommendations:
        for rec in recommendations:
            report.append(f"- {rec}")
    else:
        report.append("No recommendations available.")

    report.append("\nEND OF REPORT\n")

    return "\n".join(report)
