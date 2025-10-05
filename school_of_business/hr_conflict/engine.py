# ai_simulations/school_of_business/hr_conflict/engine.py

import json
from pathlib import Path

class HRConflictEngine:
    def __init__(self, scenario_path: str):
        self.scenario = json.load(open(scenario_path))
        self.state = self.scenario["initial_state"]
        self.history = []

    def make_decision(self, action_id: str):
        """Apply consequences of the decision"""
        decision = next(a for a in self.scenario["actions"] if a["id"] == action_id)
        self.state["morale"] += decision["effects"]["morale"]
        self.state["trust"] += decision["effects"]["trust"]
        self.state["risk"] += decision["effects"]["risk"]

        self.history.append({
            "action": decision["text"],
            "result": decision["result_text"]
        })

        return decision["result_text"]

    def get_score(self):
        return {
            "morale": self.state["morale"],
            "trust": self.state["trust"],
            "risk": self.state["risk"]
        }
