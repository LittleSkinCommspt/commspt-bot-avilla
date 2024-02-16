from avilla.core.builtins.command import AvillaCommands
from avilla.core import Context, MessageChain, Text, Selector, Notice, Message
from avilla.core.tools.filter import Filter

from commspt_bot_avilla.utils.setting_manager import S_

cmd = AvillaCommands(need_tome=False, remove_tome=True)


@cmd.on(
    "c1 {msg:str}",
    dispatchers=[
        Filter.cx.scene.follows("::group.member(742905606)")
    ],
)
async def ping2(cx: Context, msg: str):
    await cx.scene.into(f"::group({S_.defined_qq.commspt_group})").send_message(
        msg
    )

