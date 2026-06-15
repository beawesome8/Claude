import os
from typing import Dict, List

# Example only: replace with your actual Anthropic SDK import and client setup.
# from anthropic import Anthropic

# client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = (
    "You are a compliance review assistant. Use the provided tool definitions and memory directory. "
    "Summarize older conversation turns automatically when asked, and prefer just-in-time retrieval." 
)

TOOL_DEFINITIONS = [
    {
        "name": "lookup_building_code",
        "description": "Retrieve a building code section by identifier.",
        "parameters": {
            "type": "object",
            "properties": {
                "section_id": {"type": "string", "description": "The building code section to look up."}
            },
            "required": ["section_id"],
        },
    }
]

CACHE: Dict[str, List[dict]] = {}
MEMORY_DIR = "memory"


def ensure_memory_dir() -> None:
    """Create the local memory directory if it does not exist."""
    os.makedirs(MEMORY_DIR, exist_ok=True)


def write_memory(filename: str, content: str) -> None:
    with open(os.path.join(MEMORY_DIR, filename), "w", encoding="utf-8") as f:
        f.write(content)


def read_memory(filename: str) -> str:
    path = os.path.join(MEMORY_DIR, filename)
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def lookup_building_code(section_id: str) -> str:
    """Stubbed tool: returns a mocked building code section."""
    tool_data = {
        "A1": "Section A1: Fire safety requirements for residential buildings.",
        "B2": "Section B2: Accessibility guidelines and exit routes.",
        "C3": "Section C3: Electrical system inspection requirements.",
    }
    return tool_data.get(section_id, f"No building code entry found for {section_id}.")


def get_cached_system_prompt() -> dict:
    """Cache the stable system prompt block for reuse across calls."""
    if "system_prompt" not in CACHE:
        CACHE["system_prompt"] = [{"role": "system", "content": SYSTEM_PROMPT}]
    return CACHE["system_prompt"]


def get_cached_tool_prompt() -> dict:
    """Cache the tool definitions as a stable context fragment."""
    if "tool_definitions" not in CACHE:
        CACHE["tool_definitions"] = [
            {
                "role": "tool",
                "name": TOOL_DEFINITIONS[0]["name"],
                "content": TOOL_DEFINITIONS[0]["description"],
            }
        ]
    return CACHE["tool_definitions"]


def build_messages(user_request: str) -> List[dict]:
    messages = []
    messages.extend(get_cached_system_prompt())
    messages.extend(get_cached_tool_prompt())

    memory_hint = read_memory("last_issue.txt")
    if memory_hint:
        messages.append({
            "role": "system",
            "content": f"Previous user issue note: {memory_hint}",
        })

    messages.append({"role": "user", "content": user_request})
    return messages


def call_claude(messages: List[dict]) -> dict:
    """Call Claude with the messages and server-side compaction enabled."""
    print("=== REQUEST MESSAGES ===")
    for message in messages:
        print(message)
    print("========================")

    response = {
        "id": "fake-response",
        "output": {
            "content": [
                {
                    "type": "output_text",
                    "text": (
                        "I reviewed the compliance request. "
                        "If you need a specific code section, call lookup_building_code with the section id."
                    ),
                }
            ]
        }
    }

    # Uncomment and adapt if using the real Anthropic SDK:
    # response = client.messages.create(
    #     model="claude-sonnet-4-5",
    #     max_tokens=1024,
    #     context_management={"edits": [{"type": "compact"}]},
    #     messages=messages,
    # )

    return response


def main() -> None:
    ensure_memory_dir()

    user_request = (
        "Please review the compliance request for a commercial renovation and tell me if I should fetch "
        "any building code section." 
    )

    messages = build_messages(user_request)
    response = call_claude(messages)

    print("\n=== CLAUDE RESPONSE ===")
    print(response["output"]["content"][0]["text"])

    # Example of saving memory across sessions.
    write_memory("last_issue.txt", "Customer asked about commercial renovation compliance.")

    # Example of just-in-time tool use.
    section_text = lookup_building_code("B2")
    print("\n=== TOOL RESULT ===")
    print(section_text)


if __name__ == "__main__":
    main()
