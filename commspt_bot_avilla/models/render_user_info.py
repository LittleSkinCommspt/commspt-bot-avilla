import json
from datetime import datetime
from typing import Annotated

import arrow
import httpx
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, EmailStr, Field, IPvAnyAddress, computed_field
from pydantic.functional_serializers import PlainSerializer

from commspt_bot_avilla.models.bingling_ipip import BingLingIPIP
from commspt_bot_avilla.utils.setting_manager import S_, VERIFY_CONTENT

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

        # Jinja2 渲染 HTML
        jinja_env = Environment(loader=FileSystemLoader("templates"))
        template = jinja_env.get_template("user-info.html.jinja")
        html = template.render(self.model_dump())

        # 渲染截图
        async with httpx.AsyncClient(
            verify=VERIFY_CONTENT, base_url=S_.api_browserless.endpoint, http2=True
        ) as client:
            resp = await client.post(
                "/screenshot",
                params={
                    "launch": json.dumps(
                        {
                            "ignoreHTTPSErrors": True,
                            "headless": True,
                        }
                    )
                },
                json={
                    "html": html,
                    "options": {"type": "png"},
                    "viewport": {
                        "width": 530,
                        "height": 800,
                        "isMobile": True,
                        "deviceScaleFactor": 2.5,
                    },
                    "setExtraHTTPHeaders": {"Accept-Language": "zh-CN,en;q=0.9"},
                    "gotoOptions": {"waitUntil": ["networkidle0"]},
                },
            )
            resp.raise_for_status()

            # return image from response
            return resp.content
