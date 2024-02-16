import asyncio
from random import SystemRandom


async def random_sleep(max: float = 1.0):
    await asyncio.sleep(max * SystemRandom().random())
    return True
