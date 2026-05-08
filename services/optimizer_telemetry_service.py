from datetime import datetime
import time


def begin_execution(name):
    return {
        "optimizer": name,
        "start_time": time.time(),
        "started_at": datetime.utcnow().isoformat(),
    }


def finalize_execution(
    telemetry,
    result,
):
    end_time = time.time()

    telemetry["end_time"] = end_time

    telemetry["duration_seconds"] = round(
        end_time - telemetry["start_time"],
        6,
    )

    telemetry["status"] = result.get(
        "status",
        "unknown",
    )

    telemetry["strategy"] = result.get(
        "selected_strategy",
        "unknown",
    )

    telemetry["score"] = result.get(
        "score",
        0,
    )

    return telemetry
