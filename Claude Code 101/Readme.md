# Claude Code + Playwright MCP Server

A hands-on example of extending Claude Code with an MCP (Model Context Protocol) server that gives Claude the ability to control a real web browser.

---

## What is an MCP Server?

MCP servers run locally or remotely and give Claude new tools it wouldn't have by default. You can think of them as plugins — once connected, Claude can use their tools just like built-in tools (Read, Edit, Bash, etc.).

Popular use cases:

- **Browser control** (Playwright) — navigate, click, screenshot, scrape
- **Database access** — query SQL/NoSQL databases directly
- **API testing** — interact with REST/GraphQL endpoints
- **Cloud services** — AWS, GCP, Azure integrations
- **Dev tool automation** — CI pipelines, GitHub, Jira

---

## Setup: Playwright MCP Server

### 1. Install the server

Run this in a terminal **outside** of Claude Code:

```bash
claude mcp add playwright npx @playwright/mcp@latest
```

This registers a server named `playwright` that starts locally via `npx` whenever Claude Code needs it.

Verify it connected:

```bash
claude mcp list
```

You should see:

```
playwright: npx @playwright/mcp@latest - ✔ Connected
```

### 2. Configure permissions

MCP tool permissions are controlled in `.claude/settings.local.json`.

**Option A — Auto-approve all Playwright tools (no prompts):**

```json
{
  "permissions": {
    "allow": [
      "mcp__playwright"
    ]
  }
}
```

**Option B — Ask before every Playwright action (recommended for learning):**

```json
{
  "permissions": {
    "allow": [],
    "ask": [
      "mcp__playwright"
    ]
  }
}
```

> Note the double underscore: `mcp__playwright`. This is the required format for MCP server permission rules.

---

## Running the Example

> **Important:** MCP server tools only work in a **Claude Code CLI session** (terminal). They are not available inside the VSCode extension chat interface.

### Start a Claude Code session

```bash
claude
```

### Paste this prompt

```
Use the Playwright MCP server to:
1. Navigate to https://example.com
2. Take a screenshot and describe what you see
3. Click the "More information..." link on the page
4. Take another screenshot and tell me the URL you landed on
5. Get the page title of the new page
```

### What happens

Claude will use these Playwright tools in sequence:

| Tool | Action |
|---|---|
| `browser_navigate` | Opens https://example.com |
| `browser_screenshot` | Captures the page visually |
| `browser_click` | Clicks "More information..." |
| `browser_screenshot` | Captures the new page |
| `browser_snapshot` | Reads the page title |

If you configured `ask` permissions, you will be prompted to approve each tool call individually before Claude proceeds.

---

## Permission Modes Explained

| Setting | Behaviour |
|---|---|
| `allow: ["mcp__playwright"]` | Claude uses all Playwright tools without asking |
| `ask: ["mcp__playwright"]` | Claude prompts you before every Playwright tool call |
| `deny: ["mcp__playwright"]` | Claude cannot use any Playwright tools |
| *(entry absent)* | Claude prompts you the first time per session |

You can also target specific tools instead of the whole server:

```json
{
  "permissions": {
    "allow": ["mcp__playwright__browser_navigate"],
    "ask": ["mcp__playwright__browser_click"]
  }
}
```

---

## VSCode Extension vs CLI

| Context | MCP Tools Available |
|---|---|
| Claude Code CLI (`claude`) | Yes — MCP servers connect and tools are active |
| VSCode Extension (chat panel) | No — extension uses built-in tools only |

Always run browser automation tasks from a terminal `claude` session.

---

## Project Structure

```
MCP/
├── .claude/
│   └── settings.local.json   # Permission rules for MCP tools
└── README.md
```

---

## Next Steps

- Explore the full [Playwright MCP tool list](https://github.com/microsoft/playwright-mcp)
- Try combining Playwright with file-editing tools to auto-update prompts based on what Claude sees in the browser
- Browse the [MCP server ecosystem](https://github.com/modelcontextprotocol/servers) for database, API, and cloud integrations
