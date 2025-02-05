import time
import asyncio
from fastapi import HTTPException
from collections import deque


class LeakyBucket:
    CAPACITY= 10
    RATE = 1.0
    def __init__(self, capacity: int = CAPACITY, leak_rate: float = RATE):
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.water = 0
        self.last_checked = time.time()
        self.queue = deque()

    async def leak(self):

        while True:
            current_time = time.time()
            elapsed_time = current_time - self.last_checked
            leak_amount = elapsed_time * self.leak_rate
            self.water = max(0, self.water - leak_amount)
            self.last_checked = current_time
            await asyncio.sleep(1)

    def add_request(self):
        if self.water < self.capacity:
            self.water += 1
            self.queue.append(time.time())
        else:
            raise HTTPException(status_code=429, detail="Too Many Requests: Bucket Overflow")

    def get_wait_time(self):
        if self.water < self.capacity:
            return 0
        return (self.water - self.capacity) / self.leak_rate


if __name__ == "__main__":
    asyncio.create_task(bucket.leak())
