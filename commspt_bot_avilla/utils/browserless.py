import json

import httpx
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel

from commspt_bot_avilla.utils.setting_manager import S_, VERIFY_CONTENT


async def screenshot(
    template_name: str,
    width: int = 530,
    height: int = 800,
    is_mobile: bool = True,
    device_scale_factor: float = 2.5,
    **params,
) -> bytes:
    # Jinja2 render
    jinja_env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
    template = jinja_env.get_template(name=template_name)
    html = template.render(params.model_dump()) if isinstance(params, BaseModel) else template.render(params)

    # send request to /screenshot
    async with httpx.AsyncClient(
        base_url=S_.api_browserless.endpoint,
        verify=VERIFY_CONTENT,
        http2=True,
    ) as client:
        resp = await client.post(
            "/screenshot",
            params={
                "launch": json.dumps(
                    {
                        "ignoreHTTPSErrors": True,
                        "headless": True,
                    },
                ),
            },
            json={
                "html": html,
                "options": {"type": "png"},
                "viewport": {
                    "width": width,
                    "height": height,
                    "isMobile": is_mobile,
                    "deviceScaleFactor": device_scale_factor,
                },
                "setExtraHTTPHeaders": {"Accept-Language": "zh-CN,en;q=0.9"},
                "gotoOptions": {"waitUntil": ["networkidle0"]},
            },
        )

        # raise exception if status is bad
        resp.raise_for_status()

        # return image from response
        return resp.content
