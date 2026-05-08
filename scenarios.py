def generate_scenarios(base_input, evaluate_system_function, component_library):
    max_budget = base_input.get("max_budget", None)

    scenario_definitions = [
        {
            "name": "Low Cost",
            "description": "Minimum viable system with lower pressure margin.",
            "minimum_pressure_margin_psi": 10,
            "strategy": "lowest_cost"
        },
        {
            "name": "Medium",
            "description": "Balanced system with moderate pressure margin.",
            "minimum_pressure_margin_psi": 20,
            "strategy": "balanced"
        },
        {
            "name": "High End",
            "description": "Higher margin system with stronger pump preference.",
            "minimum_pressure_margin_psi": 30,
            "strategy": "high_end"
        }
    ]

    scenario_results = []

    for scenario in scenario_definitions:
        scenario_input = base_input.copy()
        scenario_input["minimum_pressure_margin_psi"] = scenario["minimum_pressure_margin_psi"]
        scenario_input["scenario_strategy"] = scenario["strategy"]

        result = evaluate_system_function(scenario_input, component_library)

        total_cost = result["cost"]["total_cost"]

        if max_budget is None:
            within_budget = None
            budget_margin = None
        else:
            within_budget = total_cost <= max_budget
            budget_margin = max_budget - total_cost

        scenario_results.append({
            "name": scenario["name"],
            "description": scenario["description"],
            "strategy": scenario["strategy"],
            "minimum_pressure_margin_psi": scenario["minimum_pressure_margin_psi"],
            "system_passed": result["summary"]["system_passed"],
            "selected_pump": result["pump"].name if result["pump"] else None,
            "selected_pipe": result["pipe"].name if result["pipe"] else None,
            "final_pressure_psi": result["pressure"]["final_pressure_psi"],
            "pressure_margin_psi": result["pressure"]["pressure_margin_psi"],
            "runtime_minutes": result["runtime"]["runtime_minutes"],
            "total_cost": total_cost,
            "max_budget": max_budget,
            "within_budget": within_budget,
            "budget_margin": budget_margin
        })

    return scenario_results