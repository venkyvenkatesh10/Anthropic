Building with the Claude API — Lessons 1–3 README
My learning notes and practice work from Anthropic's "Building with the Claude API" course on Claude Academy.
I am a Forward Deployed Engineer learning AI/LLM engineering in public. For every section of the course, I study the lessons, pass the quiz, build the practice code, and write a Medium post about what I learned.

Progress
Section
Lessons
Status
Quiz
Medium post
Accessing Claude with the API
Lessons 1–8
✅ Completed
✅ Passed
Published — The Model Remembers Nothing: 8 Lessons From Accessing the Claude API
Prompt Evaluation
Lessons 9–14
✅ Completed
✅ Passed
Ready — "Learning in Public: What Prompt Evaluation Taught Me About Measuring AI"
Prompt Engineering Techniques
5 lessons
✅ Completed
✅ Passed (5/5)
Ready — "Learning in Public: What Prompt Engineering Taught Me About Giving Better Instructions"
Tool Use with Claude
13 lessons
⏭️ Next
—
—

Section 1 — Accessing Claude with the API (Lessons 1–8)
How to talk to Claude directly from code, with no chat window in between.
#
Lesson
What I learned
1
Accessing the API
Using the API means my code sends a request and the model responds — every behavior setting becomes my design decision.
2
Getting an API key
The API key is my identity and billing account. It lives in a .env file on the server, never in client code or a public repo.
3
Making a request
A request needs 4 things: API key, model name, messages, and max_tokens (a cap, not a target). Before answering, Claude breaks text into tokens — the unit everything is priced and limited in.
4
Multi-Turn conversations
The API is stateless — Claude remembers nothing between calls. My app keeps the full conversation history and re-sends it with every request.
5
System prompts
The system prompt is the model's job description (role, tone, rules) and sits above the conversation. Example: a math tutor that gives hints instead of answers.
6
Temperature
A consistency dial, not a quality dial. Near 0.0 = predictable, factual output. Higher = more variety. For data work, I keep it near zero.
7
Response streaming
Tokens arrive as they are generated, so the answer types itself out. Total time barely changes; the app feels much faster. What matters is time to first token.
8
Structured data
To get clean JSON with nothing extra: prefill the assistant message with the opening of the JSON block + set a stop sequence at the end. Constrain the model — don't just ask it nicely.
Practice files I built:
File
What it does
test_claude.py
Basic chat with Claude; helper functions to add user/assistant messages and re-send the full history each turn.
mathtutor.py
A math tutor using a system prompt — gives hints and asks questions instead of giving answers directly.
streaming.py
The same request with streaming on, printing each token as it arrives.
.env / .env.example
Stores the real API key (.env, never shared) and a blank template (.env.example, safe to share).
Quiz note: My one wrong first instinct in this section was "ask Claude very nicely to only return JSON." The correct answer was prefill + stop sequences. That miss became the opening of my first Medium post.

Section 2 — Prompt Evaluation (Lessons 9–14)
How to stop judging prompts by feel and start measuring them with a fixed dataset and graders.
#
Lesson
What I learned
9
Prompt evaluation
Engineering = writing the prompt. Evaluation = measuring it (test against expected answers, compare versions, check for errors). Testing once or twice and trusting it is a trap — real users give inputs I never imagined.
10
A typical eval workflow
5 steps: draft prompt → create eval dataset → run inputs through Claude → grade responses (1–10) → change prompt and repeat on the same dataset. Course example: prompt v1 averaged 7.66, v2 (one line added) averaged 8.7.
11
Generating test datasets
Let a faster model (Haiku) generate the test cases, then save them to a file (e.g. dataset.json). A saved dataset is a fixed exam — every prompt version takes the same test. Course example: a prompt that writes AWS code (Python / JSON / Regex only).
12
Running the eval
Three functions: run_prompt (one case through Claude), run_test_case (run + grade one case), run_eval (loop the whole dataset). Build the pipeline first — grading starts as a placeholder score with a TODO.
13
Model based grading
A second model call acts as the examiner. Ask it for strengths, weaknesses, reasoning, and a score — a grader asked only for a score defaults to a safe middle score (~6).
14
Code based grading
Programs check what programs can check: valid JSON (json.loads), valid Python (ast.parse), valid Regex (re.compile). Valid = 10, invalid = 0. Final score = (model score + syntax score) ÷ 2.
Practice files I built:
File
What it does
prompt eval.py
My full evaluation pipeline: run_prompt sends a test case to Claude, grade_with_model scores the answer 0–10 with a second Claude call, run_test_case combines task + syntax scores, run_eval runs the whole dataset.
GRADERS.py
The three syntax validators (validate_json, validate_python, validate_regex) in one VALIDATORS table, reused by the pipeline.
My results: On my 3-case dataset, the model grader scored the answers 30/30 — answers that exact string matching would have scored 0/30 (because "The capital of France is Paris" is not the string "Paris"). My 4-case run, including a case that must return pure JSON, scored 10.0 on the JSON case (syntax 10 + task 10).
The main lesson: the score is a property of the grader as much as of the prompt. Each grader measures a different definition of success — code graders check structure, model graders check meaning, and valid syntax does not guarantee a correct answer.

Section 3 — Prompt Engineering Techniques (5 lessons)
How to improve a prompt itself. The course improves one running example — a meal-plan prompt — step by step through every lesson.
#
Lesson
What I learned
1
Prompt engineering
Improving a prompt to get more reliable, higher-quality outputs. It is not training a model, building a model, or changing the model — the instructions are usually the bug.
2
Being clear and direct
Give an order, not a topic. "Create a 30-minute workout plan for beginners" beats "I was wondering about workouts" — action + task + specifics in the first line. Meal plan: "Help me eat better" → "Create a 7-day dinner plan."
3
Being specific
Add the requirements and constraints (diet, budget, time, allergies). Every detail I omit is a decision the model makes for me on every run. Best added based on eval failures, not hunches.
4
Structure with XML tags
Put each part of the prompt in a labeled box (<instructions>, <preferences>, <document>) so the model never confuses instructions with content. Most valuable with large amounts of content.
5
Providing examples
Sample input/output pairs = one-shot / multi-shot prompting. Some patterns are easier to show than describe. Quiz example: Claude missing sarcasm is fixed by showing sarcastic posts labeled Negative, not by writing a longer rule.
Quiz result: 5 out of 5.
The main lesson: the model never changed in this section — only the asking did. When output is wrong, I check in order: Is it a real instruction? What details did I leave undecided? Are instructions and content separated? Have I shown an example of the hard case?

How to run the practice code
# 1. Install dependencies
pip install anthropic python-dotenv

# 2. Add your API key to a .env file (never commit this file)
ANTHROPIC_API_KEY=your-key-here

# 3. Run the exercises
python test_claude.py
python mathtutor.py
python streaming.py
python "prompt eval.py"
The practice code uses model claude-sonnet-4-6 with max_tokens=1000, and loads the API key from .env using load_dotenv() — the key never appears in any code file.

Key takeaways from Sections 1–3
The API is stateless — my app carries the conversation history.
Constrain, don't persuade — prefill + stop sequences for structured output.
Don't grade by feel — a fixed dataset + graders turn "seems better" into a score.
The grader is the measurement — design its criteria as carefully as the prompt.
Fix form with code, meaning with a model — validators for syntax, model graders for task completion.
The model is rarely the bug — clear, specific, structured instructions with examples fix most bad output.
Next
Section 4 — Tool Use with Claude, starting with Introducing tool use: letting Claude call functions and take actions, instead of only generating text.
