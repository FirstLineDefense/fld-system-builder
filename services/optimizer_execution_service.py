from registries.optimizer_registry import (
    optimizer_registry,
)

from registries.default_optimizers import (
    register_default_optimizers,
)

from services.optimizer_telemetry_service import (
    begin_execution,
    finalize_execution,
)

from services.optimizer_history_service import (
    append_history,
)


_registry_loaded = False


def ensure_optimizer_registry_loaded():
    global _registry_loaded

    if _registry_loaded:
        return

    register_default_optimizers()

    _registry_loaded = True


def run_optimizer(name, requirements):
    ensure_optimizer_registry_loaded()

    optimizer = optimizer_registry.get(name)

    if optimizer is None:
        raise ValueError(
            f"Unknown optimizer: {name}"
        )

    telemetry = begin_execution(name)

    result = optimizer.optimize(
        requirements
    )

    telemetry = finalize_execution(
        telemetry,
        result,
    )

    result["telemetry"] = telemetry

    append_history(
        {
            "optimizer": name,
            "requirements": requirements,
            "score": result.get(
                "score",
                0,
            ),
            "telemetry": telemetry,
        }
    )

    return result
