def suggest_battery_from_motor(primary):
    motor = primary.get("motor", {}) or {}
    operating_mode = primary.get("operating_mode", "") or primary.get("mode", "")
    runtime_minutes = float(primary.get("runtime_minutes", 0) or 0)

    suggestions = []

    motor_hp = float(motor.get("horsepower", 0) or 0)
    motor_kw = motor_hp * 0.746 if motor_hp else 0

    if not motor_kw:
        suggestions.append({
            "type": "battery",
            "label": "Battery sizing unavailable",
            "message": "No electric motor horsepower found. Battery sizing should be calculated once motor size is selected.",
            "confidence": "low",
            "icon": "🔋",
            "reason": "Battery sizing depends on motor load, runtime target, inverter losses, and reserve margin."
        })
        return suggestions

    if runtime_minutes <= 0:
        runtime_minutes = 30

    runtime_hours = runtime_minutes / 60
    inverter_efficiency = 0.90
    reserve_factor = 1.3
    running_kw = motor_kw / inverter_efficiency
    battery_kwh = running_kw * runtime_hours * reserve_factor

    if battery_kwh <= 10:
        battery_class = "10 kWh class"
    elif battery_kwh <= 20:
        battery_class = "20 kWh class"
    elif battery_kwh <= 40:
        battery_class = "40 kWh class"
    elif battery_kwh <= 60:
        battery_class = "60 kWh class"
    else:
        battery_class = "60 kWh plus"

    suggestions.append({
        "type": "battery",
        "label": "Battery sizing",
        "message": f"Suggested battery class: {battery_class}. Estimated usable requirement is about {battery_kwh:.1f} kWh for {runtime_minutes:.0f} minutes of pump operation.",
        "confidence": "medium",
        "icon": "🔋",
        "reason": "Based on electric motor horsepower, inverter loss, target runtime, and reserve margin."
    })

    if "hybrid" in operating_mode.lower():
        suggestions.append({
            "type": "battery",
            "label": "Hybrid battery role",
            "message": "Hybrid mode detected. Battery should be treated as bridge power and control reserve, not the primary long-duration pump energy source.",
            "confidence": "high",
            "icon": "🧠",
            "reason": "For wildfire defense, batteries are best used to support startup, controls, comms, transition time, and short outages while generator or grid power carries sustained pump load."
        })

    return suggestions
