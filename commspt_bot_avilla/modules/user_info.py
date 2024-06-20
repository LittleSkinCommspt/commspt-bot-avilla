from arclet.alconna import Alconna, Args, CommandMeta
from arclet.alconna.graia import Match, alcommand
from avilla.core import Context
from avilla.core.elements import Notice, Picture
from avilla.core.resource import RawResource
from richuru import logger

from commspt_bot_avilla.models.littleskin_api import LittleSkinUser
from commspt_bot_avilla.models.mongodb_data import UIDMapping
from commspt_bot_avilla.models.render_user_info import RenderUserInfo
from commspt_bot_avilla.utils.adv_filter import (
    dispatcher_from_preset_cafe,
    dispatcher_from_preset_commspt,
    dispather_by_admin_only,
)
from commspt_bot_avilla.utils.mongodb_manager import write_uid_db
from commspt_bot_avilla.utils.setting_manager import S_


@alcommand(
    Alconna(
        f"{S_.command_prompt}user",
        Args["uid", int],
        meta=CommandMeta(
            description="查询用户信息 (commspt [group] only)",
            usage=f"{S_.command_prompt}user <uid>",
            example=f"{S_.command_prompt}user 123456",
            author="SerinaNya",
        ),
    ),
)
@dispather_by_admin_only
@dispatcher_from_preset_commspt
async def user_info(ctx: Context, uid: Match[int]):
    logger.info(f"Looking for user info uid={uid.result}")
    ltsk_user = await LittleSkinUser.uid_info(uid.result)
    mapping_qq = await UIDMapping.fetch(uid=uid.result)
    logger.info(f"UID Mapping: {uid.result} -> {mapping_qq}")
    if ltsk_user:
        logger.info(f"Ready to render {uid.result} ↓")
        logger.info(ltsk_user)
        render = RenderUserInfo(**ltsk_user.model_dump(), qq=mapping_qq.qq if mapping_qq else None)
        image = await render.get_image()
        await ctx.scene.send_message(Picture(RawResource(image)))
        logger.success("Image sent.")
    else:
        await ctx.scene.send_message(f"未找到 UID 为 {uid.result} 的用户")
        logger.error(f"UID {uid.result} not found.")


@alcommand(
    Alconna(
        f"{S_.command_prompt}setuid",
        Args["target", Notice | int]["uid", int],
        meta=CommandMeta(
            description="设置用户记录的 UID (commspt only)",
            usage=f"{S_.command_prompt}setuid <target> <uid>",
            example=f"{S_.command_prompt}setuid @SerinaNya 15301",
            author="SerinaNya",
        ),
    ),
)
@dispather_by_admin_only
@dispatcher_from_preset_cafe
async def _(ctx: Context, target: Match[Notice | int], uid: Match[int]):
    target_qq = int(target.result.target["member"]) if isinstance(target.result, Notice) else target.result
    target_uid = uid.result
    await write_uid_db(uid=target_uid, qq=target_qq)
    await ctx.scene.send_message(f"RESULT ✅ > QQ {target_qq} <-> UID {target_uid}")
