# Your First Claude API Call

A minimal example of calling the Claude API to review buggy code — built as part of the Skilljar Claude Platform 101 course.

---

## What it does

Sends a snippet of buggy JavaScript to Claude and gets back a one-paragraph code review. Under 20 lines of code.

```js
function add(a, b) {
  return a - b;  // ← Claude catches this
}
```

---

## Prerequisites

- Node.js 18+
- An Anthropic API key from [platform.claude.com](https://platform.claude.com)

---

## Setup

**1. Clone the repo and install dependencies:**

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
npm install
```

**2. Create a `.env.local` file and add your API key:**

```
ANTHROPIC_API_KEY=your_api_key_here
```

> `.env.local` is listed in `.gitignore` and will never be committed. Never hardcode API keys in source files.

**3. Run the script:**

```bash
npm start
```

---

## Expected output

Claude responds with a one-paragraph review pointing out that `add` subtracts instead of adds, and suggests the fix.

---

## Key concepts

| Concept | Details |
|---|---|
| Model | `claude-opus-4-8` |
| Endpoint | `client.messages.create` |
| System prompt | Sets Claude's persona ("terse senior code reviewer") |
| Response format | Array of content blocks — always loop and check `block.type` |

---

## The anatomy of a request

Every API call goes through `messages.create`. You specify three things:

- **model** — which Claude model handles the request
- **max_tokens** — a cap on how long the response can be
- **messages** — objects with `user` or `assistant` roles

The `system` field shapes Claude's persona before the conversation starts.

---

## Project structure

```
├── index.js        # The API call (~20 lines)
├── package.json    # Dependencies
├── .env.local      # Your API key (not committed)
└── .gitignore      # Excludes node_modules and .env.local
```

---

## Learn more

- [Anthropic API Docs](https://docs.anthropic.com)
- [Claude Platform Console](https://platform.claude.com)
