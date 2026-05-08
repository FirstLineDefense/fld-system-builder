PHASE_1_FINISH_LINE = {
    "name": "FLD Evolutionary Design Engine - Phase 1",
    "goal": (
        "Stabilize the optimizer so it can evaluate, mutate, "
        "score, preserve, and explain candidate improvements."
    ),
    "must_have": [
        "stable candidate structure",
        "weighted scoring",
        "adaptive mutation",
        "hydraulic recalculation",
        "survivor memory",
        "elite memory",
        "generation cycles",
        "human-readable explanation",
        "Flask UI integration"
    ],
    "do_not_expand_yet": [
        "terrain-aware GIS",
        "full cost database",
        "real pump curve libraries",
        "sensor automation",
        "Monte Carlo simulation",
        "AI architecture generation"
    ]
}


def get_phase1_finish_line():
    return PHASE_1_FINISH_LINE
