def suggest_fuel_storage_from_engine(primary):
    engine = primary.get("engine", {}) or {}
    operating_mode = primary.get("operating_mode", "") or primary.get("mode", "")
    runtime_minutes = float(primary.get("runtime_minutes", 0) or 0)

    suggestions = []

    engine_hp = float(engine.get("horsepower", 0) or engine.get("hp", 0) or 0)

    fuel_type = (
        engine.get("fuel_type", "")
        or engine.get("fuel", "")
        or primary.get("fuel_type", "")
        or ""
    ).lower()

    if runtime_minutes <= 0:
        runtime_minutes = 60

    runtime_hours = runtime_minutes / 60

    if not engine_hp:
        suggestions.append({
            "type": "fuel",
            "label": "Fuel storage unavailable",
            "message": "No engine horsepower found. Fuel runtime should be calculated once engine size is selected.",
            "confidence": "low",
            "icon": "⛽",
            "reason": "Fuel storage depends on engine horsepower, fuel type, load facto and runtime target."
        })
        return suggestions

    if not fuel_type:
        suggestions.append({
            "type": "fuel",
            "label": "Fuel type needed",
            "message": "Engine horsepower is known, but fuel type is missing. Add gasoline, propane, or diesel to calculate fuel storage.",
            "confidence": "low",
            "icon": "⛽",
            "reason": "Different fuels have different burn rates and storage requirements."
        })
        return suggestions

    load_factor = 0.75

    if "propane" in fuel_type or "lp" in fuel_type or "lpg" in fuel_type:
        gallons_per_hp_hour = 0.095
        fuel_label = "propane"

    elif "diesel" in fuel_type:
        gallons_per_hp_hour = 0.055
        fuel_label = "diesel"

    elif "gas" in fuel_type:
        gallons_per_hp_hour = 0.075
        fuel_label = "gasoline"

    else:
        suggestions.append({
            "type": "fuel",
          "label": "Fuel type not recognized",
            "message": f"Fuel type '{fuel_type}' was detected, but only gasoline, propane, and diesel are currently modeled.",
            "confidence": "low",
            "icon": "⚠️",
            "reason": "The fuel model needs a known fuel type to estimate runtime."
        })
        return suggestions

    estimated_gallons = (
        engine_hp
        * load_factor
        * gallons_per_hp_hour
        * runtime_hours
    )

    recommended_gallons = estimated_gallons * 1.30

    suggestions.append({
        "type": "fuel",
        "label": "Fuel storage sizing",
        "message": f"For {runtime_minutes:.0f} minutes of runtime, estimated {fuel_label} need is about {estimated_gallons:.1f} gallons. Recommended storage with reserve is about {recommended_gallons:.1f} gallons.",
        "confidence": "medium",
        "icon": "⛽",
        "reason": "Based on engine horsepower, estimated 75 percent operating load, fuel burn approximation, and 30 percent reserve."
    })

    if "hybrid" in operating_mode.lower():
        suggestions.append({
            "type": "fuel",
            "label": "Hybrid fuel reserve",
            "message": "Hybrid mode detected. Fuel storage should support sustained pump operation after grid or primary energy loss.",
            "confidence": "high",
            "icon": "🔁",
            "reason": "In hybrid wildfire mode, generator or engine fuel becomes the long-duration runtime limiter."
        })

    return suggestions
