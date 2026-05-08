from registries.component_registry import registry
from registries.default_components import (
    register_default_components,
)


_registry_loaded = False


def ensure_registry_loaded():
    global _registry_loaded

    if _registry_loaded:
        return

    register_default_components()

    _registry_loaded = True


def get_registered_pumps():
    ensure_registry_loaded()

    return registry.get_category("pumps")


def get_registered_motors():
    ensure_registry_loaded()

    return registry.get_category("motors")
