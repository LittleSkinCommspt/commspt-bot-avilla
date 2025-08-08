from datetime import datetime
from typing import Annotated, Self

import httpx
from pydantic import BaseModel, Field

from commspt_bot_avilla.utils.setting_manager import S_


class CloudConfig(BaseModel):
    enable_auto_accept_join_request_main: bool = False
    enable_temporary_welcome_message_main: bool = False
    temporary_welcome_message_main: str = ""

    timestamp: Annotated[
        float,
        Field(
            default_factory=lambda: datetime.now().astimezone().timestamp(),
        ),
    ]

    @classmethod
    async def fetch(cls) -> Self:
        async with httpx.AsyncClient(http2=True, base_url=S_.api_cloudconfig.endpoint, follow_redirects=True) as client:
            resp = await client.get("/bot/")
            return cls(**resp.json())
