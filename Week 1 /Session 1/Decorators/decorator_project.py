from functools import wraps
import time
import random


# =========================================================
# Decorator 1: Timer
# Purpose: Measure how long a function takes to run
# =========================================================
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        result = func(*args, **kwargs)

        end_time = time.time()
        total_time = end_time - start_time

        print(f"[TIMER] {func.__name__} took {total_time:.2f} seconds")

        return result

    return wrapper


# =========================================================
# Decorator 2: Logger
# Purpose: Show when a function starts and finishes
# =========================================================
def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling: {func.__name__}")
        print(f"[LOG] args={args}, kwargs={kwargs}")

        result = func(*args, **kwargs)

        print(f"[LOG] Finished: {func.__name__}")

        return result

    return wrapper


# =========================================================
# Decorator 3: Retry
# Purpose: Retry a function if it fails
# Example: @retry(3)
# =========================================================
def retry(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(1, times + 1):
                try:
                    print(f"[RETRY] Attempt {attempt}/{times}")
                    return func(*args, **kwargs)

                except Exception as error:
                    last_error = error
                    print(f"[RETRY] Failed: {error}")

            raise last_error

        return wrapper

    return decorator


# =========================================================
# Decorator 4: API Key Check
# Purpose: Stop function if API key is wrong
# =========================================================
def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = kwargs.get("api_key")

        if api_key != "secret123":
            raise PermissionError("Invalid or missing API key")

        return func(*args, **kwargs)

    return wrapper


# =========================================================
# Decorator 5: Cache
# Purpose: Save result so repeated calls become faster
# =========================================================
def cache_result(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)

        if key in cache:
            print(f"[CACHE] Returning cached result for {func.__name__}")
            return cache[key]

        result = func(*args, **kwargs)
        cache[key] = result

        print(f"[CACHE] Saving result for {func.__name__}")

        return result

    return wrapper


# =========================================================
# Simulated Backend / AI Functions
# =========================================================

@timer
@log_call
def analyze_text(text):
    """
    Simulates text analysis in an AI/backend system.
    """
    time.sleep(1)

    words = text.split()

    return {
        "text": text,
        "word_count": len(words),
        "character_count": len(text)
    }


@retry(3)
@timer
def fetch_user_data(user_id):
    """
    Simulates an API call that may fail sometimes.
    """
    time.sleep(1)

    if random.choice([True, False]):
        raise ConnectionError("Temporary API failure")

    return {
        "user_id": user_id,
        "name": "Ali",
        "role": "student"
    }


@require_api_key
def access_private_data(*, api_key):
    """
    Simulates protected/private data access.
    """
    return {
        "status": "success",
        "data": "This is protected data"
    }


@cache_result
@timer
def generate_embedding(text):
    """
    Simulates generating an embedding for text.
    In real AI systems, embeddings can be expensive to calculate.
    """
    time.sleep(2)

    fake_embedding = [
        len(text),
        len(text.split()),
        sum(ord(char) for char in text) % 100
    ]

    return fake_embedding


# =========================================================
# Main Program
# =========================================================
def main():
    print("\n--- Text Analysis Example ---")
    text_result = analyze_text("Python decorators are useful in backend and AI systems")
    print(text_result)

    print("\n--- Retry Example ---")
    try:
        user = fetch_user_data(101)
        print(user)
    except Exception as error:
        print("Final error after retries:", error)

    print("\n--- API Key Example ---")
    try:
        private_data = access_private_data(api_key="secret123")
        print(private_data)
    except PermissionError as error:
        print(error)

    print("\n--- Cache Example ---")
    embedding_1 = generate_embedding("hello world")
    print(embedding_1)

    embedding_2 = generate_embedding("hello world")
    print(embedding_2)


if __name__ == "__main__":
    main()