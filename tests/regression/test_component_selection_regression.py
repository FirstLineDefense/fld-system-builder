import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)

from services.component_selection_service import (
    select_best_pump,
    select_best_motor,
)


def run():
    pump_name, pump = select_best_pump(100)

    print("\nSELECTED PUMP:")
    print(pump_name)
    print(pump)

    assert pump_name == "GX390"
    assert pump["gpm"] == 120

    motor_name, motor = select_best_motor(20)

    print("\nSELECTED MOTOR:")
    print(motor_name)
    print(motor)

    assert motor_name == "37HP"
    assert motor["hp"] == 37

    print("\nComponent selection regression passed")


if __name__ == "__main__":
    run()
