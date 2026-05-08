from services.optimizer_history_service import (
    load_history,
)

from services.orchestration_metrics_service import (
    build_metrics_summary,
)

from services.optimizer_analytics_service import (
    summarize_optimizer_performance,
)

from services.runtime_retention_service import (
    prune_optimizer_history,
)


class RuntimeIntelligenceManager:

    def build_runtime_summary(self):
        history = load_history()

        metrics = build_metrics_summary()

        optimizer_summary = (
            summarize_optimizer_performance()
        )

        return {
            "history_entries": len(history),
            "metrics": metrics,
            "optimizer_summary": (
                optimizer_summary
            ),
        }

    def apply_retention(self):
        return prune_optimizer_history()
