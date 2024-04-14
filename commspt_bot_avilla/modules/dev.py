from arclet.alconna import Alconna, Args
from arclet.alconna.graia import Match, alcommand
from avilla.core import Context

from commspt_bot_avilla.utils.adv_filter import (
    dispatcher_from_preset_general,
    dispather_by_admin_only,
)
from commspt_bot_avilla.utils.setting_manager import S_


@alcommand(Alconna(r"calltest", Args["arg1", str]))
@dispather_by_admin_only
@dispatcher_from_preset_general
async def _(cx: Context, arg1: Match[str]):
    await cx.scene.send_message(f"{arg1=}")
