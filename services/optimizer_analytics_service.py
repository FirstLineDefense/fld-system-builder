from services.optimizer_history_service import (
    load_history,
)


def summarize_optimizer_performance():
    history = load_history()

    summaries = {}

    for entry in history:
        optimizer = entry.get(
            "optimizer",
            "unknown",
        )

        score = entry.get(
            "score",
            0,
        )

        duration = (
            entry.get(
                "telemetry",
                {},
            ).get(
                "duration_seconds",
                0,
            )
        )

        bucket = summaries.setdefault(
            optimizer,
            {
                "runs": 0,
                "total_score": 0,
                "total_duration": 0,
            },
        )

        bucket["runs"] += 1
        bucket["total_score"] += score
        bucket["total_duration"] += duration

    final = {}

    for optimizer, bucket in summaries.items():
        runs = bucket["runs"]

        final[optimizer] = {
            "runs": runs,
            "average_score": round(
                bucket["total_score"] / runs,
                2,
            ),
            "average_duration": round(
                bucket["total_duration"] / runs,
                6,
            ),
        }

    return final


def rank_optimizers():
    summaries = summarize_optimizer_performance()

    ranked = sorted(
        summaries.items(),
        key=lambda item: (
            item[1]["average_score"],
            -item[1]["average_duration"],
        ),
        reverse=True,
    )

    return ranked
