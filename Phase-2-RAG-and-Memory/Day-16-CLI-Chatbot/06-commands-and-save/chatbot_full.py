"""
Day 16 - Step 6: The full CLI chatbot -- memory + persona + commands + save/load.

Slash commands are intercepted BEFORE we call the model:
  /exit /quit  -> leave
  /reset       -> clear history (keep the system prompt)
  /history     -> show how many turns are stored
  /save        -> dump the messages list to chat_history.json
  /load        -> read it back and keep chatting with full memory

Because `messages` is just a list of dicts, saving it is one json.dump call.

Setup: pip install groq python-dotenv   (+ GROQ_API_KEY in .env)
Run:   python chatbot_full.py
"""

import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "llama-3.3-70b-versatile"
HISTORY_FILE = "chat_history.json"
SYSTEM_PROMPT = "You are a friendly, concise assistant. Keep replies short and clear."


def fresh_history() -> list:
    """A new conversation: just the system message."""
    return [{"role": "system", "content": SYSTEM_PROMPT}]


def save(messages: list) -> None:
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)
    print(f"Bot: Saved {len(messages)} messages to {HISTORY_FILE}.\n")


def load() -> list:
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            messages = json.load(f)
        print(f"Bot: Loaded {len(messages)} messages from {HISTORY_FILE}.\n")
        return messages
    except FileNotFoundError:
        print(f"Bot: No {HISTORY_FILE} yet -- nothing to load.\n")
        return fresh_history()


def main() -> None:
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    messages = fresh_history()
    print("Chatbot ready. Commands: /reset /history /save /load /exit\n")

    while True:
        user_text = input("You: ").strip()
        if not user_text:
            continue

        # --- handle slash commands before touching the API ---
        cmd = user_text.lower()
        if cmd in {"/exit", "/quit"}:
            print("Bot: Bye!")
            break
        if cmd == "/reset":
            messages = fresh_history()
            print("Bot: Conversation cleared.\n")
            continue
        if cmd == "/history":
            turns = sum(1 for m in messages if m["role"] != "system")
            print(f"Bot: {turns} messages in history (excluding the system prompt).\n")
            continue
        if cmd == "/save":
            save(messages)
            continue
        if cmd == "/load":
            messages = load()
            continue

        # --- a normal message: the memory loop from Step 4 ---
        messages.append({"role": "user", "content": user_text})
        chat = client.chat.completions.create(model=MODEL, messages=messages)
        reply = chat.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": reply})
        print("Bot:", reply, "\n")


if __name__ == "__main__":
    main()
