from arclet.alconna import Alconna, Args
from arclet.alconna.graia import Match, alcommand
from avilla.core import Context
from avilla.core.elements import Picture
from avilla.core.resource import RawResource

from commspt_bot_avilla.models.littleskin_api import LittleSkinUser
from commspt_bot_avilla.models.render_user_info import RenderUserInfo
from commspt_bot_avilla.utils.adv_filter import (
    dispatcher_from,
    dispather_by_admin_only,
)
from commspt_bot_avilla.utils.setting_manager import S_


@alcommand(Alconna(r"%user", Args["uid", int]))
@dispather_by_admin_only
@dispatcher_from([S_.defined_qq.commspt_group, S_.defined_qq.dev_group])
async def _(ctx: Context, uid: Match[int]):
    ltsk_user = await LittleSkinUser.uid_info(uid.result)
    render = RenderUserInfo(**ltsk_user.model_dump())
    image = await render.get_image()
    await ctx.scene.send_message(Picture(RawResource(image)))
