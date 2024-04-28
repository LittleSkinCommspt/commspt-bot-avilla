from datetime import timedelta

from arclet.alconna import Alconna, Args, CommandMeta
from arclet.alconna.graia import Match, alcommand
from avilla.core import Context, MuteCapability, Notice

from commspt_bot_avilla.utils.adv_filter import (
    dispatcher_from_preset_general,
    dispather_by_admin_only,
)
from commspt_bot_avilla.utils.setting_manager import S_


# MARK: %mute
@alcommand(
    Alconna(
        r"%mute",
        Args["target", int | Notice]["duration", int, 10],
        meta=CommandMeta(
            description="禁言用户 (commspt only)",
            usage=r"%mute <target / qq> [duration]",
            example=r"%mute @user 10",
            author="SerinaNya",
        ),
    )
)
@dispatcher_from_preset_general
@dispather_by_admin_only
async def mute(ctx: Context, target: Match[int | Notice], duration: int):
    await ctx[MuteCapability.mute](
        target=(
            target.result.target
            if isinstance(target.result, Notice)
            else ctx.scene.into(f"::group({S_.defined_qq.littleskin_main})").into(
                f"~.member({target.result})"
            )
        ),
        # duration 的单位为分钟，默认 10 分钟
        duration=timedelta(minutes=duration),
    )


# MARK: %unmute
@alcommand(
    Alconna(
        r"%unmute",
        Args["target", int | Notice],
        meta=CommandMeta(
            description="解除禁言 (commspt only)",
            usage=r"%unmute <target / qq>",
            example=r"%unmute @user",
            author="SerinaNya",
        ),
    )
)
@dispatcher_from_preset_general
@dispather_by_admin_only
async def unmute(ctx: Context, target: Match[int | Notice]):
    await ctx[MuteCapability.unmute](
        target=(
            target.result.target
            if isinstance(target.result, Notice)
            else ctx.scene.into(f"::group({S_.defined_qq.littleskin_main})").into(
                f"~.member({target.result})"
            )
        )
    )
