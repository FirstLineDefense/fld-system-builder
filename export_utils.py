import csv
import json
import os
from datetime import datetime


EXPORT_DIR = "exports"


def ensure_export_dir():
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)


def safe_filename_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def build_report_text(input_data, result):
    primary = result["primary"]
    manifold = primary["manifold"]

    lines = []

    lines.append("===== FLD SYSTEM BUILDER REPORT =====")
    lines.append("")
    lines.append("SYSTEM SUMMARY")
    lines.append(f"System Passed: {primary['summary']['system_passed']}")
    lines.append(f"Selected Pump: {primary['pump'].name if primary['pump'] else 'None'}")
    lines.append(f"Active Branches: {manifold['active_branch_count']}")
    lines.append(f"Max Simultaneous Ports: {manifold['max_simultaneous_ports']}")
    lines.append(f"Total Installed Flow: {manifold['total_installed_flow_gpm']:.2f} GPM")
    lines.append(f"Active Operating Flow: {manifold['total_flow_gpm']:.2f} GPM")
    lines.append(f"Runtime: {primary['runtime']['runtime_minutes']:.2f} minutes")
    lines.append(f"Total Cost: ${primary['cost']['total_cost']:.2f}")
    lines.append(f"Within Budget: {primary['summary']['within_budget']}")
    lines.append("")

    lines.append("WARNINGS")
    if primary["summary"]["warnings"]:
        for warning in primary["summary"]["warnings"]:
            lines.append(f"- {warning}")
    else:
        lines.append("- None")

    lines.append("")
    lines.append("BRANCH RESULTS")

    for branch in manifold["branch_results"]:
        lines.append(
            f"Branch {branch['branch_number']} | "
            f"Role: {branch['role']} | "
            f"Priority: {branch['priority']} | "
            f"Pipe: {branch['pipe_name']} | "
            f"Length: {branch['pipe_length_ft']} ft | "
            f"Elevation: {branch['elevation_change_ft']} ft | "
            f"Flow: {branch['flow']['total_flow_gpm']:.2f} GPM | "
            f"Final PSI: {branch['final_pressure_psi']:.2f} | "
            f"Required PSI: {branch['required_terminal_pressure_psi']:.2f} | "
            f"Margin: {branch['pressure_margin_psi']:.2f} | "
            f"Passed: {branch['passed']}"
        )

    lines.append("")
    lines.append("OPERATING MODE CHECKS")

    for mode in manifold["operating_modes"]["modes"]:
        worst = mode.get("worst_branch")
        worst_branch_number = worst["branch_number"] if worst else "N/A"
        worst_margin = f"{worst['pressure_margin_psi']:.2f}" if worst else "N/A"

        lines.append(
            f"{mode['mode_name']} | "
            f"Passed: {mode['passed']} | "
            f"Branches: {mode['branch_count']} | "
            f"Total Flow: {mode['total_flow_gpm']:.2f} GPM | "
            f"Worst Branch: {worst_branch_number} | "
            f"Worst Margin: {worst_margin}"
        )

    lines.append("")
    lines.append("SELECTED COMPONENTS / CUT SHEET STARTER")

    for item in primary["selected_components"]:
        component = item["component"]
        quantity = item["quantity"]
        line_cost = component.unit_cost * quantity

        lines.append(
            f"{component.name} | "
            f"Type: {component.component_type} | "
            f"Qty: {quantity} | "
            f"Unit Cost: ${component.unit_cost:.2f} | "
            f"Line Cost: ${line_cost:.2f}"
        )

    return "\n".join(lines)


def export_bom_csv(result, filepath):
    primary = result["primary"]

    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([
            "Component",
            "Component Type",
            "Quantity",
            "Unit Cost",
            "Line Cost",
            "Notes"
        ])

        for item in primary["selected_components"]:
            component = item["component"]
            quantity = item["quantity"]
            line_cost = component.unit_cost * quantity

            writer.writerow([
                component.name,
                component.component_type,
                quantity,
                component.unit_cost,
                line_cost,
                component.notes
            ])


def export_branches_csv(result, filepath):
    primary = result["primary"]
    manifold = primary["manifold"]

    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([
            "Branch",
            "Role",
            "Priority",
            "Pipe",
            "Pipe Length Ft",
            "Elevation Change Ft",
            "Flow GPM",
            "Final PSI",
            "Required PSI",
            "Pressure Margin PSI",
            "Passed"
        ])

        for branch in manifold["branch_results"]:
            writer.writerow([
                branch["branch_number"],
                branch["role"],
                branch["priority"],
                branch["pipe_name"],
                branch["pipe_length_ft"],
                branch["elevation_change_ft"],
                branch["flow"]["total_flow_gpm"],
                branch["final_pressure_psi"],
                branch["required_terminal_pressure_psi"],
                branch["pressure_margin_psi"],
                branch["passed"]
            ])


