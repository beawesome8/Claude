# Agent Loop Explained

A minimal Python script that demonstrates how the Claude agent loop works end to end — no database, no UI, just the loop itself.

## What it does

Asks Claude "What should I wear in Austin today?" Claude has no built-in weather knowledge, so it has to call a `get_weather` tool, read the result, and then give a clothing recommendation.

**Turn 1** — stop reason is `tool_use`. Claude calls `get_weather` for Austin and gets back `95F, sunny`.  
**Turn 2** — stop reason is `end_turn`. Claude uses that result to answer the question.

Two API calls, one tool execution, one final answer. That's the entire loop.

## The three key pieces

| Piece | What it does |
|---|---|
| `tools` array | Tells Claude what's available: a name, description, and JSON schema for inputs |
| `run_tool()` | Hardcoded weather lookup — in a real app this would hit an API or database |
| `while True` loop | Sends messages to Claude, checks `stop_reason`, runs tools or prints the answer and breaks |

## Setup

**1. Install the Anthropic SDK**
```bash
pip install anthropic
```

**2. Set your API key**
```bash
# Mac/Linux
export ANTHROPIC_API_KEY="your-api-key-here"

# Windows PowerShell
$env:ANTHROPIC_API_KEY = "your-api-key-here"
```

**3. Run it**
```bash
python agent_loop.py
```

## Expected output

```
--- Turn (stop_reason: tool_use) ---
Tool call: get_weather({'city': 'Austin'})
Tool result: Weather in Austin: 95F, sunny

--- Turn (stop_reason: end_turn) ---
Since it's 95°F and sunny in Austin, I'd recommend light, breathable
clothing — a t-shirt and shorts. Don't forget sunscreen!
```

## How the loop works

```
User message
     │
     ▼
Claude API call
     │
     ├── stop_reason: tool_use ──► run the tool ──► append result to messages ──► loop
     │
     └── stop_reason: end_turn ──► print answer ──► break
```

Everything you build with the Claude API follows this same shape. The differences in production are real tools instead of a mock lookup, results streaming back to a UI, and findings persisted to a database.
