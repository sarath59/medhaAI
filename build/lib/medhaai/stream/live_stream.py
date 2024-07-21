import asyncio
from typing import AsyncGenerator, Any

class LiveStream:
    def __init__(self, speed: str = 'medium'):
        self.set_speed(speed)
        self.queue = asyncio.Queue()

    def set_speed(self, speed: str):
        self.speed = speed
        if speed == 'slow':
            self.delay = 2
        elif speed == 'medium':
            self.delay = 1
        elif speed == 'fast':
            self.delay = 0.5
        else:
            raise ValueError(f"Invalid speed: {speed}. Choose 'slow', 'medium', or 'fast'.")

    async def push(self, data: Any):
        await self.queue.put(data)

    async def get_stream(self) -> AsyncGenerator[Any, None]:
        while True:
            try:
                data = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                yield data
                await asyncio.sleep(self.delay)
            except asyncio.TimeoutError:
                continue