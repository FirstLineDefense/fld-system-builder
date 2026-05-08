def apply_auto_update_action(input_data, action_code):
    """
    Applies a structured auto-update action to the current design inputs.

    Returns:
    {
        "updated_input_data": ...,
        "changes": [...],
        "success": True/False,
    }
    """

    updated = dict(input_data)

    changes = []

    success = False

    branches = updated.get("branches", [])

    if action_code == "ADD_LAST_LINE_BRANCH":

        existing_last_line = any(
            branch.get("role") == "last_line"
            for branch in branches
        )

        if not existing_last_line:

            new_branch = {
                "active": True,
                "role": "last_line",
                "priority": 1,
                "pipe_name": "2in PVC Sch40",
                "pipe_length_ft": 80,
                "elevation_change_ft": 0,
                "device_count": 2,
                "devices": [
                    {
                        "name": "Aqualine I125A - Medium Flow",
                        "quantity": 2,
                    }
                ],
                "elbow_90_qty": 2,
                "elbow_45_qty": 0,
                "sweep_bend_qty": 0,
                "tee_qty": 1,
                "valve_qty": 1,
                "other_equivalent_length_ft": 0,
            }

            branches.append(new_branch)

            updated["branches"] = branches

            changes.append(
                "Added default Last Line / Structure Defense branch."
            )

            success = True

    elif action_code == "ADD_FOAM_BRANCH":

        existing_foam = any(
            branch.get("role") == "foam"
            for branch in branches
        )

        if not existing_foam:

            new_branch = {
                "active": True,
                "role": "foam",
                "priority": 3,
                "pipe_name": "1.5in PVC Sch40",
                "pipe_length_ft": 50,
                "elevation_change_ft": 0,
                "device_count": 1,
                "devices": [
                    {
                        "name": "Foam Cannon",
                        "quantity": 1,
                    }
                ],
                "elbow_90_qty": 1,
                "elbow_45_qty": 0,
                "sweep_bend_qty": 0,
                "tee_qty": 0,
                "valve_qty": 1,
                "other_equivalent_length_ft": 0,
            }

            branches.append(new_branch)

            updated["branches"] = branches

            changes.append(
                "Added default Foam branch."
            )

            success = True

    return {
        "updated_input_data": updated,
        "changes": changes,
        "success": success,
    }