import asyncio
from random import SystemRandom


async def random_sleep(max: float = 1.0):
    # 使用由操作系统提供的随机源
    await asyncio.sleep(max * SystemRandom().random())
    return True
