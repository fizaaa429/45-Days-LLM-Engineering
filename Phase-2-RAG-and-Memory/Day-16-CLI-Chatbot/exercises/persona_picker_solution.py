"""
Exercise 2 - Persona Picker (SOLUTION).

Run: python persona_picker_solution.py
"""

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

PERSONAS = {
    "1": "You are a patient coding tutor. Explain simply, under 4 sentences.",
    "2": "You are a witty pirate. Answer helpfully but talk like a pirate.",
    "3": "You are a formal legal advisor. Be precise and cautious.",
}


def main() -> None:
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    print("Pick a persona:  1) tutor   2) pirate   3) lawyer")
    choice = input("Choice: ").strip()                       # TODO 1
    system_prompt = PERSONAS.get(choice, PERSONAS["1"])      # TODO 2 (default = tutor)
    messages = [{"role": "system", "content": system_prompt}]  # TODO 3

    print("\nPersona set. Type /exit to quit.\n")

    while True:
        user_text = input("You: ").strip()
        if user_text.lower() in {"/exit", "/quit"}:
            print("Bot: Bye!")
            break
        if not user_text:
            continue

        messages.append({"role": "user", "content": user_text})
        chat = client.chat.completions.create(model=MODEL, messages=messages)
        reply = chat.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": reply})
        print("Bot:", reply, "\n")


if __name__ == "__main__":
    main()
