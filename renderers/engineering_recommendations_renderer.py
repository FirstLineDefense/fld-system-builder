def build_engineering_recommendations_html(recommendations):
    if not recommendations:
        return ""

    html = "<div class='section'>"

    html += "<h2>Engineering Recommendations</h2>"

    severity_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2,
        "Info": 3,
    }

    recommendations = sorted(
        recommendations,
        key=lambda x: severity_order.get(
            x.get("severity", "Info"),
            99
        )
    )

    current_severity = None

    for recommendation in recommendations:
        severity = recommendation.get("severity", "Info")

        if severity != current_severity:
            current_severity = severity
            html += f"<h3>{severity} Priority</h3>"

        html += "<div class='recommendation-card'>"

        html += (
            f"<p><strong>{recommendation.get('title', '')}</strong></p>"
        )

        html += (
            f"<p><strong>Category:</strong> "
            f"{recommendation.get('category', '')}</p>"
        )

        html += (
            f"<p>{recommendation.get('detail', '')}</p>"
        )

        html += (
            f"<p><strong>Action Code:</strong> "
            f"{recommendation.get('action_code', 'REVIEW_RECOMMENDATION')}</p>"
        )

        html += (
            f"<p><strong>Action:</strong> "
            f"{recommendation.get('action_label', 'Review Recommendation')}</p>"
        )

        can_auto_update = recommendation.get("can_auto_update", False)
        action_code = recommendation.get("action_code", "")

        html += (
            f"<p><strong>Auto Update Ready:</strong> "
            f"{can_auto_update}</p>"
        )

        if can_auto_update and action_code:
            html += (
                "<form method='post' action='/builder-v27' style='margin-top:10px;'>"
                f"<input type='hidden' name='action_code' value='{action_code}'>"
                "<button type='submit'>Apply Recommendation</button>"
                "</form>"
            )

        html += "</div>"

    html += "</div>"

    return html
