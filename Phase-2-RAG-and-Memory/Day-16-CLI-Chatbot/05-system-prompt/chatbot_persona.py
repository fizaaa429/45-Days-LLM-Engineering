"""
Day 16 - Step 5: A chatbot with a personality (system prompt).

Same memory loop as Step 4, but the `messages` list now STARTS with a `system`
message that sets the bot's identity, tone, and rules. It stays at the top of the
list, so the model re-reads it on every turn.

Edit SYSTEM_PROMPT below and watch the bot's whole personality change.

Setup: pip install groq python-dotenv   (+ GROQ_API_KEY in .env)
Run:   python chatbot_persona.py
"""

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = (
    "You are Sparky, a cheerful coding tutor for Indian B.Tech students who know only basic "
    "Python. Explain simply, use small everyday examples, and keep replies under 4 sentences."
)


def main() -> None:
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    # The conversation starts with the system message -- the bot's standing instructions.
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Sparky is ready. Type /exit to quit.\n")

    while True:
        user_text = input("You: ").strip()

        if user_text.lower() in {"/exit", "/quit"}:
            print("Bot: Bye! Keep coding.")
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
