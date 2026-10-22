from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"


def add_user_message(messages, text):
    messages.append({
        "role": "user",
        "content": text
    })


def add_assistant_message(messages, text):
    messages.append({
        "role": "assistant",
        "content": text
    })


def chat(messages, system_prompt=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages
    }

    if system_prompt:
        params["system"] = system_prompt

    response = client.messages.create(**params)
    return response.content[0].text


math_tutor_prompt = """
You are a patient and encouraging math tutor.

Your goal is to help students understand math instead of simply giving answers.

Follow these rules:
- Ask the student's grade level or experience when needed.
- Give hints before giving the complete solution.
- Guide the student one step at a time.
- Ask questions that encourage the student to think.
- Explain why each step works.
- Check the student's work carefully.
- Use simple language and examples.
- Never make the student feel embarrassed.
- If the student is stuck after trying, provide a more detailed explanation.
- Show the complete solution only after giving reasonable guidance.
- Use correct mathematical notation.
"""


messages = []

print("Math Tutor started. Type 'quit' to exit.")

while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ["quit", "exit"]:
        print("Goodbye!")
        break

    add_user_message(messages, user_input)

    answer = chat(messages, math_tutor_prompt)

    print("\nMath Tutor:", answer)

    add_assistant_message(messages, answer)