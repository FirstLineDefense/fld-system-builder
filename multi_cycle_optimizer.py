from optimizer_candidates import generate_optimization_candidates
from optimizer_engine import create_optimizer_engine


def run_multi_cycle_optimizer(primary, max_cycles=5):
    engine = create_optimizer_engine()
    current = primary
    results = []

    engine.record_state(current, "initial")

    for cycle in range(1, max_cycles + 1):
        candidates = generate_optimization_candidates(current)

        if not candidates:
            results.append({
                "cycle": cycle,
                "status": "converged",
                "message": "No additional optimization candidates were generated.",
                "candidates_tested": 0
            })
            break

        best_result = None

        for action in candidates:
            result = engine.run_action_cycle(current, action)

            if best_result is None:
                best_result = result
            elif result.get("after_score", 0) > best_result.get("after_score", 0):
                best_result = result

        if not best_result:
            results.append({
                "cycle": cycle,
                "status": "no_result",
                "message": "Candidates were generated, but no valid result was produced.",
                "candidates_tested": len(candidates)
            })
            break

        results.append({
            "cycle": cycle,
            "status": "tested",
            "message": "Optimization candidates tested.",
            "candidates_tested": len(candidates),
            "before_score": best_result.get("before_score", 0),
            "after_score": best_result.get("after_score", 0),
            "accepted": best_result.get("accepted", False),
            "action": best_result.get("action", {})
        })

        if not best_result.get("accepted", False):
            results[-1]["status"] = "converged"
            results[-1]["message"] = "No candidate improved the design score."
            break

        if best_result.get("after_score", 0) <= best_result.get("before_score", 0):
            results[-1]["status"] = "converged"
            results[-1]["message"] = "Best candidate did not improve the score."
            break

        current = best_result.get("after", current)

    return {
        "final_config": current,
        "best_config": engine.get_best_config(),
        "best_score": engine.get_best_score(),
        "history": engine.get_history(),
        "cycles": results
    }


def summarize_multi_cycle_optimizer(primary, max_cycles=5):
    result = run_multi_cycle_optimizer(primary, max_cycles=max_cycles)
    cycles = result.get("cycles", [])
    best_score = result.get("best_score", 0)

    if not cycles:
        status = "No optimization cycles ran."
    else:
        last = cycles[-1]
        status = last.get("message", "Optimization complete.")

    return {
        "type": "optimizer_loop",
        "label": "Multi-cycle optimizer",
        "message": f"Optimizer completed {len(cycles)} cycle(s). Best design score: {best_score}/100. {status}",
        "confidence": "medium",
        "icon": "🔁",
        "reason": "The optimizer repeatedly generated candidates, tested mutations, rescored the design, and retained the best configuration."
    }
