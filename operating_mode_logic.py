def suggest_operating_mode_logic(primary):
    suggestions = []

    operating_mode = (
        primary.get("operating_mode", "")
        or primary.get("mode", "")
        or ""
    ).lower()

    power_source = (
        primary.get("power_source", "")
        or ""
    ).lower()

    if not operating_mode:
        suggestions.append({
            "type": "mode",
            "label": "Operating mode missing",
            "message": "Add an operating mode to improve system intelligence recommendations.",
            "confidence": "medium",
            "icon": "🧠",
            "reason": "Operating mode affects runtime assumptions, resilience strategy, and optimization behavior."
        })

        return suggestions

    if "wildfire" in operating_mode:
        suggestions.append({
            "type": "mode",
            "label": "Wildfire operating profile",
            "message": "Wildfire mode prioritizes runtime resilience, redundancy, survivability, and autonomo operation over efficiency.",
            "confidence": "high",
            "icon": "🔥",
            "reason": "Wildfire defense systems should tolerate infrastructure failure and prolonged runtime conditions."
        })

    if "residential" in operating_mode:
        suggestions.append({
            "type": "mode",
            "label": "Residential operating profile",
            "message": "Residential mode prioritizes quieter operation, lower maintenance burden, and simplified automation.",
            "confidence": "high",
            "icon": "🏠",
            "reason": "Residential systems typically favor ease of ownership and reduced operational complexity."
        })

    if "agricultural" in operating_mode:
        estions.append({
            "type": "mode",
            "label": "Agricultural operating profile",
            "message": "Agricultural mode prioritizes long duty cycles, serviceability, and fuel efficiency.",
            "confidence": "high",
            "icon": "🚜",
            "reason": "Agricultural systems are often expected to run extended hours under continuous load."
        })

    if "hybrid" in operating_mode:
        suggestions.append({
            "type": "mode",
            "label": "Hybrid architecture detected",
            "message": "Hybrid systems should maintain layered fallback paths between grid, generator, and battery systs.",
            "confidence": "high",
            "icon": "🔁",
            "reason": "Resilient wildfire architecture depends on graceful fallback between multiple energy sources."
        })

    if "off-grid" in operating_mode:
        suggestions.append({
            "type": "mode",
            "label": "Off-grid architecture detected",
            "message": "Off-grid systems should prioritize fuel storage, field serviceability, and autonomous restart capability.",
            "confidence": "high",
            "icon": "🏕️",
            "reason": "Off-grid deployments cannot assume utility restoration during emergency conditions."
        })

    if "electric" in power_source and "wildfire" in operating_mode:
        suggestions.append({
            "type": "mode",
            "label": "Grid dependency warning",
            "message": "Pure electric wildfire systems may lose functionality during PSPS or infrastructure failure unless backup energy systems exist.",
            "confidence": "high",
            "icon": "⚠️",
            "reason": "Wildfire events frequently coincide with utility shutoffs and infrastructure instability."
        })

    return suggestions
