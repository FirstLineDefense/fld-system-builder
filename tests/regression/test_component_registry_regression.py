import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from registries.component_registry import registry
from registries.default_components import (
    register_default_components,
)


def run():
    register_default_components()

    pumps = registry.get_category("pumps")
    motors = registry.get_category("motors")

    print("\nREGISTERED CATEGORIES:")
    print(registry.categories())

    print("\nPUMPS:")
    print(pumps)

    print("\nMOTORS:")
    print(motors)

    gx390 = registry.get("pumps", "GX390")

    assert gx390 is not None
    assert gx390["gpm"] == 120

    hp37 = registry.get("motors", "37HP")

    assert hp37 is not None
    assert hp37["hp"] == 37

    print("\nComponent registry regression passed")


if __name__ == "__main__":
    run()
