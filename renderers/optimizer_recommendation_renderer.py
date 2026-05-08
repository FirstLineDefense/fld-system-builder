def build_optimizer_recommendation_html(optimizer_result):
    if not optimizer_result:
        return ""

    summary = optimizer_result.get("summary", {}) or {}

    status = summary.get(
        "optimizer_status",
        "optimizer status unavailable"
    )

    source = summary.get(
        "recommended_candidate_source",
        "unknown"
    )

    original_score = summary.get(
        "original_input_score",
        "N/A"
    )

    best_score = summary.get(
        "best_score",
        "N/A"
    )

    improvement = summary.get(
        "true_total_improvement",
        "N/A"
    )

    if source == "original_input":
        recommendation = (
            "Keep the original System Builder input. "
            "The optimizer tested alternatives, but none "
            "scored better than the current design."
        )

        recommendation_class = "section section-green"

    elif source == "evolved_candidate":
        recommendation = (
            "Review the evolved optimizer candidate. "
            "It scored better than the original input "
            "and may be worth applying manually."
        )

        recommendation_class = "section section-yellow"

    else:
        recommendation = "Review optimizer output manually."

        recommendation_class = "section section-yellow"

    html = f"""
    <div class="{recommendation_class}">
    <h2>Optimizer Recommendation</h2>
    """

    html += f"<p><strong>Status:</strong> {status}</p>"
    html += f"<p><strong>Recommended Source:</strong> {source}</p>"
    html += f"<p><strong>Original Input Score:</strong> {original_score}</p>"
    html += f"<p><strong>Recommended Score:</strong> {best_score}</p>"
    html += f"<p><strong>True Improvement:</strong> {improvement}</p>"

    html += (
        f"<p><strong>Recommendation:</strong> "
        f"{recommendation}</p>"
    )

    html += "</div>"

    return html
