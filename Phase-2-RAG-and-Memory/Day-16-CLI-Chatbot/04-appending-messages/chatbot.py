"""
Day 16 - Step 4: A chatbot that REMEMBERS (the core lesson).

We keep ONE `messages` list for the whole conversation and append every turn:
  - append the user's message  -> then call the model with the FULL history
  - append the assistant's reply -> so the bot remembers its own answers too

Try it: say "My name is Riya." then ask "What is my name?" -- now it knows.

Setup: pip install groq python-dotenv   (+ GROQ_API_KEY in .env)
Run:   python chatbot.py
"""

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "llama-3.3-70b-versatile"


def main() -> None:
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    messages = []                              # the conversation -- kept alive across turns
    print("Chatbot with memory. Type /exit to quit.\n")

    while True:
        user_text = input("You: ").strip()

        if user_text.lower() in {"/exit", "/quit"}:
            print("Bot: Bye!")
            break
        if not user_text:
            continue

        # 1. Add the user's message to the history.
        messages.append({"role": "user", "content": user_text})

        # 2. Send the ENTIRE history -- this is what gives the bot memory.
        chat = client.chat.completions.create(model=MODEL, messages=messages)
        reply = chat.choices[0].message.content.strip()

        # 3. Add the bot's reply too, so it remembers what it said.
        messages.append({"role": "assistant", "content": reply})

        print("Bot:", reply, "\n")


if __name__ == "__main__":
    main()
