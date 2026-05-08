from registries.optimizer_registry import (
    optimizer_registry,
)

from registries.default_optimizers import (
    register_default_optimizers,
)


_registry_loaded = False


def ensure_loaded():
    global _registry_loaded

    if _registry_loaded:
        return

    register_default_optimizers()

    _registry_loaded = True


def discover_optimizers():
    ensure_loaded()

    discovered = []

    for name in optimizer_registry.names():
        optimizer = optimizer_registry.get(name)

        discovered.append(
            optimizer.metadata()
        )

    return discovered
