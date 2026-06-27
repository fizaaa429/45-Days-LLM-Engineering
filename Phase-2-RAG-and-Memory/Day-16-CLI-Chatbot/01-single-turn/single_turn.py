"""
Day 16 - Step 1: A single-turn LLM call.

Send ONE message, print ONE reply. This is the seed the whole chatbot grows from:
notice that `messages` is a LIST, even though it has only one item right now.

Setup: pip install groq python-dotenv   (+ GROQ_API_KEY in .env from console.groq.com/keys)
Run:   python single_turn.py
"""

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()                                    # read GROQ_API_KEY from a .env file

MODEL = "llama-3.3-70b-versatile"                # see README if this name changes


def main() -> None:
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    # A message is a dict: who is speaking (role) + what they said (content).
    # We always send a LIST of messages -- today it has just one item.
    messages = [
        {"role": "user", "content": "In one sentence, what is a chatbot?"},
    ]

    chat = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )

    # The reply is buried inside the response. Pull out the first choice's text.
    reply = chat.choices[0].message.content
    print(reply.strip())


if __name__ == "__main__":
    main()
