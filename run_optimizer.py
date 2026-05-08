from evolutionary_runtime import (
    run_evolution
)

from convergence_report import (
    print_evolution_summary
)


def main():
    candidate = {
        "primary": {
            "pump": {"gpm": 300},
            "motor": {"hp": 10},
            "runtime_minutes": 120,
            "water_gallons": 5000,
            "branches": [
                {
                    "target_gpm": 120,
                    "velocity_fps": 9,
                    "pipe_diameter_in": 1.0
                }
            ]
        }
    }

    history = run_evolution(
        candidate,
        generations=20,
        population_size=20
    )

    print_evolution_summary(
        history
    )


if __name__ == "__main__":
    main()
