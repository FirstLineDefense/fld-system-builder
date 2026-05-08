
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class ProjectReport:
    meta: Dict[str, Any] = field(default_factory=dict)
    pricing: Dict[str, Any] = field(default_factory=dict)
    html_report: str = ""
