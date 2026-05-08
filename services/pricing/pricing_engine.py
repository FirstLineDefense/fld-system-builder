from typing import Dict, Any


def calculate_component_cost(component: Dict[str, Any]) -> float:
    cost = float(component.get("cost", 0))
    qty = float(component.get("quantity", 1))
    return cost * qty


def calculate_base_cost(package: Dict[str, Any]) -> float:
    components = package.get("components", []) or []
    return sum(calculate_component_cost(c) for c in components)


def calculate_labor_cost(package: Dict[str, Any]) -> float:
    design_hours = float(package.get("design_hours", 0))
    hourly_rate = float(package.get("labor_rate", 150))
    return design_hours * hourly_rate


def apply_markup(cost: float, markup_percent: float) -> float:
    return cost * (1 + markup_percent / 100.0)


def generate_pricing_summary(package: Dict[str, Any]) -> Dict[str, Any]:
    markup_percent = float(package.get("markup_percent", 30))

    base_cost = calculate_base_cost(package)
    labor_cost = calculate_labor_cost(package)

    internal_cost = base_cost + labor_cost
    client_price = apply_markup(internal_cost, markup_percent)

    return {
        "internal": {
            "base_cost": base_cost,
            "labor_cost": labor_cost,
            "total_internal_cost": internal_cost,
        },
        "client": {
            "markup_percent": markup_percent,
            "final_price": client_price,
        }
    }
