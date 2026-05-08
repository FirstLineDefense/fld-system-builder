def suggest_generator_from_engine(primary):
    engine = primary.get("engine", {}) or {}
    motor = primary.get("motor", {}) or {}
    operating_mode = primary.get("operating_mode", "") or primary.get("mode", "")

    suggestions = []

    motor_hp = float(motor.get("horsepower", 0) or 0)
    motor_kw = motor_hp * 0.746 if motor_hp else 0

    if motor_kw > 0:
        running_kw = motor_kw / 0.88
        starting_kw = running_kw * 2.5

        if starting_kw <= 12:
            gen_class = "12 to 15 kW"
        elif starting_kw <= 20:
            gen_class = "20 to 24 kW"
        elif starting_kw <= 30:
            gen_class = "30 to 35 kW"
        elif starting_kw <= 45:
            gen_class = "45 to 50 kW"
        else:
            gen_class = "50 kW plus"

        suggestions.append({
            "type": "generator",
            "label": "Generator sizing",
            "message": f"Suggested generator class: {gen_class}. Estimated running load is about {running_kw:.1f} kW with starting surge around {starting_kw:.1f} kW.",
            "confidence": "medium",
            "icon": "⚡",
            "reason": "Based on motor horsepower, estimated motor efficiency, and conservative pump motor starting surge."
        })

    if "hybrid" in operating_mode.lower():
        suggestions.append({
            "type": "generator",
            "label": "Hybrid fallback logic",
            "message": "Hybrid mode detected. Generator should be sized to carry the pump load directlynot merely recharge batteries.",
            "confidence": "high",
            "icon": "🔁",
            "reason": "For wildfire runtime, generator fallback should preserve battery reserve and support continuous pump operation."
        })

    if not motor_kw and engine:
        suggestions.append({
            "type": "generator",
            "label": "Generator sizing unavailable",
            "message": "No electric motor horsepower found. Generator sizing should be calculated once motor size is selected.",
            "confidence": "low",
            "icon": "⚠️",
            "reason": "Generator sizing depends primarily on electric motor load and starting surge."
        })

    return suggestions
