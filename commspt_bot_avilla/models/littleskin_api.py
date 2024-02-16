from datetime import datetime

import httpx
from pydantic import BaseModel, EmailStr, IPvAnyAddress, field_validator
from commspt_bot_avilla.utils.setting_manager import S_


class LittleSkinUser(BaseModel):
    uid: int
    nickname: str
    email: EmailStr
    locale: str | None = None
    score: int
    avatar: int = 0
    ip: list[IPvAnyAddress]
    is_dark_mode: bool = False
    permisson: int = 0
    last_sign_at: datetime
    register_at: datetime
    verified: bool
    verification_token: str = ""
    salt: str = ""

    @field_validator('ip', mode='before')
    def validate_ip(cls, v: str):
        return v.split(', ')

    @classmethod
    async def query(cls, query_string: str):
        async with httpx.AsyncClient(
            http2=True, headers={"Authorization": f"Bearer {S_.littleskin_admin_token}"}
        ) as client:
            api = await client.get(
                "https://littleskin.cn/api/admin/users", params={"q": query_string}
            )
            if data := api.json()["data"]:
                return cls(**data[0])

    @classmethod
    async def qmail_api(cls, qq: int):
        if data := await cls.query(f"email:'{qq}@qq.com'"):
            return data
