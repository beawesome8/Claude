# Building with Claude API — Multi-Turn Conversations

Skilljar learning project demonstrating how to maintain conversation context with the Anthropic API.

## Key concept

Claude is stateless — each API call knows nothing about prior calls. To simulate memory, you maintain a `messages` list in your code and send the **full history** on every request.

## Setup

1. Add your key to `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

2. Install dependencies (activate venv first):
   ```bash
   pip install anthropic python-dotenv
   ```

3. Run the demo:
   ```bash
   python conversation.py
   ```

## What to look for

- Turn 1: Claude defines quantum computing.
- Turn 2: Claude expands on *that specific definition* — not something random — because the full history was sent.
- The printed `messages` list at the end shows the exact payload structure sent to the API.

## Files

| File | Purpose |
|------|---------|
| `conversation.py` | Core implementation with helper functions |
| `.env` | API key (git-ignored) |
| `.gitignore` | Excludes secrets and virtualenv |
