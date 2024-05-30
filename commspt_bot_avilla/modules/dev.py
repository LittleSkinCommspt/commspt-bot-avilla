from arclet.alconna import Alconna, CommandMeta
from arclet.alconna.graia import alcommand
from avilla.core import Context, Message
from commspt_bot_avilla.utils.adv_filter import (
    dispatcher_from_preset_commspt,
    dispather_by_admin_only,
)
from commspt_bot_avilla.utils.setting_manager import S_


@alcommand(
    Alconna(
        f"{S_.command_prompt}id",
        meta=CommandMeta(
            description="获取环境 ID (commspt only)",
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
        f"""Channel ID: {ctx.scene.channel}
Message ID: {message.id}
Message Content: {message.content}
Reply Message ID: {origin_message.id if message.reply else None}
Reply Message Content: {origin_message.content if message.reply else None}"""
    )
