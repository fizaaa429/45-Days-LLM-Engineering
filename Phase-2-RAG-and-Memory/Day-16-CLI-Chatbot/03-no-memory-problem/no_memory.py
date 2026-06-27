"""
Day 16 - Step 3: Proving the bot has NO memory.

Two separate calls. We tell it our name, then ask for it back. Because each call
sends only its own message (a fresh list), the model cannot answer the second one.

This is a DEMONSTRATION of the problem -- Step 4 fixes it.

Setup: pip install groq python-dotenv   (+ GROQ_API_KEY in .env)
Run:   python no_memory.py
"""

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "llama-3.3-70b-versatile"


def ask(client: Groq, user_text: str) -> str:
    """Each call builds a BRAND-NEW list with just one message -- no history."""
    chat = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": user_text}],
    )
    return chat.choices[0].message.content.strip()


def main() -> None:
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    print("Call 1 -> 'My name is Riya.'")
    print("Bot:", ask(client, "My name is Riya. Remember it."), "\n")

    print("Call 2 -> 'What is my name?'")
    print("Bot:", ask(client, "What is my name?"))

    print("\n^ The bot can't say 'Riya' -- the first message was gone by the second call.")


if __name__ == "__main__":
    main()
