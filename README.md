# Experiment with AI

This repository tracks my day-by-day learning and practice for becoming a production-ready AI Engineer.

## Course Syllabus

- Week 1: LLM Fundamentals + API Mastery (you are here)
- Week 2: Prompt Engineering + Structured Outputs
- Week 3: RAG Foundations
- Week 4: Advanced RAG + Evaluation
- Week 5: Agents + Tool Use
- Week 6: LangGraph + MCP + Multi-Agent
- Week 7: Observability + Guardrails + Security
- Week 8: Deployment + Fine-Tuning + Capstone
- Bonus: Interview Prep + Resume Building

## Daily Setup Workflow (uv + Python 3.11)

Use this workflow whenever you start a new day folder.

1. Create a new folder for the day.
2. Initialize the project with uv.
3. Create and activate a virtual environment.
4. Add dependencies.
5. Create your code file.

### Commands

```bash
# Example: create a new folder for the day
mkdir "week2/Day3"
cd "week2/Day3"

# Initialize project
uv init

# Create virtual environment with Python 3.11
uv venv --python 3.11

# Activate venv (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Add dependencies (example)
uv add openai python-dotenv pydantic

# Create starter code file
New-Item main.py -ItemType File
```

## Recommended File Naming

- Use `main.py` for runnable demos
- Use descriptive names for topic scripts, for example:
	- `tokens.py`
	- `tickets.py`
	- `resume_parser.py`
	- `react_loop.py`

## Suggested Folder Pattern

```text
weekX/
	DayY/
		README.md
		main.py
		pyproject.toml
```

## Important Notes (from my side)

- Keep each day independent: its own `pyproject.toml`, dependencies, and README notes.
- Store API keys only in `.env` files and never hardcode secrets.
- Test every script on the same day you write it, and keep examples small and focused.
- At the end of each day, add a short summary in that day README: what worked, what failed, and what to improve tomorrow.