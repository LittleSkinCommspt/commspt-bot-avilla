# Author: @ChatGPT@ #
import re
from datetime import timedelta


def parse_timedelta(timedelta_str: str):
    # fallback: 适配旧习惯
    if timedelta_str.isdecimal():
        return timedelta(minutes=int(timedelta_str))

    pattern = r"(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?"
    match = re.match(pattern, timedelta_str)

    if not match:
        raise ValueError("Invalid timedelta format")

    days = int(match.group(1) or 0)
    hours = int(match.group(2) or 0)
    minutes = int(match.group(3) or 0)
    seconds = int(match.group(4) or 0)

    return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
