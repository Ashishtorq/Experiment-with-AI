# AI-Powered Resume Evaluator (ATS Project)

## Project Overview

This project demonstrates how to build an **AI-powered Resume Evaluator** that automates candidate screening by comparing resumes against a job description (JD).

The system performs the following tasks:

1. Parse the Job Description.
2. Parse candidate resumes (PDF/DOCX).
3. Convert both into structured JSON.
4. Compare the resume with the job description.
5. Generate a match score and detailed feedback.

---

# Project Workflow

```text
Job Description
        │
        ▼
Extract Job Requirements
        │
        ▼
Structured Job Description (JSON)
        │
        │
        │
Resume (PDF / DOCX)
        │
        ▼
Extract Resume Text
        │
        ▼
Structured Resume (JSON)
        │
        ▼
Compare Resume with Job Description
        │
        ▼
Match Score + Strengths + Weaknesses + Verdict
```

---

# 1. Job Description Parsing

The application accepts an unstructured job description and converts it into a structured format using an LLM and a predefined schema.

Typical information extracted includes:

- Job role
- Required skills
- Preferred skills
- Minimum experience
- Responsibilities
- Qualifications
- Education requirements

## Example Pydantic Schema

```python
from pydantic import BaseModel

class JobDescription(BaseModel):
    role: str
    required_skills: list[str]
    preferred_skills: list[str] = []
    minimum_experience: float | None = None
    responsibilities: list[str] = []
    qualifications: list[str] = []
```

### Benefits

- Standardizes different job descriptions.
- Makes comparison easier.
- Eliminates manual parsing.

---

# 2. Resume Schema Design

Since resumes vary significantly in format, a generalized schema is used to represent candidate information consistently.

Typical fields include:

- Name
- Email
- Phone number
- Skills
- Education
- Certifications
- Projects
- Experience

## Experience Model

```python
from pydantic import BaseModel

class Experience(BaseModel):
    company: str
    role: str
    start_date: str | None = None
    end_date: str | None = None
    responsibilities: list[str] = []
    technologies: list[str] = []
```

## Resume Model

```python
class Resume(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    skills: list[str] = []
    education: list[str] = []
    experiences: list[Experience] = []
    certifications: list[str] = []
    projects: list[str] = []
```

### Why Use Optional Fields?

Not every resume contains:

- Email
- Certifications
- Projects
- Phone number

Optional fields prevent validation failures when information is unavailable.

---

# 3. Resume Parsing

Candidate resumes are converted into plain text before being processed by the LLM.

Supported file types:

- PDF
- DOCX

Common libraries include:

- **pypdf** (or **PyPDF2**) for PDF extraction
- **python-docx** for Word documents

The parser should extract:

- Paragraphs
- Headings
- Lists
- Tables (when present)

Extracting text from tables helps preserve structured information such as education, certifications, and project details.

---

# 4. Structured Resume Extraction

The extracted resume text is sent to an LLM with instructions to return structured JSON.

Typical workflow:

```text
Resume File
      │
      ▼
Extract Text
      │
      ▼
LLM
      │
      ▼
JSON Response
      │
      ▼
Pydantic Validation
      │
      ▼
Resume Object
```

Using structured outputs makes downstream processing more reliable than parsing free-form text.

---

# 5. Resume Matching

After parsing both the job description and the resume, the application compares:

- Required skills
- Preferred skills
- Experience
- Education
- Certifications
- Projects
- Previous job roles

The result is an evaluation describing how well the candidate matches the job requirements.

---

# 6. Match Result

A structured evaluation may include:

```python
class MatchResult(BaseModel):
    score: float
    strengths: list[str]
    weaknesses: list[str]
    feedback: str
    verdict: str
```

Typical output includes:

- Match score (0–100)
- Candidate strengths
- Missing skills
- Areas for improvement
- Overall recommendation

---

# 7. Rate Limiting

When sending multiple API requests, applications should avoid exceeding provider rate limits.

A simple approach is:

```python
import time

time.sleep(5)
```

This introduces a delay between requests.

### Note

A fixed delay may reduce request frequency, but it does **not** guarantee protection from rate limits or lower API costs.

Production systems should additionally:

- Handle rate-limit errors.
- Retry requests with exponential backoff.
- Respect provider-specific rate limits.
- Monitor API usage and token consumption.

---

# 8. Error Handling

The application should safely handle:

- Unsupported file types.
- Empty resumes.
- Corrupted PDF or DOCX files.
- Invalid JSON returned by the LLM.
- Missing fields.
- Validation failures.
- API errors.

Example:

```python
from pydantic import ValidationError

try:
    resume = Resume.model_validate_json(raw_response)
except ValidationError as error:
    print(error)
```

Proper error handling improves application stability.

---

# 9. Practical Evaluation

Once the structured resume is generated, it is compared against the structured job description.

The evaluation can explain:

- Why the candidate matches the role.
- Which required skills are missing.
- Whether the experience level is sufficient.
- Strengths of the candidate.
- Weaknesses or gaps.
- An overall recommendation.

Providing explanations makes the evaluation more transparent than returning only a numerical score.

---

# 10. ATS-Style Workflow

```text
Job Description
        │
        ▼
Structured JD
        │
        │
Resume
        │
        ▼
Text Extraction
        │
        ▼
Structured Resume
        │
        ▼
Matching Engine
        │
        ▼
Match Score
Strengths
Weaknesses
Feedback
Verdict
```

---

# Best Practices

- Use Pydantic schemas for both job descriptions and resumes.
- Keep optional resume fields nullable.
- Validate all LLM responses before using them.
- Reject unsupported document formats gracefully.
- Extract information from document tables when possible.
- Avoid hardcoding API keys.
- Monitor API usage and rate limits.
- Prefer deterministic business logic for final scoring.
- Use the LLM primarily for information extraction and qualitative feedback.

---

# Real-World Applications

Resume evaluation systems can be used for:

- Applicant Tracking Systems (ATS)
- HR automation
- Resume screening
- Candidate ranking
- Talent acquisition
- Recruitment assistance

AI-generated evaluations should assist recruiters rather than replace human decision-making.

---

# Summary

- Job descriptions are parsed into structured JSON using an LLM and Pydantic.
- Resumes from PDF and DOCX files are converted into structured resume objects.
- Structured job descriptions and resumes are compared to evaluate candidate suitability.
- The system generates a match score along with strengths, weaknesses, feedback, and an overall verdict.
- Proper validation, error handling, and rate-limit management are essential for building reliable AI-powered recruitment applications.