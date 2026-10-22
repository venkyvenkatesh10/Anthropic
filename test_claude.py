from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"


def add_user_message(messages, text):
    user_message = {
        "role": "user",
        "content": text
    }
    messages.append(user_message)


def add_assistant_message(messages, text):
    assistant_message = {
        "role": "assistant",
        "content": text
    }
    messages.append(assistant_message)


def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages
    )
    return message.content[0].text


# Start with an empty conversation
messages = []

# First question
add_user_message(messages, "Explain quantum computing in one sentence.")

# Get Claude's response
answer = chat(messages)
print("Claude:", answer)

# Save Claude's response to the conversation history
add_assistant_message(messages, answer)

# Follow-up question
add_user_message(messages, "Explain it in a simple way for a beginner.")

# Get a response using the full conversation history
final_answer = chat(messages)
print("Claude:", final_answer)