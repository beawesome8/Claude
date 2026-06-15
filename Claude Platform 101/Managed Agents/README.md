# Building Your First Managed Agent

This sample shows how to create a managed agent on Anthropic's infrastructure, start a session, and stream the agent's events as it creates a temp file, counts its lines, and reports back.

## What is a managed agent?

A managed agent is an agent loop that runs on Anthropic's infrastructure instead of yours. You describe the agent once, provide an environment to work in, and start a session. Anthropic runs the loop, and you stream events back to your application.

Managed agents are enabled by default for every API account — no special access is needed.

## Overview

There are four main primitives:

1. `Agent` — the persona: model, system prompt, and toolset. This is reusable across many runs.
2. `Environment` — where the agent runs: cloud or local, networking configuration, and so on.
3. `Session` — a single run of an agent inside an environment. The session is the unit of work.
4. `Events` — the messages flowing in and out: agent actions, tool calls, tool results, and final replies.

Your app sends events in and reads events out. The managed agent runs the loop for you.

## Sample implementation

This repository contains `line_counter_agent.py`, which:

- creates an Anthropic managed agent
- creates a cloud environment with unrestricted networking
- starts a session
- opens an event stream
- sends a kickoff user message
- prints `agent.message`, `agent.tool_use`, and `session.status_idle` events

## Usage

1. Install the Anthropic Python client if you don't already have it:

```bash
pip install anthropic
```

2. Set your API key:

```bash
set ANTHROPIC_API_KEY=your_api_key_here
```

3. Run the sample:

```bash
python line_counter_agent.py
```

## Important details

- Open the event stream before sending the kickoff event.
- The agent is reusable; create it once and run many sessions.
- Events are how everything flows in this API.
- The demo watches for `agent.message`, `agent.tool_use`, and `session.status_idle`.

## Expected behavior

The sample prints the agent's reasoning and tool usage as it runs inside Anthropic's cloud container, not on your server.

## When to use managed agents

Use managed agents when the loop would run for a long time, perform many tool-driven steps, touch files, or need resumability after interruptions. If you want full control over the loop and direct tool orchestration, a manual loop may be more appropriate.
