from arclet.alconna import Alconna, CommandMeta
from arclet.alconna.graia import alcommand
from avilla.core import Context, Message, Picture

from commspt_bot_avilla.utils.adv_filter import dispatcher_from_preset_commspt, dispather_by_admin_only
from commspt_bot_avilla.utils.setting_manager import S_


@alcommand(
    Alconna(
        f"{S_.command_prompt}ot",
        meta=CommandMeta(
            description=f"{S_.command_prompt}ot",
            usage=f"{S_.command_prompt}ot",
            example=f"{S_.command_prompt}ot",
            author="SerinaNya",
        ),
    )
)
@dispatcher_from_preset_commspt
@dispather_by_admin_only
async def _(ctx: Context, message: Message):
    _ = await ctx.scene.into(f"::group({S_.defined_qq.littleskin_main})").send_message(
        [
            Picture("assets/images/honoka cafe ng.png"),
            """本群不允许闲聊，闲聊请加群 👉 651672723
大水怪将会收到我们赠送的禁言大礼包。""",
        ]
    )
