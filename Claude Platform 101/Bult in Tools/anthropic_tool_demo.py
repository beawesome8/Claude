import os
from anthropic import Anthropic


def run_web_search(client, query: str):
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        tools=[{"type": "web_search_20260209", "name": "web_search"}],
        messages=[
            {"role": "user", "content": query}
        ],
    )

    for block in response.content:
        if block.type == "server_tool_use":
            print(f"Tool call: {block.name} — {block.input}")
        elif block.type == "text":
            print(block.text)


def run_code_execution(client, expression: str):
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        tools=[{"type": "code_execution_20260120", "name": "code_execution"}],
        messages=[
            {"role": "user", "content": expression}
        ],
    )

    for block in response.content:
        if block.type == "server_tool_use":
            print(f"Tool call: {block.name} — {block.input}")
        elif block.type == "bash_code_execution_tool_result":
            print(f"stdout: {block.content.stdout}")
        elif block.type == "text":
            print(block.text)


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Set the ANTHROPIC_API_KEY environment variable before running this script."
        )

    client = Anthropic(api_key=api_key)

    print("--- Web Search Demo ---")
    run_web_search(client, "What is Anthropic's latest model release? Answer in one sentence.")

    print("\n--- Code Execution Demo ---")
    run_code_execution(client, "Calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]")


if __name__ == "__main__":
    main()
