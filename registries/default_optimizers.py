from registries.optimizer_registry import optimizer_registry

from engines.optimizers.basic_optimizer import (
    BasicOptimizer,
)


def register_default_optimizers():
    optimizer_registry.register(
        "basic",
        BasicOptimizer(),
    )
