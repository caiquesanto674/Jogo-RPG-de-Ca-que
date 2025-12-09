"""
APOLO ENGINE – CRONOS TIMELINE
Registra eventos importantes e pontos temporais do projeto.
"""

import json
import os
from datetime import datetime
from typing import Dict, List

class ChronosTimeline:
    def __init__(self, path: str = "./.apolo_backups/timeline.json"):
        self.path = path
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump([], f, indent=4)

    def add_event(self, description: str, snapshot: str):
        with open(self.path, "r") as f:
            timeline = json.load(f)

        timeline.append({
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "snapshot": snapshot
        })

        with open(self.path, "w") as f:
            json.dump(timeline, f, indent=4)

    def get_events(self) -> List[Dict]:
        with open(self.path, "r") as f:
            return json.load(f)
