from datetime import timedelta
from avilla.core.builtins.command import AvillaCommands
from avilla.core import Context, MessageChain, Text, Selector, Notice, Message, MuteCapability
from avilla.core.tools.filter import Filter

from commspt_bot_avilla.utils.setting_manager import S_

cmd = AvillaCommands(need_tome=False, remove_tome=True)


@cmd.on(
    "c1 {target} {duration:int}",
    dispatchers=[
        Filter.cx.scene.follows("::group.member(742905606)")
    ],
)
async def c1(cx: Context,target: Notice, duration: int):
    # await cx.scene.into(f"::group({S_.defined_qq.commspt_group})").send_message(
    #     msg
    # )
    # await cx[MuteCapability.mute](
    #     target.target, timedelta(minutes=duration)
    # )
    ...

