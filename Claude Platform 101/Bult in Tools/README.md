# Anthropic Built-in Tools Demo

This repository demonstrates how to use Anthropic's built-in **server tools** in one file: a web search tool and a code execution tool.

## Files

- `anthropic_tool_demo.py` - Example Python script that calls Anthropic's `messages.create` API with server tools.
- `requirements.txt` - Python dependency list.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set your Anthropic API key in the environment:

```bash
# macOS / Linux
export ANTHROPIC_API_KEY="your_api_key"

# Windows PowerShell
$env:ANTHROPIC_API_KEY = "your_api_key"
```

## Run the demo

```bash
python anthropic_tool_demo.py
```

## What it shows

- A `web_search` tool call that queries the internet for Anthropic's latest model release.
- A `code_execution` tool call that computes the mean and standard deviation of a list.

## Notes

- These are server tools: Anthropic runs the tool logic on their infrastructure and returns the results directly in the response.
- The script prints both the tool invocation details and the returned text/output blocks.

## GitHub

Use this repo as a sample for a GitHub README explaining built-in Anthropic tools in a production-style sample project.
