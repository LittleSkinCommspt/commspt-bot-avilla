from datetime import timedelta
from typing import Literal

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
        Args["target", int | Notice]["duration", int, 10][
            "group?", str, Literal["main", "cafe", None]
        ],
        meta=CommandMeta(
            description="禁言用户 (commspt only)",
            usage=r"%mute <target / qq> [duration] [group]",
            example=r"%mute @user 10 main",
            author="SerinaNya & FalfaChino",
        ),
    )
)
@dispatcher_from_preset_general
@dispather_by_admin_only
async def mute(
    ctx: Context,
    target: Match[int | Notice],
    duration: int,
    group: Match[Literal["main", "cafe", None]],
):
    if (
        ctx.scene.channel
        in [S_.defined_qq.littleskin_main, S_.defined_qq.littleskin_cafe]
        and not group
    ):
        await ctx[MuteCapability.mute](
            target=(
                target.result.target
                if isinstance(target.result, Notice)
                else ctx.scene.into(f"~.member({target.result})")
            ),
            # duration 的单位为分钟，默认 10 分钟
            duration=timedelta(minutes=duration),
        )
    elif group:
        match group.result:
            case "main":
                await ctx[MuteCapability.mute](
                    target=(
                        target.result.target
                        if isinstance(target.result, Notice)
                        else ctx.scene.into(
                            f"::group({S_.defined_qq.littleskin_main})"
                        ).into(f"~.member({target.result})")
                    ),
                    duration=timedelta(minutes=duration),
                )
                return
            case "cafe":
                await ctx[MuteCapability.mute](
                    target=(
                        target.result.target
                        if isinstance(target.result, Notice)
                        else ctx.scene.into(
                            f"::group({S_.defined_qq.littleskin_cafe})"
                        ).into(f"~.member({target.result})")
                    ),
                    duration=timedelta(minutes=duration),
                )
                return
    await ctx.scene.send_message("需要指定群组 main 或 cafe")


# MARK: %unmute
@alcommand(
    Alconna(
        r"%unmute",
        Args["target", int | Notice]["group?", str, Literal["main", "cafe", None]],
        meta=CommandMeta(
            description="解除禁言 (commspt only)",
            usage=r"%unmute <target / qq> [group]",
            example=r"%unmute @user main",
            author="SerinaNya & FalfaChino",
        ),
    )
)
@dispatcher_from_preset_general
@dispather_by_admin_only
async def unmute(
    ctx: Context,
    target: Match[int | Notice],
    group: Match[Literal["main", "cafe", None]],
):
    if (
        ctx.scene.channel
        in [S_.defined_qq.littleskin_main, S_.defined_qq.littleskin_cafe]
        and not group
    ):
        await ctx[MuteCapability.unmute](
            target=(
                target.result.target
                if isinstance(target.result, Notice)
                else ctx.scene.into(f"~.member({target.result})")
            )
        )
        return
    elif group:
        match group.result:
            case "main":
                await ctx[MuteCapability.unmute](
                    target=(
                        target.result.target
                        if isinstance(target.result, Notice)
                        else ctx.scene.into(
                            f"::group({S_.defined_qq.littleskin_main})"
                        ).into(f"~.member({target.result})")
                    )
                )
                return
            case "cafe":
                await ctx[MuteCapability.unmute](
                    target=(
                        target.result.target
                        if isinstance(target.result, Notice)
                        else ctx.scene.into(
                            f"::group({S_.defined_qq.littleskin_cafe})"
                        ).into(f"~.member({target.result})")
                    )
                )
                return
    await ctx.scene.send_message("需要指定群组 main 或 cafe")
