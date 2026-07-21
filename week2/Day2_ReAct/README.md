# ReAct (Reasoning + Acting)

## Overview

**ReAct (Reasoning + Acting)** is one of the most important design patterns for building AI agents.

Instead of generating a final answer immediately, the model:

1. Thinks about the problem.
2. Chooses an appropriate tool.
3. Executes the tool.
4. Observes the result.
5. Decides whether another tool is needed.
6. Repeats until the task is complete.

This reasoning loop enables LLMs to solve problems that require external information or multiple steps.

Modern AI agent frameworks are built around this idea.

Examples include:

- ChatGPT with tools
- Claude with tools
- LangChain Agents
- LangGraph
- LlamaIndex Agents
- OpenAI Agents SDK

---

# Why ReAct is Necessary

## 1. LLM Knowledge is Static

Large Language Models are trained on historical data.

They **do not automatically know**:

- Today's weather
- Live stock prices
- Current exchange rates
- Latest product prices
- Database records
- Company-specific information

Example:

```
What is today's weather in Delhi?
```

An LLM cannot reliably answer unless it can access a weather service.

---

## 2. External Tools Solve This Problem

Developers connect external tools to the model.

Examples:

- Weather API
- Calculator
- Database
- Search Engine
- Email API
- Calendar API
- Product Catalog
- CRM System

Instead of guessing, the LLM retrieves real information.

---

## 3. Hardcoding Tool Logic Doesn't Scale

Imagine an application with dozens of tools.

Example:

- Calculator
- Weather
- Currency conversion
- Maps
- Database
- Gmail
- Calendar
- Shopping API

Writing manual logic for every possible combination quickly becomes impossible.

Example:

```
If weather requested
    call weather

If currency requested
    call converter

If weather + currency
    call weather then converter

If calendar + email
    call calendar then email
```

As the number of tools increases, the number of possible workflows grows rapidly.

The ReAct pattern allows the model to decide dynamically which tools to use and in what order.

---

# The ReAct Cycle

A ReAct agent repeatedly performs three steps:

```text
Thought
    ↓
Action
    ↓
Observation
    ↓
Thought
    ↓
Action
    ↓
Observation
    ↓
...
Final Answer
```

This loop continues until the model determines that it has enough information.

---

# Step 1: Thought

The model first reasons about the user's request.

Example:

User:

```
I have ₹5000.
What is the price of an iPhone 17,
and how much money will I have left?
```

The model might internally reason:

```
I don't know the current price.

I need to use the product lookup tool.

After that, I must subtract the price from ₹5000.
```

The thought determines the next action.

> **Note:** In production systems, internal reasoning is often hidden from the user. Many APIs expose only the tool calls and the final answer, not the model's private reasoning.

---

# Step 2: Action

The model chooses the appropriate tool.

Example:

```
Action:
lookup_product_price

Input:
iPhone 17
```

The application executes the tool.

Example Python function:

```python
def get_product_price(product_name):
    ...
```

The tool returns the requested information.

---

# Step 3: Observation

The tool returns data.

Example:

```
Observation:

Price = ₹89,999
```

The model updates its knowledge.

Now it knows:

- User budget = ₹5000
- Phone price = ₹89,999

It can continue reasoning.

---

# Another Thought

The model thinks again.

```
Now I know the price.

Next I should calculate

5000 - 89999
```

---

# Another Action

```
Action:

Calculator

Input:

5000 - 89999
```

---

# Observation

Calculator returns:

```
-84999
```

Now the model has all necessary information.

---

# Final Answer

```
The iPhone 17 costs ₹89,999.

You currently have ₹5,000.

After purchasing it, you would need an additional ₹84,999.
```

The agent stops because no more tools are required.

---

# Complete ReAct Flow

```text
User Question
       │
       ▼
LLM

Thought:
Need product price
       │
       ▼
Action:
Product Lookup
       │
       ▼
Observation:
₹89,999
       │
       ▼
Thought:
Need subtraction
       │
       ▼
Action:
Calculator
       │
       ▼
Observation:
-84,999
       │
       ▼
Final Answer
```

---

# Tool Definition

A tool is simply a function that the agent can call.

Example:

```python
def calculator(expression):
    ...
```

Example:

