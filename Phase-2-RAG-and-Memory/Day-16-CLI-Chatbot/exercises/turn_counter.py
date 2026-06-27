"""
Exercise 1 - Turn Counter (STUDENT STUB).

Start from your Step 4 chatbot (memory loop). Add:
  - a counter that increases by 1 each time the user sends a real message
  - print "Turn N" before each bot reply
  - on /exit, print "We had N exchanges. Bye!"

Setup: pip install groq python-dotenv   (+ GROQ_API_KEY in .env)
Run:   python turn_counter.py
"""

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "llama-3.3-70b-versatile"


def main() -> None:
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    messages = []

    # TODO 1: create a counter variable, e.g. turns = 0
    print("Chatbot ready. Type /exit to quit.\n")

    while True:
        user_text = input("You: ").strip()

        if user_text.lower() in {"/exit", "/quit"}:
            # TODO 4: print how many exchanges happened using the counter
            break
        if not user_text:
            continue

        # TODO 2: increase the counter by 1 here

        messages.append({"role": "user", "content": user_text})
        chat = client.chat.completions.create(model=MODEL, messages=messages)
        reply = chat.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": reply})

        # TODO 3: print the turn number (e.g. "Turn 1") before the reply
        print("Bot:", reply, "\n")


if __name__ == "__main__":
    main()
