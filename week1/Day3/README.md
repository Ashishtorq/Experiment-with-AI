# Tokens

## Key Concepts Explained

### What is a Token?

- Large Language Models (LLMs) process text as numbers, not as words.
- Since words and characters are unpredictable, models split text into reusable building blocks called **tokens**.
- Common words (e.g., `"the"`) may be represented by a single token, while uncommon or complex words (e.g., `"Pratyush"`) may be broken into multiple smaller tokens.
- **Tokenization** is the process of converting text into tokens and then mapping those tokens to numerical representations that the model can understand.

---

### Why Tokens Matter for Costs

- LLM API pricing is based on the **number of tokens**, not the number of words.
- Total API cost is calculated using:
  - **Input Tokens (Prompt Tokens)**
  - **Output Tokens (Completion Tokens)**

**Formula:**

```text
Total Cost = Input Tokens + Output Tokens
```

---

### Managing LLM Costs in Production

#### Max Tokens

- The `max_tokens` parameter limits the maximum number of tokens the model can generate.
- Setting an appropriate limit helps prevent excessively long responses and reduces API costs.

#### Finish Reason

- The `finish_reason` field indicates why the model stopped generating text.
- Common values include:
  - `stop` → The model completed its response naturally.
  - `length` → The response was cut off because it reached the maximum token limit.

Checking this field helps determine whether a response is complete or truncated.

---

## Practical Takeaways

### 1. Coding Best Practices

- Avoid naming Python files `token.py`.
- This can create circular import issues because it conflicts with internal libraries.
- Use descriptive names such as:
  - `tokens.py`
  - `token_utils.py`
  - `tokenizer.py`

---

### 2. Performance Monitoring

To monitor API usage and costs, inspect the `usage` field in the API response.

It typically contains:

- `prompt_tokens` – Number of input tokens
- `completion_tokens` – Number of output tokens
- `total_tokens` – Total tokens consumed

Tracking these values helps estimate API costs and optimize prompts.

---

### 3. Managing Response Length

- Adjust the `max_tokens` parameter to control the length of generated responses.
- This ensures:
  - Lower API costs
  - Predictable outputs
  - Better efficiency for production AI applications

---

## Summary

- LLMs understand **tokens**, not words.
- **Tokenization** converts text into numerical representations.
- API pricing depends on the total number of input and output tokens.
- Use `max_tokens` to control response length and costs.
- Check `finish_reason` to verify whether a response completed naturally or was truncated.
- Monitor the `usage` field to track token consumption.
- Follow good coding practices by avoiding filenames that conflict with Python's internal modules.
