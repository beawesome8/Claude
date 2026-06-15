import os
from typing import Dict, List

# Example only: replace with your actual Anthropic SDK import and live client setup.
# from anthropic import Anthropic

# client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

MEMORY_PATH = "memory"
CACHE: Dict[str, List[dict]] = {}

SYSTEM_PROMPT = (
    "You are a contract compliance assistant. You may use tools and a memory directory "
    "to keep the request inside the context window while preserving critical information."
)

TOOL_DEFINITIONS = [
    {
        "name": "lookup_building_code",
        "description": "Retrieve a specific building code section by ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "section_id": {"type": "string", "description": "The code section to find."}
            },
            "required": ["section_id"],
        },
    },
    {
        "name": "store_memory_note",
        "description": "Save a short note to the memory directory for future sessions.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Memory filename."},
                "content": {"type": "string", "description": "Note content."},
            },
            "required": ["filename", "content"],
        },
    },
]


def ensure_memory_path() -> None:
    os.makedirs(MEMORY_PATH, exist_ok=True)


def write_memory(filename: str, content: str) -> None:
    with open(os.path.join(MEMORY_PATH, filename), "w", encoding="utf-8") as f:
        f.write(content)


def read_memory(filename: str) -> str:
    path = os.path.join(MEMORY_PATH, filename)
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_cached_system_prompt() -> List[dict]:
    if "system_prompt" not in CACHE:
        CACHE["system_prompt"] = [{"role": "system", "content": SYSTEM_PROMPT}]
    return CACHE["system_prompt"]


def get_cached_tool_fragments() -> List[dict]:
    if "tools" not in CACHE:
        CACHE["tools"] = [
            {
                "role": "tool",
                "name": tool["name"],
                "content": tool["description"],
            }
            for tool in TOOL_DEFINITIONS
        ]
    return CACHE["tools"]


def build_messages(user_question: str) -> List[dict]:
    messages: List[dict] = []
    messages.extend(get_cached_system_prompt())
    messages.extend(get_cached_tool_fragments())

    recent_memory = read_memory("notes.txt")
    if recent_memory:
        messages.append({
            "role": "system",
            "content": f"Memory note from prior session: {recent_memory}",
        })

    messages.append({"role": "user", "content": user_question})
    return messages


def call_claude(messages: List[dict]) -> dict:
    print("=== REQUEST MESSAGES ===")
    for message in messages:
        print(message)
    print("========================")

    response = {
        "id": "fake-extended-response",
        "output": {
            "content": [
                {
                    "type": "output_text",
                    "text": (
                        "I reviewed the current contract concerns. "
                        "If you need a section of the code, request lookup_building_code with the section id. "
                        "Also, I can store a session note to memory if you want to preserve it."
                    ),
                }
            ]
        }
    }

    # Uncomment and adapt the real client call:
    # response = client.messages.create(
    #     model="claude-sonnet-4-5",
    #     max_tokens=1024,
    #     context_management={"edits": [{"type": "compact"}]},
    #     messages=messages,
    # )

    return response


def simulate_tool_usage() -> None:
    code_section = lookup_building_code("C3")
    print("\n=== JUST-IN-TIME TOOL OUTPUT ===")
    print(code_section)

    write_memory("notes.txt", "Saved a contract risk note for next session.")
    print("\n=== MEMORY SAVED ===")
    print(read_memory("notes.txt"))


def lookup_building_code(section_id: str) -> str:
    tool_data = {
        "A1": "Section A1: Fire safety requirements for residential buildings.",
        "B2": "Section B2: Accessibility guidelines and exit routes.",
        "C3": "Section C3: Electrical system inspection requirements.",
    }
    return tool_data.get(section_id, f"No building code entry found for {section_id}.")


def main() -> None:
    ensure_memory_path()

    user_question = (
        "A client wants to update their lease agreement. "
        "Identify any compliance risks and tell me if I should fetch a specific code section."
    )

    messages = build_messages(user_question)
    response = call_claude(messages)

    print("\n=== CLAUDE RESPONSE ===")
    print(response["output"]["content"][0]["text"])

    simulate_tool_usage()


if __name__ == "__main__":
    main()
