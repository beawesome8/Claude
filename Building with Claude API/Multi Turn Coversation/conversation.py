import os
from dotenv import load_dotenv, find_dotenv
import anthropic

load_dotenv(find_dotenv())

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
model = "claude-haiku-4-5-20251001"


def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})


def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})


def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
    )
    return message.content[0].text


if __name__ == "__main__":
    messages = []

    # Turn 1: initial question
    add_user_message(messages, "Define quantum computing in one sentence")
    answer = chat(messages)
    print(f"Claude: {answer}\n")

    # Add Claude's response to history so the next turn has context
    add_assistant_message(messages, answer)

    # Turn 2: follow-up that relies on context
    add_user_message(messages, "Write another sentence expanding on that")
    final_answer = chat(messages)
    print(f"Claude (follow-up): {final_answer}\n")

    # Show the full conversation history so you can inspect the structure
    print("--- Full message history ---")
    for msg in messages:
        print(f"[{msg['role']}] {msg['content']}")
