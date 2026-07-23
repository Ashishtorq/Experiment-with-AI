# Prompt Chaining

## Overview

**Prompt Chaining** is a production AI technique where one complex task is divided into several small, focused LLM calls.

Instead of asking one large prompt to extract data, compare results, calculate a score, make a decision, and generate a response, developers build a sequence of modular steps.

```text
Input
  ↓
Prompt 1
  ↓
Output 1
  ↓
Prompt 2
  ↓
Output 2
  ↓
Final Result
```

The output of one step becomes the input of the next.

---

## Why Prompt Chaining Is Useful

Large prompts are often difficult to:

- Debug
- Test
- Maintain
- Monitor
- Refine
- Reuse

When a large prompt produces an incorrect result, it may be difficult to determine whether the problem came from extraction, comparison, scoring, or formatting.

Prompt chaining separates these responsibilities.

```text
Extract
  ↓
Validate
  ↓
Compare
  ↓
Score
  ↓
Route
```

Each stage can be inspected and improved independently.

---

## Main Benefits

### Easier Debugging

Each intermediate result can be printed or logged.

```python
candidate_skills = extract_candidate_skills(resume_text)
required_skills = extract_required_skills(job_description)
match_result = compare_skills(candidate_skills, required_skills)

print(candidate_skills)
print(required_skills)
print(match_result)
```

If the final result is wrong, the developer can identify which step failed.

### Better Reliability

A focused prompt is easier for an LLM to follow.

```text
Extract only the technical skills from this resume.
```

This is usually more reliable than asking the model to extract skills, evaluate experience, calculate a score, and write an email in one call.

### Modular Design

Each part of the workflow can be changed independently.

For example:

- Replace the resume parser.
- Improve the job-description extractor.
- Change the scoring formula.
- Update routing thresholds.
- Use a different model for one step.

### Cost Optimization

Different models can be selected for different tasks.

```text
Simple extraction
    ↓
Smaller, cheaper model

Complex comparison
    ↓
More capable model

Email generation
    ↓
Writing-focused model
```

### Better Testing

Each function can be tested separately.

```python
def test_extract_candidate_skills():
    result = extract_candidate_skills(sample_resume)

    assert "Python" in result.skills
```

---

## Prompt Chaining vs ReAct

Prompt Chaining and ReAct both support multi-step workflows, but they work differently.

| Prompt Chaining | ReAct |
|---|---|
| Developer defines the sequence | Model decides the next action |
| Deterministic workflow | Dynamic workflow |
| Easier to test | More flexible |
| Easier to debug | Harder to predict |
| Best for known pipelines | Best for open-ended tasks |
| Steps run in a fixed order | Tools are selected during execution |

### Prompt Chaining

```text
Extract Resume Skills
        ↓
Extract JD Skills
        ↓
Compare Skills
        ↓
Calculate Score
        ↓
Route Candidate
```

### ReAct

```text
Thought
  ↓
Action
  ↓
Observation
  ↓
Thought
  ↓
Next Action
```

In prompt chaining, the developer controls the workflow. In ReAct, the model dynamically decides what to do next.

---

# Resume Matching Pipeline

A recruitment workflow can be implemented as a prompt chain.

```text
Resume
   ↓
Extract Candidate Skills
   ↓
Candidate Skills

Job Description
   ↓
Extract Required Skills
   ↓
Required Skills

Candidate Skills + Required Skills
   ↓
Compare and Score
   ↓
Match Result

Match Result
   ↓
Conditional Routing
   ↓
Shortlist, Review, or Reject
```

---

## Step 1: Extract Candidate Skills

```python
def extract_candidate_skills(resume_text: str) -> str:
    prompt = f"""
You are a resume parsing assistant.

Extract only the technical skills from the resume below.

Return the skills as a comma-separated list.
Do not include explanations.

Resume:
{resume_text}
"""

    return call_llm(prompt)
```

Example output:

```text
Python, FastAPI, PostgreSQL, Docker, AWS
```

This step should perform extraction only.

---

## Step 2: Extract Required Skills from the Job Description

```python
def extract_required_skills(job_description: str) -> str:
    prompt = f"""
You are a job-description parsing assistant.

Extract only the required technical skills from the job description below.

Return the skills as a comma-separated list.
Do not include explanations.

Job Description:
{job_description}
"""

    return call_llm(prompt)
```

