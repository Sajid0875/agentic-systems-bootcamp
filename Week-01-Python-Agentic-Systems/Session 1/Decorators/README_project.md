# Python Decorator Project

This is a beginner-friendly Python project that explains decorators through real-world backend and AI-style examples.

The project is written in one file:

```text
decorator_project.py
```

## Project Goal

The goal of this project is to understand how Python decorators work in real projects.

Decorators are used to add extra behavior to functions without changing the original function code.

In this project, decorators are used for:

- Timing functions
- Logging function calls
- Retrying failed functions
- Checking API keys
- Caching expensive results

## Concepts Covered

- Functions as first-class objects
- Functions passed into functions
- Functions returned from functions
- Closures
- Wrapper functions
- `*args` and `**kwargs`
- `return result`
- `functools.wraps`
- Decorators with arguments

## Decorators Used

### 1. `@timer`

Measures how long a function takes to run.

Used on:

```python
@timer
def analyze_text(text):
    ...
```

Purpose:

```text
Check function execution time.
```

---

### 2. `@log_call`

Logs when a function starts and finishes.

Used on:

```python
@log_call
def analyze_text(text):
    ...
```

Purpose:

```text
Help debug function calls.
```

---

### 3. `@retry(3)`

Retries a function if it fails.

Used on:

```python
@retry(3)
def fetch_user_data(user_id):
    ...
```

Purpose:

```text
Useful for unstable API calls, network requests, and temporary failures.
```

---

### 4. `@require_api_key`

Checks if the correct API key is provided.

Used on:

```python
@require_api_key
def access_private_data(*, api_key):
    ...
```

Purpose:

```text
Protect private functions from unauthorized access.
```

---

### 5. `@cache_result`

Stores the result of a function and returns the saved result when the same input is used again.

Used on:

```python
@cache_result
def generate_embedding(text):
    ...
```

Purpose:

```text
Avoid repeating slow or expensive calculations.
```

## Why This Project Matters

In real backend and AI systems, functions often call:

- APIs
- Databases
- LLMs
- Embedding models
- External tools
- Private services

Decorators help add common behavior around these functions without rewriting the same logic again and again.

For example:

```python
@retry(3)
def call_api():
    ...
```

means:

```text
If this API call fails, try again up to 3 times.
```

This is cleaner than writing retry logic manually everywhere.

## How Decorators Work

A decorator takes a function, wraps it inside another function, and returns the wrapper.

Simple mental model:

```text
original function
      ↓
decorator
      ↓
wrapper function
      ↓
extra behavior + original function
```

After decoration, the function name points to the wrapper, but the wrapper still remembers the original function.

## How to Run

Clone the repository or download the file.

Then run:

```bash
python decorator_project.py
```

No external libraries are required.

## Expected Output

The output will show examples of:

- Function timing
- Function logging
- Retry attempts
- API key validation
- Cached result reuse

Some retry output may change each time because the project uses random failure simulation.

## Example Output

```text
--- Text Analysis Example ---
[LOG] Calling: analyze_text
[LOG] args=('Python decorators are useful in backend and AI systems',), kwargs={}
[LOG] Finished: analyze_text
[TIMER] analyze_text took 1.00 seconds
{'text': 'Python decorators are useful in backend and AI systems', 'word_count': 8, 'character_count': 55}

--- Retry Example ---
[RETRY] Attempt 1/3
[TIMER] fetch_user_data took 1.00 seconds
{'user_id': 101, 'name': 'Ali', 'role': 'student'}

--- API Key Example ---
{'status': 'success', 'data': 'This is protected data'}

--- Cache Example ---
[TIMER] generate_embedding took 2.00 seconds
[CACHE] Saving result for generate_embedding
[11, 2, 16]
[CACHE] Returning cached result for generate_embedding
[11, 2, 16]
```

## Key Learning

A decorator is not magic.

It simply:

1. Takes a function
2. Creates a wrapper
3. Adds extra behavior
4. Calls the original function inside the wrapper
5. Returns the wrapper

## Final Note

This project connects Python decorators with backend and agentic AI systems.

Decorators are useful when building:

- API clients
- AI tools
- Agent workflows
- Retry systems
- Logging systems
- Authentication checks
- Caching layers
