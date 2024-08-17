from typing import Literal

from pytz import timezone
from yggdrasil_mc.client import YggdrasilMC
from yggdrasil_mc.models import PlayerProfile

from .csl_api import CustomSkinLoaderApi

LTSK_YGG_ENDPOINT = "https://littleskin.cn/api/yggdrasil"
LTSK_CSL_ENDPOINT = "https://littleskin.cn/csl"

LTSK_YGG = YggdrasilMC(api_root=LTSK_YGG_ENDPOINT)
PRO_YGG = YggdrasilMC()
TZ_SHANGHAI = timezone("Asia/Shanghai")
LTSK_CSL = CustomSkinLoaderApi


async def get_csl_player(player_name: str) -> CustomSkinLoaderApi | None:
    return await LTSK_CSL.get(api_root=LTSK_CSL_ENDPOINT, username=player_name)


async def get_ygg_player(player_type: Literal["pro", "ltsk"], player_name: str) -> PlayerProfile | None:
    if player_type == "pro":
        try:
            return await PRO_YGG.by_name_async(player_name)
        except Exception:
            return None
    try:
        return await LTSK_YGG.by_name_async(player_name)
    except Exception:
        return None
