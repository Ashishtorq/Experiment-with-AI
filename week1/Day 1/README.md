# AI Engineer Course Introduction & Environment Setup

## Course Overview

### Goal of the Course

- The primary objective is to become a **production-ready AI Engineer**.
- The course emphasizes practical, industry-relevant skills instead of extensive mathematical theory or traditional machine learning lectures.
- Content is designed around real-world engineering tasks and common AI interview topics.

---

### Target Audience

This course is suitable for:

- College students interested in AI.
- Software engineers transitioning into AI Engineering.
- Developers working in service-based companies who want to contribute to AI projects.
- Anyone with basic programming knowledge looking to build AI applications.

---

### Prerequisites

Before starting, you should have:

- Basic knowledge of **Python**.
- Familiarity with writing and running Python programs.
- A development environment for coding and executing scripts.

---

## Course Curriculum

The course covers several important AI engineering topics, including:

- LLM Fundamentals
- Prompt Engineering
- Tokenization
- System Roles & Temperature
- Retrieval-Augmented Generation (RAG)
- AI Agents
- LangGraph
- Observability
- Deployment of AI Applications

The focus throughout is on building production-ready AI systems.

---

# Environment Setup

The development environment is lightweight and does **not** require high-end hardware.

Even a system with approximately **4 GB RAM** is sufficient for following along because most AI models are accessed through cloud APIs instead of running locally.

---

## Required Software

### 1. Python

Python is the primary programming language used throughout the course.

Verify the installation:

```bash
python --version
```

---

### 2. Visual Studio Code (VS Code)

VS Code is the recommended code editor.

Recommended extensions:

- Python
- Pylance
- Jupyter

These extensions provide:

- Syntax highlighting
- Intelligent code completion
- Debugging support
- Notebook execution

---

### 3. Git & GitHub

Git is used for version control, while GitHub is used for hosting and sharing projects.

Verify the installation:

```bash
git --version
```

---

### 4. uv

`uv` is a fast Python package and environment manager used throughout the course.

Benefits include:

- Faster dependency installation
- Virtual environment management
- Simplified project setup

Verify the installation:

```bash
uv --version
```

---

### 5. Microsoft Terminal

Microsoft Terminal is recommended for a better command-line experience on Windows.

Advantages include:

- Multiple terminal tabs
- Better customization
- Improved usability compared to the default Command Prompt

---

# Cloud Services

Instead of running large language models locally, the course uses cloud-based services.

This approach:

- Requires less hardware.
- Provides faster inference.
- Simplifies development.
- Makes projects easier to deploy.

---

## Groq

Groq provides access to high-performance Large Language Models (LLMs) through cloud APIs.

Typical use cases:

- Chat applications
- AI assistants
- Code generation
- Text summarization

---

## Qdrant

Qdrant is a **Vector Database** used for Retrieval-Augmented Generation (RAG).

It stores vector embeddings and enables efficient semantic search.

Typical use cases:

- Document retrieval
- Knowledge bases
- AI search systems
- RAG pipelines

---

## Managing API Keys

Store API keys securely using a `.env` file.

Example:

```env
GROQ_API_KEY=your_api_key
QDRANT_API_KEY=your_api_key
```

Benefits:

- Prevents exposing secrets in source code.
- Makes configuration easier across different environments.
- Improves application security.

---

# Verifying the Setup

After installation, verify that all required tools are available.

Example commands:

```bash
python --version
uv --version
git --version
code --version
```

If each command returns a version number, the environment is ready for development.

---

# Best Practices

- Keep Python and project dependencies updated.
- Use virtual environments for each project.
- Never hardcode API keys in source code.
- Store secrets in a `.env` file.
- Use Git to track project changes.
- Push projects regularly to GitHub for backup and collaboration.

---

# Summary

- The course is designed to prepare you for real-world AI engineering.
- A basic understanding of Python is sufficient to begin.
- The curriculum focuses on practical topics such as LLMs, RAG, AI Agents, LangGraph, Observability, and Deployment.
- Development is done using **Python**, **VS Code**, **Git**, **uv**, and **Microsoft Terminal**.
- Large language models are accessed through **Groq**, while **Qdrant** is used as the vector database for RAG applications.
- Store API credentials securely in a `.env` file.
- Verify all installations before starting development to ensure a smooth learning experience.
