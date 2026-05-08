from copy import deepcopy
import math
import random


TARGET_VELOCITY = 6.0

DIAMETER_STEPS = [
    0.5,
    1.0,
    1.5,
    2.0,
    2.5,
    3.0,
    3.5,
    4.0
]


def calculate_velocity(gpm, diameter):
    area = math.pi * (diameter / 2) ** 2

    if area <= 0:
        return 0

    return (gpm * 0.4085) / area


def find_candidate_diameters(gpm):
    candidates = []

    for diameter in DIAMETER_STEPS:
        velocity = calculate_velocity(gpm, diameter)

        candidates.append({
            "diameter": diameter,
            "velocity": round(velocity, 2),
            "distance": abs(TARGET_VELOCITY - velocity)
        })

    return sorted(candidates, key=lambda x: x["distance"])


def mutate_branch_diameters(candidate):
    mutated = deepcopy(candidate)
    primary = mutated.get("primary", {}) or {}
    branches = primary.get("branches", []) or []

    for branch in branches:
        gpm = branch.get("target_gpm", 0) or 0

        options = find_candidate_diameters(gpm)
        top_options = options[:4]

        selected = random.choice(top_options)

        branch["pipe_diameter_in"] = selected["diameter"]
        branch["velocity_fps"] = selected["velocity"]
        branch["diameter_mutated"] = True

    primary["branches"] = branches
    mutated["primary"] = primary

    return mutated


def mutate_branch_flow(candidate):
    mutated = deepcopy(candidate)
    primary = mutated.get("primary", {}) or {}
    branches = primary.get("branches", []) or []

    for branch in branches:
        current_gpm = float(branch.get("target_gpm", 0) or 0)

        if current_gpm <= 0:
            continue

        factor = random.choice([
            0.75,
            0.85,
            0.95,
            1.05,
            1.15,
            1.25
        ])

        new_gpm = round(current_gpm * factor, 1)

        branch["target_gpm"] = new_gpm
        branch["flow_mutated"] = True

        diameter = float(branch.get("pipe_diameter_in", 1.0) or 1.0)
        branch["velocity_fps"] = round(
            calculate_velocity(new_gpm, diameter),
            2
        )

    primary["branches"] = branches
    mutated["primary"] = primary

    return mutated


def mutate_branch_hydraulics(candidate):
    mutated = deepcopy(candidate)

    if random.random() < 0.65:
        mutated = mutate_branch_diameters(mutated)

    if random.random() < 0.45:
        mutated = mutate_branch_flow(mutated)

    return mutated
