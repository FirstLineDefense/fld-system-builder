from data.components import COMPONENT_LIBRARY
from services.optimizer_service import get_pump_recommendation


def safe_float(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def make_bom_row(component_key, qty, markup_percent):
    component = COMPONENT_LIBRARY[component_key]

    unit_cost = component["unit_cost"]
    internal_total = qty * unit_cost
    client_unit_price = unit_cost * (1 + markup_percent / 100)
    client_total = qty * client_unit_price

    return {
        "item": component["item"],
        "qty": qty,
        "unit_cost": round(unit_cost, 2),
        "internal_total": round(internal_total, 2),
        "client_unit_price": round(client_unit_price, 2),
        "client_total": round(client_total, 2),
        "notes": component["notes"],
    }


def determine_pump_package(project):

    target_gpm = safe_float(project.get("target_gpm"), 0)
    required_pump_psi = safe_float(project.get("required_pump_psi"), 0)
    hydraulic_hp = safe_float(project.get("hydraulic_hp"), 0)

    if hydraulic_hp <= 10 and target_gpm <= 150:
        return {
            "component_key": "pump_package_light",
            "label": "Light-Duty GX390-Class Pump Package",
            "notes": (
                "Suitable for smaller residential systems "
                "with moderate flow and pressure demand."
            )
        }

    elif hydraulic_hp <= 25 and target_gpm <= 350:
        return {
            "component_key": "pump_package_mid",
            "label": "Mid-Range Gorman-Rupp-Class Pump Package",
            "notes": (
                "Recommended for higher-flow wildfire "
                "protection systems with significant "
                "pressure and elevation demand."
            )
        }

    return {
        "component_key": "pump_package_industrial",
        "label": "Industrial High-Output Pump Package",
        "notes": (
            "Required due to very high hydraulic "
            "horsepower and pressure demand."
        )
    }



def build_basic_bom(project):
    markup_percent = project.get("markup_percent", 35)

    target_gpm = safe_float(project.get("target_gpm"), 0)
    elevation_gain_ft = safe_float(project.get("elevation_gain_ft"), 0)

    estimated_head_flow = 35

    sprinkler_qty = max(4, round(target_gpm / estimated_head_flow))

    pvc_length = max(
        150,
        round(
            150
            + (sprinkler_qty * 25)
            + (elevation_gain_ft * 1.5)
        )
    )

    manifold_qty = max(1, round(sprinkler_qty / 6))

    pump_info = determine_pump_package(project)

    rows = [
        make_bom_row(pump_info["component_key"], 1, markup_percent),
        make_bom_row("manifold", manifold_qty, markup_percent),
        make_bom_row("sprinkler_heads", sprinkler_qty, markup_percent),
        make_bom_row("schedule_80_pvc", pvc_length, markup_percent),
        make_bom_row("control_package", 1, markup_percent),
    ]

    for row in rows:

        if row["item"] == "Self-Priming Pump Package":
            row["item"] = pump_info["label"]
            row["notes"] = pump_info["notes"]



        if row["item"] == "Sprinkler / Nozzle Heads":
            row["notes"] = (
                f"Calculated from target flow of "
                f"{target_gpm:.0f} GPM using estimated "
                f"{estimated_head_flow} GPM per head."
            )

        elif row["item"] == "Schedule 80 PVC Main Runs":

            if target_gpm <= 120:
                pipe_info = {
                    "label": '2\" Sch 80 PVC',
                    "unit_cost": 4.5,
                }

            elif target_gpm <= 400:
                pipe_info = {
                    "label": '3\" Sch 80 PVC',
                    "unit_cost": 6.0,
                }

            else:
                pipe_info = {
                    "label": '4\" Sch 80 PVC',
                    "unit_cost": 11.5,
                }

            row["unit_cost"] = pipe_info["unit_cost"]

            row["internal_total"] = round(
                row["qty"] * row["unit_cost"], 2
            )

            row["client_unit_price"] = round(
                row["unit_cost"] * (1 + markup_percent / 100), 2
            )

            row["client_total"] = round(
                row["qty"] * row["client_unit_price"], 2
            )

            row["notes"] = (
                f"{pipe_info['label']} selected from "
                f"{target_gpm:.0f} GPM system demand and "
                f"{elevation_gain_ft:.0f} ft elevation gain."
            )

        elif row["item"] == "Primary Manifold Assembly":

            if target_gpm <= 120:

                manifold_info = {
                    "label": "Light-Duty Residential Manifold",
                    "unit_cost": 850,
                    "zones": 4,
                }

            elif target_gpm <= 400:

                manifold_info = {
                    "label": "Mid-Range Zoned Manifold",
                    "unit_cost": 2250,
                    "zones": 6,
                }

            else:

                manifold_info = {
                    "label": "Industrial Multi-Zone Manifold",
                    "unit_cost": 6800,
                    "zones": 12,
                }

            row["qty"] = max(
                1,
                round(sprinkler_qty / manifold_info["zones"])
            )

            row["unit_cost"] = manifold_info["unit_cost"]

            row["internal_total"] = round(
                row["qty"] * row["unit_cost"], 2
            )

            row["client_unit_price"] = round(
                row["unit_cost"] * (1 + markup_percent / 100), 2
            )

            row["client_total"] = round(
                row["qty"] * row["client_unit_price"], 2
            )

            row["notes"] = (
                f"{manifold_info['label']} using estimated "
                f"{manifold_info['zones']} active zones and "
                f"{sprinkler_qty} sprinkler heads."
            )

        elif row["item"] == "Control / Activation Package":

            if target_gpm <= 120:

                control_info = {
                    "label": "Manual Wildfire Control Package",
                    "unit_cost": 1200,
                    "tier": "V1",
                    "notes": (
                        "Manual startup and basic pressure monitoring."
                    )
                }

            elif target_gpm <= 400:

                control_info = {
                    "label": "Remote Monitoring Control Package",
                    "unit_cost": 4800,
                    "tier": "V2",
                    "notes": (
                        "Remote monitoring, health alerts, and "
                        "basic automation capability."
                    )
                }

            else:

                control_info = {
                    "label": "Industrial Autonomous Protection System",
                    "unit_cost": 18500,
                    "tier": "V4",
                    "notes": (
                        "Industrial automation, sensor integration, "
                        "and autonomous wildfire response capability."
                    )
                }

            row["item"] = control_info["label"]

            row["unit_cost"] = control_info["unit_cost"]

            row["internal_total"] = round(
                row["qty"] * row["unit_cost"], 2
            )

            row["client_unit_price"] = round(
                row["unit_cost"] * (1 + markup_percent / 100), 2
            )

            row["client_total"] = round(
                row["qty"] * row["client_unit_price"], 2
            )

            row["notes"] = (
                f"{control_info['tier']} architecture. "
                f"{control_info['notes']}"
            )

    return rows


def build_project_report(form):
    target_gpm = safe_float(form.get("target_gpm"))
    target_psi = safe_float(form.get("target_psi"))
    elevation_gain_ft = safe_float(form.get("elevation_gain_ft"))

    elevation_psi_loss = elevation_gain_ft * 0.433
    required_pump_psi = target_psi + elevation_psi_loss
    hydraulic_hp = (target_gpm * required_pump_psi) / 1714 if required_pump_psi else 0

    design_hours = safe_float(form.get("design_hours"), 0)
    design_hourly_rate = safe_float(form.get("design_hourly_rate"), 0)
    design_total = design_hours * design_hourly_rate
    maintenance_plan_fee = safe_float(form.get("maintenance_plan_fee"), 0)
    subscription_cost = safe_float(form.get("subscription_cost"), 0)

    project = {
        "project_name": form.get("project_name", ""),
        "client_name": form.get("client_name", ""),
        "water_source": form.get("water_source", ""),
        "target_gpm": target_gpm,
        "target_psi": target_psi,
        "elevation_gain_ft": elevation_gain_ft,
        "elevation_psi_loss": round(elevation_psi_loss, 1),
        "required_pump_psi": round(required_pump_psi, 1),
        "hydraulic_hp": round(hydraulic_hp, 1),
        "markup_percent": safe_float(form.get("markup_percent"), 35),
        "design_hours": design_hours,
        "design_hourly_rate": design_hourly_rate,
        "design_total": round(design_total, 2),
        "maintenance_plan_fee": round(maintenance_plan_fee, 2),
        "subscription_cost": round(subscription_cost, 2),
    }

    project["bom"] = build_basic_bom(project)
    project["internal_bom_total"] = round(sum(row["internal_total"] for row in project["bom"]), 2)
    project["client_bom_total"] = round(sum(row["client_total"] for row in project["bom"]), 2)
    project["client_proposal_total"] = round(
        project["client_bom_total"]
        + project["design_total"]
        + project["maintenance_plan_fee"]
        + project["subscription_cost"],
        2,
    )

    project["optimizer_recommendation"] = get_pump_recommendation(project)

    return project
