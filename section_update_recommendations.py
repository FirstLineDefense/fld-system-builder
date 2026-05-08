def apply_section_update_recommendation(input_data, section_key):
    updated = dict(input_data)
    changes = []

    if section_key == "controls":
        updated["selected_controls"] = [
            {
                "name": "Automation Ready Control Panel",
                "quantity": 1
            }
        ]

        changes.append(
            "Recommended Automation Ready Control Panel for Controls."
        )

    if section_key == "sensors":
        updated["selected_sensors"] = [
            {
                "name": "Tank Level Sensor",
                "quantity": 1
            }
        ]

        changes.append(
            "Recommended Tank Level Sensor for Sensors."
        )

    if section_key == "manifold_branches":
        branches = updated.get("branches", [])

        has_last_line = any(
            branch.get("role") == "last_line"
            for branch in branches
        )

        if not has_last_line:
            next_branch_number = len(branches) + 1

            branches.append({
                "branch_number": next_branch_number,
                "active": True,
                "role": "last_line",
                "priority": 1,
                "pipe_name": "2in PVC Sch40",
                "pipe_length_ft": 80,
                "elevation_change_ft": 0,
                "device_count": 1,
                "devices": [
                    {
                        "name": "Aqualine I125A - Medium Flow",
                        "quantity": 1
                    }
                ],
                "elbow_90_qty": 2,
                "elbow_45_qty": 0,
                "sweep_bend_qty": 0,
                "tee_qty": 1,
                "valve_qty": 1,
                "other_equivalent_length_ft": 0
            })

            updated["branches"] = branches

            changes.append(
                "Added a suggested Last Line / Structure Defense branch."
            )

        if not branches:
            changes.append(
                "Recommendation: add at least one active branch with pipe, device count, length, and elevation."
            )

    if section_key == "water_runtime":
        updated["water_storage_name"] = "Auto Select Water Storage"

        changes.append(
            "Set Water Storage to Auto Select Water Storage."
        )

    if section_key == "system_drive":
        updated["pump_name"] = "Auto Select Pump"
        updated["engine_name"] = "Auto Select Engine"

        changes.append(
            "Set Pump and Engine to Auto Select."
        )

    if section_key == "budget":
        current_budget = float(updated.get("max_budget", 0) or 0)

        if current_budget < 100000:
            updated["max_budget"] = 100000

            changes.append(
                "Raised budget target to $100,000 for preliminary full-system feasibility."
            )

    updated["last_updated_section"] = section_key
    updated["section_update_changes"] = changes

    return updated
