def attach_recommendation_actions(recommendations):
    """
    Converts human-readable engineering recommendations into structured action codes.

    These action codes are the bridge toward future Update button behavior.
    """

    updated_recommendations = []

    for recommendation in recommendations:
        title = recommendation.get("title", "")
        detail = recommendation.get("detail", "")
        category = recommendation.get("category", "")

        combined_text = f"{title} {detail} {category}".lower()

        action_code = "REVIEW_RECOMMENDATION"
        action_label = "Review Recommendation"
        can_auto_update = False

        if "last line" in combined_text or "structure defense" in combined_text or "structure-defense" in combined_text:
            action_code = "ADD_LAST_LINE_BRANCH"
            action_label = "Add Last-Line Branch"
            can_auto_update = True

        elif "foam" in combined_text:
            action_code = "ADD_FOAM_BRANCH"
            action_label = "Add Foam Branch"
            can_auto_update = True

        elif "low pressure margin" in combined_text:
            action_code = "IMPROVE_BRANCH_PRESSURE_MARGIN"
            action_label = "Improve Branch Pressure Margin"
            can_auto_update = False

        elif "velocity is high" in combined_text or "high velocity" in combined_text:
            action_code = "UPSIZE_BRANCH_PIPE"
            action_label = "Upsize Branch Pipe"
            can_auto_update = False

        elif "high friction loss" in combined_text or "friction loss" in combined_text:
            action_code = "REDUCE_BRANCH_FRICTION"
            action_label = "Reduce Branch Friction"
            can_auto_update = False

        elif "pump is near maximum" in combined_text or "near maximum flow" in combined_text:
            action_code = "INCREASE_PUMP_CAPACITY"
            action_label = "Increase Pump Capacity"
            can_auto_update = False

        elif "pump may be oversized" in combined_text or "oversized" in combined_text:
            action_code = "REVIEW_PUMP_DOWNSIZE"
            action_label = "Review Pump Sizing"
            can_auto_update = False

        elif "budget" in combined_text:
            action_code = "REVIEW_BUDGET"
            action_label = "Review Budget"
            can_auto_update = False

        elif "proposal-ready" in combined_text or "proposal ready" in combined_text:
            action_code = "RESOLVE_MATURITY_GATES"
            action_label = "Resolve Maturity Gates"
            can_auto_update = False

        recommendation["action_code"] = action_code
        recommendation["action_label"] = action_label
        recommendation["can_auto_update"] = can_auto_update

        updated_recommendations.append(recommendation)

    return updated_recommendations