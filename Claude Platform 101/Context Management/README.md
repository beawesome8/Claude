# Claude Context Management

A small repository for demonstrating Anthropic Claude context management patterns in a practical agent use case.

## Overview

Context is everything Claude sees on a single turn:

- The system prompt
- Message history
- Tool definitions and tool results
- Attached files and skills
- Thinking blocks

This repository explains the four key context-management patterns and shows a sample use case for a compliance review agent.

## Why context management matters

A large context window may still fill quickly in a real agent, especially when using long system prompts, many history turns, and tool outputs. Once the window fills, requests fail.

The goal is not to fit everything in. The goal is to fit the right things in.

## The four context management patterns

### 1. Just-in-time context

Load only what the agent needs immediately. Let the agent pull additional data from tools when it asks.

Example: don't preload an entire codebook into the system prompt. Instead, expose a `lookup_building_code` tool and fetch only the needed section.

### 2. Server-side compaction

Use Anthropic's `context_management` key to summarize older conversation turns automatically. This keeps a long-running session within the model's context window.

Example:

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    context_management={
        "edits": [
            {"type": "compact"}
        ]
    },
    messages=messages,
)
```

### 3. Prompt caching

Cache stable request components such as the system prompt, tool definitions, or static documents. Reuse cached prompt turns across calls to reduce token cost and improve performance.

### 4. The memory tool

Use a memory directory that Claude can read and write through tool calls. This lets you store user preferences and long-lived state outside the immediate conversation while still making it available across sessions.

## Example use case: Compliance review agent

This repo includes two sample Python scripts that demonstrate the same core context management patterns with different workflows.

- `example.py`: a compliance review agent with cached prompts, memory hints, and a just-in-time building code lookup tool.
- `example_extended.py`: a second example with multiple tool fragments, memory note persistence, and a second compliance-style workflow.

Both scripts show:

- just-in-time context with a `lookup_building_code` tool
- server-side compaction via `context_management`
- prompt caching for stable request fragments
- a simple memory directory for cross-session state

### Files

- `example.py`: primary example script
- `example_extended.py`: second example with a different workflow
- `README.md`: this guide
- `requirements.txt`: dependency list for the Anthropic SDK

## How to run

1. Install dependencies if you have the Anthropic SDK available.
2. Set `ANTHROPIC_API_KEY` in your environment.
3. Run:

```bash
python example.py
```

> Note: This example uses a stubbed memory directory and tool implementation to demonstrate the pattern. Replace the stubs with your actual backend and tool integrations.

## Recap

- Context is everything Claude receives in a turn, and it is expensive.
- Use just-in-time context to keep only current needs in the request.
- Use server-side compaction to summarize long histories automatically.
- Use prompt caching to reuse stable request fragments.
- Use the memory tool to persist important state across sessions.

Wire these patterns together for a production-ready agent that stays inside its window without losing what matters.
