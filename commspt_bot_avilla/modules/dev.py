from datetime import timedelta
from avilla.core.builtins.command import AvillaCommands
from avilla.core import Context, MessageChain, Text, Selector, Notice, Message, MuteCapability
from avilla.core.tools.filter import Filter

from arclet.alconna import Alconna, Args, Arparma

from commspt_bot_avilla.utils.setting_manager import S_
from commspt_bot_avilla.utils.adv_filter import by_admin_only

cmd = AvillaCommands(need_tome=False, remove_tome=True)


default_dispatchers = [
    Filter.cx.client.assert_true(by_admin_only()),
]


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

@cmd.on(Alconna(r"calltest", Args["arg1", str]["arg2", str]), dispatchers=default_dispatchers)
async def _(cx: Context, target: Notice, parma: Arparma):
    await cx.scene.send_message(f"Arg1: {parma["arg1"]}")
    if parma["arg2"]:
        await cx.scene.send_message(f"Arg2: right, {parma["arg2"]}")
    else:
        await cx.scene.send_message("Arg2: unknown")