import time
from functools import wraps

import asyncio

def retry_async(max_retries: int, delay: float):
    """Retries async methods """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    print(f"Attempt {attempt} failed with error: {e}")
                    if attempt >= max_retries:
                        raise
                    print(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
        return wrapper
    return decorator