```python
def weather(city):
    ...
```

Example:

```python
def search_product(product_name):
    ...
```

The LLM does not execute Python code itself.

Instead, it decides **which tool should be called**.

The application executes the function and returns the result.

---

# System Prompt

The system prompt tells the model:

- Which tools exist
- How to use them
- When to stop
- Expected output format

Example:

```
You are an AI assistant.

Available tools:

1. calculator
2. product_lookup

When you need external information,
call the appropriate tool.

Continue reasoning until the task is complete.

Finally provide the answer.
```

Without clear instructions, the model may:

- Ignore tools
- Hallucinate answers
- Use the wrong tool
- Stop too early

---

# The Agent Loop

A typical ReAct agent repeatedly performs the following operations.

```text
Receive User Input
        │
        ▼
Ask LLM

LLM returns:

Thought
Action
        │
        ▼
Execute Tool
        │
        ▼
Observation
        │
        ▼
Send Observation back to LLM
        │
        ▼
More actions needed?
       / \
      Yes  No
      │     │
      ▼     ▼
Repeat   Final Answer
```

---

# Maintaining Memory

Each iteration adds information to the conversation history.

Example:

```text
User:
Price of iPhone?

Assistant:
Use Product Tool

Observation:
₹89,999

Assistant:
Need calculator

Observation:
₹84,999
```

The agent remembers previous observations because they remain in the conversation context.

Without memory, the model would repeatedly ask for the same information.

---

# Example Agent

User:

```
I have ₹5000.

What is the price of an iPhone 17,
and how much money will I have left?
```

Iteration 1

```
Thought

Need product price.
```

↓

```
Action

Lookup Product
```

↓

```
Observation

₹89,999
```

Iteration 2

```
Thought

Need subtraction.
```

↓

```
Action

Calculator
```

↓

```
Observation

-84,999
```

Iteration 3

```
Final Answer

Phone price: ₹89,999

Money remaining:
−₹84,999
```

---

# Advantages of ReAct

- Handles multi-step reasoning.
- Retrieves real-time information using tools.
- Dynamically chooses tools.
- Reduces hallucinations.
- Supports complex workflows.
- Easier to extend with new tools.
- Enables autonomous AI agents.

---

# Limitations

- More API calls increase latency.
- Tool execution can fail.
- Poor prompts can lead to incorrect tool selection.
- Conversation history grows over time, increasing token usage.
- Requires careful error handling.

---

# Best Practices

- Define tools clearly.
- Write explicit system prompts.
- Validate tool inputs.
- Validate tool outputs.
- Handle tool failures gracefully.
- Limit the number of reasoning iterations.
- Maintain conversation memory.
- Log tool usage for debugging.
- Prevent infinite reasoning loops.

---

# Common ReAct Use Cases

- Customer support agents
- Travel assistants
- Shopping assistants
- Coding assistants
- Database querying
- Financial assistants
- Research assistants
- Email automation
- Calendar management
- Data analysis

---

# ReAct vs Traditional Prompting

| Traditional Prompt | ReAct Agent |
|--------------------|-------------|
| Generates answer directly | Reasons before answering |
| No external tools | Uses external tools |
| Limited to model knowledge | Can access live information |
| Single response | Multi-step reasoning loop |
| Less suitable for complex tasks | Designed for autonomous workflows |

---

# Key Takeaways

- ReAct stands for **Reasoning + Acting**.
- It enables LLMs to solve multi-step problems using external tools.
- The reasoning cycle consists of **Thought → Action → Observation**.
- The loop continues until the model determines that the task is complete.
- Tools are ordinary application functions or APIs that the model can request.
- The application executes the tool and returns the result to the model.
- Clear system prompts are essential for reliable tool use.
- Conversation history acts as the agent's working memory.
- ReAct is a foundational pattern used in modern AI agent frameworks.

---

# Summary

The ReAct pattern transforms an LLM from a simple text generator into an AI agent capable of reasoning, interacting with external tools, and solving complex, multi-step tasks. By iteratively cycling through **Thought → Action → Observation**, the agent can gather real-time information, perform calculations, and make informed decisions before producing a final response. This approach forms the basis of many modern AI agent systems and is a key concept for building production-ready AI applications.