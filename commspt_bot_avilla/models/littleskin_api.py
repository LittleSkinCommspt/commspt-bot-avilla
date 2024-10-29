from datetime import datetime
from typing import Annotated

import arrow
import httpx
from pydantic import (
    AfterValidator,
    BaseModel,
    EmailStr,
    IPvAnyAddress,
    field_validator,
)

from commspt_bot_avilla.utils.setting_manager import S_

StdTime = Annotated[
    datetime,
    AfterValidator(lambda v: arrow.get(v).replace(tzinfo="Asia/Shanghai").datetime),
]


class LittleSkinUser(BaseModel):
    uid: int
    nickname: str
    email: EmailStr
    locale: str | None = None
    score: int
    avatar: int = 0
    ip: list[IPvAnyAddress]
    is_dark_mode: bool = False

    permission: int = 0
    # Banned = -1,
    # Normal = 0,
    # Admin = 1,
    # SuperAdmin = 2,

    last_sign_at: datetime
    register_at: datetime
    verified: bool
    verification_token: str = ""
    salt: str = ""

    @field_validator("ip", mode="before")
    def validate_ip(cls, v: str):
        return v.split(", ")

    @classmethod
    async def query(cls, query_string: str):
        async with httpx.AsyncClient(
            http2=True, headers={"Authorization": f"Bearer {S_.littleskin_admin_token}"},
        ) as client:
            api = await client.get("https://littleskin.cn/api/admin/users", params={"q": query_string})
            if data := api.json()["data"]:
                return cls(**data[0])
            return None

    @classmethod
    async def qmail_api(cls, qq: int | str):
        return await cls.query(f"email:'{qq}@qq.com'")

    @classmethod
    async def uid_info(cls, uid: int | str):
        return await cls.query(f"uid:{uid}")
