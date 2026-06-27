"""
Exercise 2 - Persona Picker (STUDENT STUB).

Before the chat loop starts, ask the user which persona they want, then use the
matching system prompt. Reuse the memory loop from Step 5.

Personas:
  1 -> tutor:  "You are a patient coding tutor. Explain simply, under 4 sentences."
  2 -> pirate: "You are a witty pirate. Answer helpfully but talk like a pirate."
  3 -> lawyer: "You are a formal legal advisor. Be precise and cautious."

Setup: pip install groq python-dotenv   (+ GROQ_API_KEY in .env)
Run:   python persona_picker.py
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

    # TODO 1: show the choices and read the user's pick with input()
    # TODO 2: look up the chosen system prompt in PERSONAS
    #         (use PERSONAS.get(choice, <a sensible default>) so a bad pick still works)
    # TODO 3: start `messages` with that system prompt:
    #         messages = [{"role": "system", "content": chosen_prompt}]
    messages = []   # replace this

    print("Persona set. Type /exit to quit.\n")

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
