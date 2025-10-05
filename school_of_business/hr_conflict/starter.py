# ai_simulations/school_of_business/hr_conflict/starter.py

import os
import json
import streamlit as st
from pathlib import Path
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from transformers import pipeline

from engine import HRConflictEngine
from ai_dialogue import generate_dialogue

# Load .env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    st.error("HF_TOKEN not found. Set it in .env")
    st.stop()

# --- AI Dialogue Client ---
client = InferenceClient(
    model="ibm-granite/granite-4.0-micro",
    token=HF_TOKEN
)

def generate_dialogue(prompt: str) -> str:
    full_prompt = f"You are Employee A in a workplace conflict. Respond professionally to: {prompt}"
    result = client.text_generation(full_prompt, max_new_tokens=150, temperature=0.7)
    return result.strip()

# --- Engine ---
class HRConflictEngine:
    def __init__(self, scenario_path):
        self.scenario = json.load(open(scenario_path))
        self.state = self.scenario["initial_state"].copy()
        self.history = []

    def make_decision(self, action_id: str):
        decision = next(a for a in self.scenario["actions"] if a["id"] == action_id)
        self.state["morale"] += decision["effects"]["morale"]
        self.state["trust"] += decision["effects"]["trust"]
        self.state["risk"] += decision["effects"]["risk"]
        self.history.append({"action": decision["text"], "result": decision["result_text"]})
        return decision["result_text"]

    def get_score(self):
        return self.state

# --- Streamlit UI ---
def main():
    st.title("🧑‍💼 HR Conflict Simulation (NajmAI)")

    scenario_file = Path(__file__).parent / "scenario.json"
    engine = HRConflictEngine(scenario_file)

    st.write("### Scenario")
    st.write(engine.scenario["description"])

    st.write("### Decisions")
    for action in engine.scenario["actions"]:
        if st.button(action["text"]):
            result = engine.make_decision(action["id"])
            st.success(result)
            st.write("**Current Scores:**", engine.get_score())

    user_prompt = st.text_input("Ask Employee A a question:")
    if user_prompt:
        ai_reply = generate_dialogue(user_prompt)
        st.write(f"**Employee A:** {ai_reply}")

if __name__ == "__main__":
    main()
