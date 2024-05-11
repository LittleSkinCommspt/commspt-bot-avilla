from arclet.alconna import Alconna, Args, CommandMeta
from arclet.alconna.graia import Match, alcommand
from avilla.core import Context, Message
from avilla.core.elements import Picture
from avilla.core.resource import RawResource

from commspt_bot_avilla.models.littleskin_api import LittleSkinUser
from commspt_bot_avilla.models.render_user_info import RenderUserInfo
from commspt_bot_avilla.utils.adv_filter import (
    dispatcher_from_preset_commspt,
    dispather_by_admin_only,
)
from commspt_bot_avilla.utils.setting_manager import S_


# @alcommand(Alconna(r"%user", Args["uid", int]))
# @dispather_by_admin_only
# @dispatcher_from([S_.defined_qq.commspt_group, S_.defined_qq.dev_group])
# async def _(ctx: Context, uid: Match[int]):
#     ltsk_user = await LittleSkinUser.uid_info(uid.result)
#     render = RenderUserInfo(**ltsk_user.model_dump(), qq=None, qq_nickname="")
#     image = await render.get_image()
#     await ctx.scene.send_message(Picture(RawResource(image)))


@alcommand(
    Alconna(
        f"{S_.command_prompt}id",
        meta=CommandMeta(
            description="获取环境 ID (commspt [group] only)",
            usage=f"{S_.command_prompt}id",
            example=f"{S_.command_prompt}id",
            author="SerinaNya",
        ),
    )
)
@dispather_by_admin_only
@dispatcher_from_preset_commspt
async def _(ctx: Context, message: Message):
    if message.reply:
        origin_message = await ctx.pull(Message, message.reply)
    await ctx.scene.send_message(
        f"Channel ID: {ctx.scene.channel}\nMessage ID: {message.id}\nReply Message ID: {origin_message.id if message.reply else None}"
    )
