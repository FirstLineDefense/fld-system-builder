import copy

from design_score import suggest_design_score
from optimizer_actions import apply_optimization_action


class OptimizerEngine:
    def __init__(self):
        self.history = []
        self.best_config = None
        self.best_score = 0

    def get_design_score(self, primary):
        suggestions = suggest_design_score(primary)

        for item in suggestions:
            message = item.get("message", "")

            if "Current design score:" in message:
                try:
                    part = message.split("Current design score: ")[1]
                    score_text = part.split("/")[0]
                    return int(score_text)
                except Exception:
                    pass

        return 0

    def record_state(self, primary, label):
        snapshot = copy.deepcopy(primary)
        score = self.get_design_score(primary)

        entry = {
            "label": label,
            "score": score,
            "state": snapshot
        }

        self.history.append(entry)

        if score > self.best_score:
            self.best_score = score
            self.best_config = snapshot

        return entry

    def run_action_cycle(self, primary, action):
        before = copy.deepcopy(primary)
        before_score = self.get_design_score(before)

        after = apply_optimization_action(before, action)
        after_score = self.get_design_score(after)

        accepted = after_score >= before_score

        result = {
            "action": action,
            "before_score": before_score,
            "after_score": after_score,
            "accepted": accepted,
            "before": before,
            "after": after
        }

        self.history.append(result)

        if accepted and after_score > self.best_score:
            self.best_score = after_score
            self.best_config = copy.deepcopy(after)

        return result

    def get_best_config(self):
        return self.best_config

    def get_best_score(self):
        return self.best_score

    def get_history(self):
        return self.history


def create_optimizer_engine():
    return OptimizerEngine()
