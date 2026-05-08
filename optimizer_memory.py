import json
from pathlib import Path


MEMORY_FILE = "optimizer_memory.json"


def load_optimizer_memory():
    path = Path(MEMORY_FILE)

    if not path.exists():
        return []

    try:
        return json.loads(
            path.read_text()
        )

    except Exception:
        return []


def save_optimizer_memory(memory):
    path = Path(MEMORY_FILE)

    path.write_text(
        json.dumps(memory, indent=2)
    )


def remember_candidate(candidate, score):
    memory = load_optimizer_memory()

    memory.append({
        "candidate": candidate,
        "score": score
    })

    memory.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    memory = memory[:50]

    save_optimizer_memory(memory)

    return memory


def get_best_memory_candidates(count=5):
    memory = load_optimizer_memory()

    return memory[:count]


def summarize_optimizer_memory():
    memory = load_optimizer_memory()

    if not memory:
        return [{
            "type": "memory",
            "label": "Optimizer memory",
            "message": "No optimizer memory stored yet.",
            "confidence": "low",
            "icon": "🧠",
            "reason": (
                "Optimizer memory builds over time as "
                "high-performing candidates are discovered."
            )
        }]

    best = memory[0]

    return [{
        "type": "memory",
        "label": "Optimizer memory",
        "message": (
            f"{len(memory)} candidates stored. "
            f"Best historical score: "
            f"{best['score']}/100."
        ),
        "confidence": "high",
        "icon": "💾",
        "reason": (
            "Persistent memory allows the optimizer "
            "to retain historically strong designs "
            "across optimization sessions."
        )
    }]
