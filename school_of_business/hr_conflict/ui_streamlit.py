# ai_simulations/school_of_business/hr_conflict/ui_streamlit.py

import streamlit as st
import sys
from pathlib import Path

# Add project root to Python path
ROOT = Path(__file__).resolve().parents[3]  # adjust depending on depth
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from ai_simulations.school_of_business.hr_conflict.engine import HRConflictEngine
from ai_simulations.school_of_business.hr_conflict.ai_dialogue import generate_dialogue

def main():
    st.title("🧑‍💼 HR Conflict Simulation")
    engine = HRConflictEngine(Path(__file__).parent / "scenario.json")

    st.write("### Scenario")
    st.write(engine.scenario["description"])

    for action in engine.scenario["actions"]:
        if st.button(action["text"]):
            result = engine.make_decision(action["id"])
            st.write(result)
            st.write(engine.get_score())

    user_prompt = st.text_input("Ask Employee A a question:")
    if user_prompt:
        ai_reply = generate_dialogue(user_prompt)
        st.write(f"**Employee A:** {ai_reply}")

if __name__ == "__main__":
    main()
