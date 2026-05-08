def normalize_violation_key(text):
    text = str(text or "").strip().lower()
    text = text.replace("-", "_").replace(" ", "_")
    while "__" in text:
        text = text.replace("__", "_")
    return text


def classify_constraint_violation(violation):
    if isinstance(violation, dict):
        key = violation.get("key") or violation.get("type") or violation.get("name") or violation.get("message")
        severity = violation.get("severity", "medium")
        message = violation.get("message") or violation.get("description") or str(violation)
    else:
        key = str(violation)
        severity = "medium"
        message = str(violation)

    key = normalize_violation_key(key)

    if any(term in key for term in ["velocity", "fps", "pipe_speed"]):
        family = "hydraulics_velocity"
    elif any(term in key for term in ["pressure", "psi", "head"]):
        family = "hydraulics_pressure"
    elif any(term in key for term in ["pump", "gpm", "flow"]):
        family = "pump_flow"
    elif any(term in key for term in ["motor", "hp", "horsepower", "power"]):
        family = "motor_power"
    elif any(term in key for term in ["cost", "budget", "price"]):
        family = "cost"
    else:
        family = "general"

    return {
        "key": key,
        "family": family,
        "severity": severity,
        "message": message,
    }


def summarize_constraint_violations(violations):
    violations = violations or []
    classified = [classify_constraint_violation(v) for v in violations]

    counts = {}
    for item in classified:
        family = item["family"]
        counts[family] = counts.get(family, 0) + 1

    return {
        "count": len(classified),
        "families": counts,
        "violations": classified,
    }


def get_violation_families(violations):
    summary = summarize_constraint_violations(violations)
    return summary["families"]
