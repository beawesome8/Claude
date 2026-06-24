# Chat Bot Example

A simple interactive chatbot built with the Anthropic API that runs in your terminal.

## What it does

Starts a loop that:
1. Waits for you to type something
2. Sends your message (plus the full conversation history) to Claude
3. Prints Claude's reply
4. Goes back to step 1

Because the full message history is sent every time, Claude remembers everything said earlier in the conversation.

## How to run

Make sure your API key is set in the root `.env` file, then:

```bash
cd "Chat Bot Example"
..\venv\Scripts\activate
python chatbot.py
```

Type `quit` or `exit` to stop.

## Key concept — `while True`

```python
while True:
    user_input = input("You: ")   # wait for you to type
    ...                           # send to Claude, print reply
    # loop starts over automatically
```

`while True` runs forever — it keeps the chatbot alive until you explicitly type `quit`, which hits the `break` and exits the loop.
