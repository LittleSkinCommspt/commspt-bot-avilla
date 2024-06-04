import asyncio
from random import SystemRandom


async def random_sleep(tmax: float = 1.0):
    # 使用由操作系统提供的随机源
    await asyncio.sleep(tmax * SystemRandom().random())
    return True