def export_modes_csv(result, filepath):
    primary = result["primary"]
    manifold = primary["manifold"]

    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([
            "Mode",
            "Passed",
            "Branch Count",
            "Total Flow GPM",
            "Worst Branch",
            "Worst Margin PSI"
        ])

        for mode in manifold["operating_modes"]["modes"]:
            worst = mode.get("worst_branch")
            worst_branch_number = worst["branch_number"] if worst else "N/A"
            worst_margin = worst["pressure_margin_psi"] if worst else "N/A"

            writer.writerow([
                mode["mode_name"],
                mode["passed"],
                mode["branch_count"],
                mode["total_flow_gpm"],
                worst_branch_number,
                worst_margin
            ])


def export_report_txt(input_data, result, filepath):
    report_text = build_report_text(input_data, result)

    with open(filepath, "w") as f:
        f.write(report_text)


def write_latest_design_snapshot(input_data, result):
    primary = result.get("primary", {}) or {}
    manifold = primary.get("manifold", {}) or {}

    pump = primary.get("pump")
    motor = primary.get("motor") or primary.get("engine")

    pump_data = {
        "name": getattr(pump, "name", None) or "Unknown Pump",
        "gpm": getattr(pump, "gpm", None) or getattr(pump, "flow_gpm", None),
        "cost": getattr(pump, "cost", None),
    }

    motor_data = {
        "name": getattr(motor, "name", None) or "Unknown Motor",
        "hp": getattr(motor, "hp", None) or getattr(motor, "horsepower", None),
        "cost": getattr(motor, "cost", None),
    }

    branches = []

    input_branches = input_data.get("branches", []) or []
    result_branches = manifold.get("branch_results", []) or []

    for index, branch_result in enumerate(result_branches, start=1):
        source = input_branches[index - 1] if index - 1 < len(input_branches) else {}

        flow = branch_result.get("flow", {}) or {}

        branches.append(
            {
                "branch_number": branch_result.get("branch_number", index),
                "name": source.get("name") or source.get("role") or f"Branch {index}",
                "role": branch_result.get("role") or source.get("role"),
                "priority": branch_result.get("priority") or source.get("priority"),
                "pipe_name": branch_result.get("pipe_name"),
                "pipe_size": source.get("pipe_size"),
                "pipe_type": source.get("pipe_type"),
                "pipe_length_ft": branch_result.get("pipe_length_ft") or source.get("pipe_length_ft"),
                "elevation_change_ft": branch_result.get("elevation_change_ft") or source.get("elevation_change_ft"),
                "target_gpm": flow.get("total_flow_gpm") or source.get("target_gpm"),
                "final_pressure_psi": branch_result.get("final_pressure_psi"),
                "required_terminal_pressure_psi": branch_result.get("required_terminal_pressure_psi"),
                "pressure_margin_psi": branch_result.get("pressure_margin_psi"),
                "velocity_fps": branch_result.get("velocity_fps") or source.get("velocity_fps"),
                "passed": branch_result.get("passed"),
                "sprinkler_count": source.get("sprinkler_count", 0),
                "elbow_90_qty": source.get("elbow_90_qty", 0),
                "tee_qty": source.get("tee_qty", 0),
                "valve_qty": source.get("valve_qty", 1),
            }
        )

    summary = primary.get("summary", {}) or {}
    runtime = primary.get("runtime", {}) or {}
    cost = primary.get("cost", {}) or {}

    snapshot = {
        "source": "write_export_files",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "pump": pump_data,
        "motor": motor_data,
        "branches": branches,
        "summary": {
            "system_passed": summary.get("system_passed"),
            "within_budget": summary.get("within_budget"),
            "warnings": summary.get("warnings", []),
            "runtime_minutes": runtime.get("runtime_minutes"),
            "total_cost": cost.get("total_cost"),
            "total_installed_flow_gpm": manifold.get("total_installed_flow_gpm"),
            "total_flow_gpm": manifold.get("total_flow_gpm"),
            "active_branch_count": manifold.get("active_branch_count"),
            "max_simultaneous_ports": manifold.get("max_simultaneous_ports"),
        },
        "optimizer_result": result.get("optimizer_result"),
    }

    latest_path = os.path.join(EXPORT_DIR, "latest_design.json")
    with open(latest_path, "w") as f:
        json.dump(snapshot, f, indent=2, default=str)


def write_export_files(input_data, result):
    ensure_export_dir()

    stamp = safe_filename_timestamp()

    bom_filename = f"fld_bom_{stamp}.csv"
    branches_filename = f"fld_branches_{stamp}.csv"
    modes_filename = f"fld_modes_{stamp}.csv"
    report_filename = f"fld_report_{stamp}.txt"

    bom_path = os.path.join(EXPORT_DIR, bom_filename)
    branches_path = os.path.join(EXPORT_DIR, branches_filename)
    modes_path = os.path.join(EXPORT_DIR, modes_filename)
    report_path = os.path.join(EXPORT_DIR, report_filename)

    export_bom_csv(result, bom_path)
    export_branches_csv(result, branches_path)
    export_modes_csv(result, modes_path)
    export_report_txt(input_data, result, report_path)
    write_latest_design_snapshot(input_data, result)

    return {
        "bom": f"/exports/{bom_filename}",
        "branches": f"/exports/{branches_filename}",
        "modes": f"/exports/{modes_filename}",
        "report": f"/exports/{report_filename}",
    }