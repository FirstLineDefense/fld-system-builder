from registries.component_registry import registry


DEFAULT_COMPONENTS = {
    "pumps": {
        "GX390": {
            "gpm": 120,
            "psi": 110,
        },
        "Kubota_D902": {
            "gpm": 250,
            "psi": 145,
        },
    },
    "motors": {
        "13HP": {
            "hp": 13,
        },
        "37HP": {
            "hp": 37,
        },
    },
}


def register_default_components():
    for category, components in DEFAULT_COMPONENTS.items():
        for name, component in components.items():
            registry.register(
                category,
                name,
                component,
            )