Example output:

```text
Python, FastAPI, PostgreSQL, Docker, Kubernetes
```

---

## Step 3: Compare the Skills

```python
def compare_skills(
    candidate_skills: str,
    required_skills: str,
) -> str:
    prompt = f"""
You are a recruitment evaluation assistant.

Compare the candidate skills with the required skills.

Candidate Skills:
{candidate_skills}

Required Skills:
{required_skills}

Return:
- Matched skills
- Missing skills
- Match score from 0 to 100
- Final verdict
"""

    return call_llm(prompt)
```

Example output:

```text
Matched Skills:
Python, FastAPI, PostgreSQL, Docker

Missing Skills:
Kubernetes

Match Score:
80

Verdict:
Good Match
```

---

## Step 4: Apply Conditional Logic

Normal Python code should handle deterministic business rules.

```python
def route_candidate(score: float) -> str:
    if score >= 80:
        return "Shortlist candidate"

    if score >= 60:
        return "Send for manual review"

    return "Reject candidate"
```

An LLM is usually unnecessary for:

- Numerical thresholds
- Approval rules
- Access control
- Routing
- Financial calculations
- Fixed business policies

---

# Structured Outputs

Comma-separated text is easy to read, but structured JSON is more reliable for application code.

## Skill Extraction Schema

```python
from pydantic import BaseModel


class SkillExtraction(BaseModel):
    skills: list[str]
```

## Match Result Schema

```python
from pydantic import BaseModel, Field


class MatchResult(BaseModel):
    matched_skills: list[str]
    missing_skills: list[str]
    score: float = Field(ge=0, le=100)
    verdict: str
```

Example JSON:

```json
{
  "matched_skills": [
    "Python",
    "FastAPI",
    "PostgreSQL"
  ],
  "missing_skills": [
    "Kubernetes"
  ],
  "score": 75,
  "verdict": "Manual Review"
}
```

Structured output is easier to:

- Parse
- Validate
- Store
- Test
- Pass to another step

---

# Validate Every Step

Each LLM response should be validated before being passed forward.

```python
skills = SkillExtraction.model_validate_json(raw_response)
```

Without validation:

```text
Invalid Step 1 Output
        ↓
Step 2 Receives Bad Data
        ↓
Incorrect Comparison
        ↓
Incorrect Final Decision
```

LLM output should always be treated as untrusted data.

---

# Normalize Extracted Data

The same skill may appear in different forms.

```text
Node
Node.js
NodeJS
node js
```

A simple normalization function:

```python
def normalize_skill(skill: str) -> str:
    return skill.strip().lower()
```

More advanced systems may use:

- Alias dictionaries
- Embeddings
- Skill taxonomies
- Semantic similarity
- Ontologies

---

# Error Handling

Each stage should handle failures independently.

```python
try:
    candidate_skills = extract_candidate_skills(resume_text)
except Exception as error:
    print("Candidate skill extraction failed:")
    print(error)
```

Possible failures include:

- Invalid JSON
- Empty model output
- API timeouts
- Rate-limit errors
- Missing input
- Validation errors
- Unsupported file formats

Independent error handling prevents one failed stage from silently corrupting the entire pipeline.

---

# Rate Limiting

A simple delay can be added between API calls.

```python
import time

candidate_skills = extract_candidate_skills(resume_text)

time.sleep(5)

required_skills = extract_required_skills(job_description)
```

However, `time.sleep(5)` is only a basic throttling technique.

It does not guarantee that rate limits will not occur.

Production systems should also use:

- Exponential backoff
- Retry limits
- Provider retry headers
- Request queues
- Concurrency controls
- Token monitoring

---

# Environment Variables

API keys should not be hardcoded.

## `.env`

```env
GROQ_API_KEY=your_api_key
```

## Python

```python
import os
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing")
```

Add `.env` to `.gitignore`.

```gitignore
.env
```

---

# Prompt Templates with F-Strings

F-strings allow values to be inserted into prompt templates.

```python
prompt = f"""
Candidate Skills:
{candidate_skills}

Required Skills:
{required_skills}
"""
```

Schemas can be formatted with `json.dumps()`.

```python
import json

schema_text = json.dumps(schema, indent=2)
```

---

# Observability

Prompt chaining makes each stage easier to monitor.

Useful information to record includes:

- Step name
- Input size
- Output
- Model used
- Token usage
- Latency
- Errors
- Retry count
- Validation result

