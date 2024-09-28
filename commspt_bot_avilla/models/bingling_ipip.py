import httpx
from pydantic import BaseModel

from commspt_bot_avilla.utils.setting_manager import S_, VERIFY_CONTENT


class BingLingIPIP(BaseModel):
    country_name: str | None = None
    region_name: str | None = None
    city_name: str | None = None
    owner_domain: str | None = None
    isp_domain: str | None = None
    latitude: str | None = None
    longitude: str | None = None
    china_region_code: str | None = None
    china_district_code: str | None = None
    country_code: str | None = None
    continent_code: str | None = None

    @classmethod
    async def get(cls, ip: str):
        """
        获取 IP 信息
        ```json
        {
            "country_name": "中国",
            "region_name": "湖北",
            "city_name": "武汉",
            "owner_domain": "",
            "isp_domain": "移动",
            "latitude": "30.572399",
            "longitude": "114.279121",
            "china_region_code": null,
            "china_district_code": null,
            "country_code": "CN",
            "continent_code": "AP"
        }
        ```
        """
        async with httpx.AsyncClient(
            verify=VERIFY_CONTENT, base_url=S_.api_bingling_ipip.endpoint, http2=True,
        ) as client:
            resp = await client.get(f"/{ip}")
        return cls(**resp.json())
