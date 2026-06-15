# Claude Tool Use Demo

This repository contains a simple example showing how to expose local functions as Claude tools, send them to the Claude SDK, and let Claude decide which tool to call.

## Files

- `tool_use_demo.js` — a working Node.js demo using the Anthropic Claude SDK and the tool runner.
- `package.json` — project metadata and dependencies.
- `.gitignore` — ignores `node_modules`.

## What it demonstrates

- Defining plain functions that act as tools (`getWeather` and `getForecast`).
- Using the SDK's `toolRunner` so Claude can call the tool it needs.
- Running a prompt about Denver weather and printing the final assistant response.

## Setup

1. Install dependencies:

```bash
npm install
```

2. Set your Claude API key in the environment:

- PowerShell:

```powershell
$env:ANTHROPIC_API_KEY = "your_api_key_here"
```

- macOS/Linux:

```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

## Run

```bash
npm start
```

## Notes

- Claude does not run the tool directly. Your code executes the tool and returns the result back to Claude.
- The `toolRunner` handles the tool loop for you, so you do not need to manually manage `stop_reason: "tool_use"` or tool result messages.
- Update the example functions to wrap your real project logic and external systems.
