from typing import Any
import httpx
from commspt_bot_avilla.utils.setting_manager import S_

FEISHU_OPENAPI_HEADER = {
    "Authorization": f"Bearer {S_.feishu_bitable.access_token}",
    "Content-Type": "application/json; charset=utf-8",
}

FEISHU_OPENAPI_BASE = "https://open.feishu.cn/open-apis/"
FEISHU_OPENAPI_BITABLE_BASE = f"{FEISHU_OPENAPI_BASE}bitable/v1/apps/"
FEISHU_OPENAPI_BITABLE = (
    f"{FEISHU_OPENAPI_BITABLE_BASE}{S_.feishu_bitable.app_token}/tables/{S_.feishu_bitable.table_id}"
)


async def records_search(field_names: list[str]):  # TODO
    pass
