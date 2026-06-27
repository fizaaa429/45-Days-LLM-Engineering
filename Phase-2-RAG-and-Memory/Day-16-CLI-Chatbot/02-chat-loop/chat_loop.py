"""
Day 16 - Step 2: An interactive chat loop.

Wrap the single call from Step 1 in a `while True` loop so you can keep typing.
Type /exit (or /quit) to leave.

IMPORTANT: this version still sends ONLY the current message each time -- so the bot
has no memory yet. Step 3 makes that obvious; Step 4 fixes it.

Setup: pip install groq python-dotenv   (+ GROQ_API_KEY in .env)
Run:   python chat_loop.py
"""

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "llama-3.3-70b-versatile"


def ask(client: Groq, user_text: str) -> str:
    """Send a single message and return the reply text."""
    chat = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": user_text}],   # just THIS turn
    )
    return chat.choices[0].message.content.strip()


def main() -> None:
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    print("Chatbot ready. Type /exit to quit.\n")

    while True:
        user_text = input("You: ").strip()

        if user_text.lower() in {"/exit", "/quit"}:
            print("Bot: Bye!")
            break
        if not user_text:                      # ignore empty lines (no wasted call)
            continue

        reply = ask(client, user_text)
        print("Bot:", reply, "\n")


if __name__ == "__main__":
    main()
