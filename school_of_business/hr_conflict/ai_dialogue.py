# ai_simulations/school_of_business/hr_conflict/ai_dialogue.py
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv('../../.env')  # Loads .env into environment variables

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    model="microsoft/Phi-3-mini-4k-instruct",
    token=HF_TOKEN,
)

def generate_dialogue(prompt: str) -> str:
    """Send prompt to hosted model and return generated text."""
    full_prompt = f"You are Employee A in a workplace conflict. Respond professionally to: {prompt}"
    result = client.text_generation(
        full_prompt,
        max_new_tokens=150,
        temperature=0.7,
    )
    return result.strip()
