from optimization_goals import get_goal_weights
from pressure_score import score_pressure_performance


def score_hydraulics(primary):
    branches = primary.get("branches", []) or []

    score = 100
    notes = []

    if not branches:
        return 50, "branch data missing"

    for branch in branches:

        velocity = float(
            branch.get("velocity_fps", 0) or 0
        )

        loss = float(
            branch.get("friction_loss_psi", 0)
            or branch.get("loss_psi", 0)
            or 0
        )

        if velocity > 5:

            excess = velocity - 5

            penalty = round(
                (excess ** 1.4) * 2.5,
                1
            )

            penalty = min(40, penalty)

            score -= penalty

            notes.append(
                f"velocity penalty {penalty}"
            )

        if loss > 5:

            excess_loss = loss - 5

            penalty = round(
                (excess_loss ** 1.3) * 2.0,
                1
            )

            penalty = min(35, penalty)

            score -= penalty

            notes.append(
                f"friction penalty {penalty}"
            )

    score = max(0, min(100, score))

    return (
        score,
        ", ".join(notes)
        if notes
        else "hydraulics stable"
    )


def score_pump_matching(primary):

    pump = primary.get("pump", {}) or {}

    branches = primary.get("branches", []) or []

    pump_gpm = (
        pump.get("gpm", 0) or 0
    )

    total_branch_gpm = 0

    for branch in branches:

        total_branch_gpm += (
            branch.get("target_gpm", 0) or 0
        )

    if not pump_gpm or not total_branch_gpm:
        return 70, "pump matching incomplete"

    ratio = (
        total_branch_gpm / pump_gpm
    )

    deviation = abs(1.0 - ratio)

    penalty = round(
        (deviation ** 1.8) * 140,
        1
    )

    penalty = min(70, penalty)

    score = 100 - penalty

    # reward practical pump reserve instead of treating exact 1.0
    # as the only ideal. Wildfire systems should not be razor-thin.
    if 0.55 <= ratio <= 0.85:
        reserve_bonus = 8
        score += reserve_bonus
        note = "pump has useful reserve"

    elif ratio > 1.15:
        reserve_bonus = 0
        note = "pump undersized"

    elif ratio < 0.45:
        reserve_bonus = 0
        score -= 8
        note = "pump heavily oversized"

    elif ratio < 0.75:
        reserve_bonus = 0
        note = "pump oversized"

    else:
        reserve_bonus = 0
        note = "pump well matched"

    return (
        max(0, min(100, score)),
        f"{note}, ratio={round(ratio,2)}, reserve_bonus={reserve_bonus}"
    )


def score_runtime(primary):

    runtime_minutes = float(
        primary.get("runtime_minutes", 0) or 0
    )

    storage = float(
        primary.get("water_gallons", 0)
        or primary.get("storage_gallons", 0)
        or 0
    )

    score = 100
    notes = []

    if runtime_minutes <= 0:
        score -= 30
        notes.append("runtime missing")

    if storage <= 0:
        score -= 30
        notes.append("storage missing")

    if runtime_minutes and runtime_minutes < 60:
        score -= 20
        notes.append("short runtime")

    elif runtime_minutes >= 480:
        notes.append("long runtime")

    score = max(0, min(100, score))

    return (
        score,
        ", ".join(notes)
        if notes
        else "runtime stable"
    )


def score_resilience(primary):

    operating_mode = (
        primary.get("operating_mode", "")
        or primary.get("mode", "")
        or ""
    ).lower()

    engine = primary.get("engine", {}) or {}
    motor = primary.get("motor", {}) or {}

    score = 100
    notes = []

    if (
        "wildfire" in operating_mode
        and "hybrid" not in operating_mode
    ):
        score -= 20
        notes.append(
            "wildfire without hybrid fallback"
        )

    if not engine and not motor:
        score -= 25
        notes.append("power source missing")

    if "hybrid" in operating_mode:
        notes.append("hybrid architecture")

    score = max(0, min(100, score))

    return (
        score,
        ", ".join(notes)
        if notes
        else "resilience stable"
    )



def score_cost_simplicity(primary):

    score = 100

    notes = []

    branches = primary.get(
        "branches",
        []
    ) or []

    total_pipe_penalty = 0

    for branch in branches:

        diameter = float(
            branch.get(
                "pipe_diameter_in",
                1.0
            ) or 1.0
        )

        # nonlinear cost scaling
        # abs() prevents fractional powers of sub-1.0 diameters
        # from creating complex numbers during mutation.
        # stronger multiplier prevents oversized pipe from looking free.
        penalty = round(
            (abs(diameter - 1.0) ** 1.8) * 14,
            1
        )

        total_pipe_penalty += penalty

    score -= total_pipe_penalty

    if total_pipe_penalty > 0:
        notes.append(
            f"pipe cost penalty {round(total_pipe_penalty,1)}"
        )

    if len(branches) > 6:
        score -= 10
        notes.append(
            "many branches"
        )

    score = max(0, min(100, score))

    return (
        score,
        ", ".join(notes)
        if notes
        else "cost efficient"
    )


def calculate_weighted_design_score(
    primary,
    weights=None
):

    if weights is None:

        goal = (
            primary.get("optimization_goal", "")
            or "balanced"
        )

        weights = get_goal_weights(goal)

    categories = {

        "hydraulics":
            score_hydraulics(primary),

        "pump_matching":
            score_pump_matching(primary),

        "pressure":
            score_pressure_performance(primary),

        "runtime":
            score_runtime(primary),

        "resilience":
            score_resilience(primary),

        "cost_simplicity":
            score_cost_simplicity(primary)
    }

    total = 0

    for key, value in categories.items():

        category_score = value[0]

        weight = weights.get(
            key,
            0.2
        )

        total += (
            category_score * weight
        )

    return {
        "overall_score": round(total, 1),
        "categories": categories,
        "weights": weights
    }
