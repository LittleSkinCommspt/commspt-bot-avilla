from datetime import datetime
from typing import Annotated

import arrow
from pydantic import BaseModel, EmailStr, Field, IPvAnyAddress, computed_field
from pydantic.functional_serializers import PlainSerializer

from commspt_bot_avilla.models.bingling_ipip import BingLingIPIP
from commspt_bot_avilla.utils.browserless import screenshot

HumanReadableTime = Annotated[
    datetime,
    PlainSerializer(
        lambda t: arrow.get(t).to("Asia/Shanghai").format("YYYY-MM-DD HH:mm:ss")
    ),
    Field(default_factory=datetime.now),
]


class RenderUserInfo(BaseModel):
    generated_at: HumanReadableTime
    uid: int
    score: int
    nickname: str
    network: str = ""

    qq: int | None = None
    qq_nickname: str = ""

    register_at: HumanReadableTime
    last_sign_at: HumanReadableTime

    email: EmailStr
    verified: bool

    ip: list[IPvAnyAddress]

    @computed_field
    def email_help(self) -> str:
        v: list[str] = []
        v.append("已验证" if self.verified else "未验证")
        if self.email.lower() != self.email:
            v.append("⚠️ 含有大写字母 ⚠️ ")
        return " / ".join(v)

    async def get_image(self) -> bytes:
        # 获取 IP 属地信息
        ipip = await BingLingIPIP.get(self.ip[0])
        self.network = f"{ipip.country_name}{ipip.region_name}{ipip.city_name} {ipip.isp_domain}{ipip.owner_domain}"

        return await screenshot("user-info.html.jinja", self)
