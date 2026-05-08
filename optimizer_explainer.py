def explain_optimizer_decision(summary):
    if not summary:
        return [
            "Optimizer summary was not available."
        ]

    explanations = []

    source = summary.get(
        "recommended_candidate_source",
        "unknown"
    )

    original_score = summary.get(
        "original_input_score",
        0
    ) or 0

    best_score = summary.get(
        "best_score",
        0
    ) or 0

    improvement = summary.get(
        "true_total_improvement",
        0
    ) or 0

    best_branch = summary.get(
        "best_branch",
        {}
    ) or {}

    best_pump = summary.get(
        "best_pump",
        {}
    ) or {}

    velocity = best_branch.get(
        "velocity_fps",
        None
    )

    pipe_diameter = best_branch.get(
        "pipe_diameter_in",
        None
    )

    pump_gpm = best_pump.get(
        "gpm",
        None
    )

    if source == "original_input":
        explanations.append(
            "The original System Builder input remained the safest recommendation because the optimizer did not find a higher-scoring evolved candidate."
        )

    elif source == "evolved_candidate":
        explanations.append(
            "The optimizer found an evolved candidate with a stronger weighted score than the original input."
        )

    else:
        explanations.append(
            "The optimizer recommendation source was unclear, so the result should be reviewed manually."
        )

    explanations.append(
        f"Original score: {original_score}. Recommended score: {best_score}. True improvement: {improvement}."
    )

    if velocity is not None:
        if velocity <= 7:
            explanations.append(
                f"The recommended branch velocity is {velocity} ft/s, which is within the preferred hydraulic range."
            )
        elif velocity <= 10:
            explanations.append(
                f"The recommended branch velocity is {velocity} ft/s, which is usable but should be reviewed for friction loss and noise."
            )
        else:
            explanations.append(
                f"The recommended branch velocity is {velocity} ft/s, which is high and may indicate a pipe sizing issue."
            )

    if pipe_diameter is not None:
        explanations.append(
            f"The recommended branch pipe diameter is {pipe_diameter} inches."
        )

    if pump_gpm is not None:
        explanations.append(
            f"The recommended pump flow basis is {pump_gpm} GPM."
        )

    return explanations


def build_optimizer_explanation_html(optimizer_result):
    if not optimizer_result:
        return ""

    summary = optimizer_result.get(
        "summary",
        {}
    ) or {}

    explanations = explain_optimizer_decision(
        summary
    )

    html = """
    <div class="section section-yellow">
    <h2>Why The Optimizer Chose This</h2>
    <ul>
    """

    for item in explanations:
        html += f"<li>{item}</li>"

    html += """
    </ul>
    </div>
    """

    return html
