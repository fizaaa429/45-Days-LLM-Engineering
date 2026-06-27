# Day 16 — Exercises

Practice on top of the chatbot you built today. Each problem has a **stub** (with `# TODO`s) and a
worked **`_solution.py`**. Try the stub first; peek at the solution only when stuck.

Start from your Step 4 / Step 5 chatbot — these add small features to it.

| # | File | Build this |
|--:|------|------------|
| 1 | [turn_counter.py](turn_counter.py) | A chatbot that shows the **turn number** before each reply and, on `/exit`, prints how many exchanges happened. |
| 2 | [persona_picker.py](persona_picker.py) | At startup, let the user **pick a persona** (tutor / pirate / lawyer); set the system prompt from their choice. |

Solutions: [turn_counter_solution.py](turn_counter_solution.py) · [persona_picker_solution.py](persona_picker_solution.py)

## Stretch goals (no solution provided — make them yours)
- Add a `/undo` command that removes the last user+assistant pair from `messages`.
- Cap memory to the **last N turns** (keep the system prompt + the most recent N exchanges) so the
  history can't grow forever — a first taste of the "context window" problem from Day 9.
- Colour the `You:` / `Bot:` labels using ANSI escape codes.

➡ Back to [Day 16 overview](../README.md)
