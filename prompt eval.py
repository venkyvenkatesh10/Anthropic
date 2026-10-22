from dotenv import load_dotenv
from anthropic import Anthropic
from GRADERS import VALIDATORS

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"


def run_prompt(test_case):
    """Send one test case to Claude, return the answer text."""
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=[
            {"role": "user", "content": test_case["question"]}
        ]
    )
    return message.content[0].text


def grade_with_model(test_case, output):
    """A second Claude call — the examiner. Returns a score 0–10."""
    grader_prompt = f"""
You are grading an AI's answer.

Question: {test_case["question"]}
The answer should be about: {test_case["expected"]}
The AI answered: {output}

Score it 0 to 10 for correctness. Reply with ONLY the number.
"""
    message = client.messages.create(
        model=model,
        max_tokens=10,
        messages=[{"role": "user", "content": grader_prompt}]
    )
    return int(message.content[0].text.strip())


def run_test_case(test_case):
    """Run one case, grade it, return the report card."""
    output = run_prompt(test_case)

    # Model grader: Claude marks the answer (Lesson 13)
    task_score = grade_with_model(test_case, output)

    # Code grader: only when the case demands a format (Lesson 14)
    if "format" in test_case:
        syntax_score = VALIDATORS[test_case["format"]](output)
        score = (task_score + syntax_score) / 2   # combining scores
    else:
        syntax_score = None
        score = task_score

    return {
        "test_case": test_case,
        "output": output,
        "syntax_score": syntax_score,
        "task_score": task_score,
        "score": score,
    }


def run_eval(dataset):
    """Run every case, collect all the report cards."""
    results = []
    for test_case in dataset:
        results.append(run_test_case(test_case))
    return results


dataset = [
    {"question": "What is 2 + 2?",      "expected": "4"},
    {"question": "Capital of France?",  "expected": "Paris"},
    {"question": "Color of the sky?",   "expected": "Blue"},
    {
    "question": 'Reply with ONLY a JSON object, no other text: {"capital": "Paris", "country": "France"}',
    "expected": "a JSON object with capital Paris and country France",
    "format": "json",
},

]

results = run_eval(dataset)

for r in results:
    line = f'{r["test_case"]["question"]} → {r["output"]} | score: {r["score"]}'
    if r["syntax_score"] is not None:
        line += f' (syntax: {r["syntax_score"]}, task: {r["task_score"]})'
    print(line)
