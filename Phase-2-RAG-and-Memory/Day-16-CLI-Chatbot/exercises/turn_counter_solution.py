"""
Exercise 1 - Turn Counter (SOLUTION).

Run: python turn_counter_solution.py
"""

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "llama-3.3-70b-versatile"


def main() -> None:
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    messages = []

    turns = 0                                  # TODO 1: the counter
    print("Chatbot ready. Type /exit to quit.\n")

    while True:
        user_text = input("You: ").strip()

        if user_text.lower() in {"/exit", "/quit"}:
            print(f"Bot: We had {turns} exchanges. Bye!")   # TODO 4
            break
        if not user_text:
            continue

        turns += 1                             # TODO 2: count this exchange

        messages.append({"role": "user", "content": user_text})
        chat = client.chat.completions.create(model=MODEL, messages=messages)
        reply = chat.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": reply})

        print(f"[Turn {turns}]")              # TODO 3
        print("Bot:", reply, "\n")


if __name__ == "__main__":
    main()
