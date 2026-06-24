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
    print("Chat Bot ready. Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        if not user_input:
            continue

        add_user_message(messages, user_input)
        response = chat(messages)
        add_assistant_message(messages, response)

        print(f"\nClaude: {response}\n")
