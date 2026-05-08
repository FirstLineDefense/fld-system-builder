from engines.optimizers.base_optimizer import (
    BaseOptimizer,
)


class BasicOptimizer(BaseOptimizer):
    name = "basic"

    version = "1.1"

    description = (
        "Minimum viable component matching optimizer"
    )

    capabilities = [
        "minimum_viable_match",
        "component_selection",
        "baseline_optimization",
    ]

    def optimize(self, requirements):
        target_gpm = requirements.get(
            "target_gpm",
            0,
        )

        score = min(
            100,
            int(target_gpm / 2),
        )

        return {
            "optimizer": self.name,
            "status": "success",
            "requirements": requirements,
            "selected_strategy": "minimum_viable_match",
            "score": score,
        }