```python
print("Step 1: Candidate skills")
print(candidate_skills)

print("Step 2: Required skills")
print(required_skills)

print("Step 3: Match result")
print(match_result)
```

Production applications should use structured logging rather than relying only on `print()`.

---

# Cost Optimization

Prompt chaining can increase the number of API calls, but it also provides better cost control.

Useful strategies include:

- Use smaller models for simple extraction.
- Use stronger models only for difficult comparisons.
- Cache parsed resumes.
- Cache parsed job descriptions.
- Avoid resending unnecessary text.
- Limit output tokens.
- Use deterministic code for scoring.
- Track cost and token usage per step.

---

# Prompt Chaining Patterns

## Sequential Chain

Each step depends on the previous result.

```text
Extract
  ↓
Summarize
  ↓
Classify
  ↓
Respond
```

## Parallel Chain

Independent steps run separately.

```text
             ┌─ Extract Skills
Resume ──────┼─ Extract Education
             └─ Extract Experience
```

## Conditional Chain

The next step depends on a result.

```text
Calculate Score
      ↓
Score ≥ 80?
   /       \
 Yes        No
 ↓           ↓
Shortlist   Review or Reject
```

## Validation Chain

One stage generates an output and another checks it.

```text
Generate Output
      ↓
Validate Output
      ↓
Correct or Retry
```

## Map-Reduce Chain

Large input is split into smaller pieces.

```text
Large Document
      ↓
Split into Chunks
      ↓
Process Each Chunk
      ↓
Combine Results
      ↓
Final Output
```

---

# When to Use Prompt Chaining

Prompt chaining is useful when:

- A task has clear stages.
- Each stage has a separate responsibility.
- Intermediate results need inspection.
- Different models suit different steps.
- Business logic should remain deterministic.
- Individual stages require separate testing.

# When Not to Use It

Prompt chaining may be unnecessary when:

- The task is simple.
- One structured prompt already works reliably.
- Latency is critical.
- Extra calls add no meaningful benefit.
- The workflow requires dynamic tool selection.

For open-ended workflows, ReAct or agent-based systems may be more appropriate.

---

# Best Practices

- Give each prompt one clear responsibility.
- Use structured outputs where possible.
- Validate every LLM response.
- Keep fixed business rules in application code.
- Log intermediate outputs.
- Add retry logic to each stage.
- Use smaller models for simple tasks.
- Pass only necessary context.
- Test each stage independently.
- Do not rely only on `time.sleep()` for rate limiting.

---

# Common Mistakes

## One Prompt Doing Everything

```text
Extract, compare, score, email, and decide.
```

This is difficult to test and debug.

## Passing Unvalidated Output

```python
result_2 = next_step(result_1)
```

If `result_1` is malformed, the next stage may fail.

## Using LLMs for Simple Logic

Do not ask a model whether `80` is greater than `60`. Use normal code.

## No Logging

Without intermediate logs, it is difficult to identify the failing stage.

## Excessive Chaining

Too many calls can increase:

- Latency
- Cost
- Complexity
- Failure points

Every stage should have a clear purpose.

---

# Prompt Chaining Checklist

Before deployment, verify that:

- Each step has one responsibility.
- Every output has a defined structure.
- Every response is validated.
- Failures are handled independently.
- Intermediate results are logged.
- Deterministic logic is written in code.
- Token usage is monitored.
- Rate-limit retries are configured.
- Edge cases are tested.

---

# Key Takeaways

- Prompt chaining divides a complex task into smaller LLM calls.
- The output of one stage becomes the input of the next.
- The developer controls the execution order.
- It is easier to debug than one large prompt.
- Different models can be used for different stages.
- Structured outputs improve reliability.
- Deterministic code should handle thresholds and routing.
- Prompt chaining differs from ReAct because ReAct dynamically selects actions.
- Every intermediate response should be validated.
- Chaining improves maintainability but may increase latency and API calls.

---

# Summary

Prompt Chaining is a practical design pattern for building reliable AI applications.

In the resume evaluation example:

1. Candidate skills are extracted.
2. Required job skills are extracted.
3. Both outputs are compared.
4. A score and verdict are generated.
5. Deterministic application logic routes the candidate.

This design improves debugging, testing, maintainability, observability, and cost optimization while keeping the developer in control of the workflow.
