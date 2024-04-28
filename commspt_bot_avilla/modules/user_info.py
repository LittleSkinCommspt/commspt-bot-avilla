from arclet.alconna import Alconna, Args, CommandMeta
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
from richuru import logger


@alcommand(
    Alconna(
        r"%user",
        Args["uid", int],
        meta=CommandMeta(
            description="查询用户信息 (commspt [group] only)",
            usage=r"%user <uid>",
            example=r"%user 123456",
            author="SerinaNya",
        ),
    )
)
@dispather_by_admin_only
@dispatcher_from([S_.defined_qq.commspt_group, S_.defined_qq.dev_group])
async def user_info(ctx: Context, uid: Match[int]):
    logger.info(f"Looking for user info uid={uid.result}")
    ltsk_user = await LittleSkinUser.uid_info(uid.result)
    if ltsk_user:
        logger.info(f"Ready to render {uid.result} ↓")
        logger.info(ltsk_user)
        render = RenderUserInfo(**ltsk_user.model_dump())
        image = await render.get_image()
        await ctx.scene.send_message(Picture(RawResource(image)))
        logger.success("Image sent.")
    else:
        await ctx.scene.send_message(f"未找到 UID 为 {uid.result} 的用户")
        logger.error(f"UID {uid.result} not found.")
