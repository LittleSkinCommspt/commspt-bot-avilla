from datetime import timedelta
from typing import Literal

from arclet.alconna import Alconna, Args, CommandMeta
from arclet.alconna.graia import Match, alcommand
from avilla.core import Context, Message, MuteAllCapability, MuteCapability, Notice

from commspt_bot_avilla.utils.adv_filter import (
    dispatcher_from_preset_cafe,
    dispather_by_admin_only,
)
from commspt_bot_avilla.utils.setting_manager import S_

_GROUP_NAME_MAPPING = {
    "main": S_.defined_qq.littleskin_main,
    "cafe": S_.defined_qq.littleskin_cafe,
}


# MARK: %mute
@alcommand(
    Alconna(
        f"{S_.command_prompt}mute",
        Args["target#目标", int | Notice]["duration#时长", int, 10]["group#群组", Literal["main", "cafe"] | None, None],
        meta=CommandMeta(
            description="禁言用户 (commspt only)",
            usage=f"{S_.command_prompt}mute <target> [duration] [group]",
            example=f"{S_.command_prompt}mute @user 10 main",
        ),
    ),
)
@dispatcher_from_preset_cafe
@dispather_by_admin_only
async def mute(
    ctx: Context,
    target: Match[int | Notice],
    duration: int,
    group: Match[Literal["main", "cafe"] | None],
):
    if group.result:
        if isinstance(target.result, Notice):
            await ctx.scene.send_message("指定群组时不允许使用 @user")
            return

        await ctx[MuteCapability.mute](
            target=(ctx.scene.into(f"::group({_GROUP_NAME_MAPPING[group.result]})").into(f"~.member({target.result})")),
            duration=timedelta(minutes=duration),
        )
        return

    await ctx[MuteCapability.mute](
        target=(
            target.result.target if isinstance(target.result, Notice) else ctx.scene.into(f"~.member({target.result})")
        ),
        duration=timedelta(minutes=duration),
    )
    return


# MARK: %unmute
@alcommand(
    Alconna(
        f"{S_.command_prompt}unmute",
        Args["target#目标", int | Notice]["group#群组", Literal["main", "cafe"] | None, None],
        meta=CommandMeta(
            description="解除禁言 (commspt only)",
            usage=f"{S_.command_prompt}unmute <target / qq> [group]",
            example=f"{S_.command_prompt}unmute @user main",
        ),
    ),
)
@dispatcher_from_preset_cafe
@dispather_by_admin_only
async def unmute(
    ctx: Context,
    target: Match[int | Notice],
    group: Match[Literal["main", "cafe"] | None],
):
    if group.result:
        if isinstance(target.result, Notice):
            await ctx.scene.send_message("指定群组时不允许使用 @user")
            return

        await ctx[MuteCapability.unmute](
            target=(ctx.scene.into(f"::group({_GROUP_NAME_MAPPING[group.result]})").into(f"~.member({target.result})")),
        )
        return

    await ctx[MuteCapability.unmute](
        target=(
            target.result.target if isinstance(target.result, Notice) else ctx.scene.into(f"~.member({target.result})")
        ),
    )
    return


# MARK: %recall
@alcommand(
    Alconna(
        f"{S_.command_prompt}recall",
        meta=CommandMeta(
            description="撤回消息 (commspt only)",
            usage=r"%recall",
            example=r"%recall",
        ),
    ),
)
@dispatcher_from_preset_cafe
@dispather_by_admin_only
async def recall(ctx: Context, message: Message):
    if message.reply:
        origin_message = await ctx.pull(Message, message.reply)
    else:
        await ctx.scene.send_message("需要回复消息")
        return
    await origin_message.revoke()
    await message.revoke()


@alcommand(
    Alconna(
        f"{S_.command_prompt}muteall",
        Args["group#群组", Literal["main", "cafe"]],
        meta=CommandMeta(
            description="MUTEALL (commspt only)",
            usage=f"{S_.command_prompt}muteall <group>",
            example=f"{S_.command_prompt}muteall main",
        ),
    ),
)
@dispatcher_from_preset_cafe
@dispather_by_admin_only
async def mute_all(ctx: Context, group: Match[Literal["main", "cafe"]]):
    await ctx[MuteAllCapability.mute_all](
        target=ctx.scene if not group.result else ctx.scene.into(f"::group({_GROUP_NAME_MAPPING[group.result]})"),
    )
    return


@alcommand(
    Alconna(
        f"{S_.command_prompt}unmuteall",
        Args["group#群组", Literal["main", "cafe"]],
        meta=CommandMeta(
            description="UNMUTEALL (commspt only)",
            usage=f"{S_.command_prompt}unmuteall <group>",
            example=f"{S_.command_prompt}unmuteall main",
        ),
    ),
)
@dispatcher_from_preset_cafe
@dispather_by_admin_only
async def unmute_all(ctx: Context, group: Match[Literal["main", "cafe"]]):
    await ctx[MuteAllCapability.unmute_all](
        target=ctx.scene if not group.result else ctx.scene.into(f"::group({_GROUP_NAME_MAPPING[group.result]})"),
    )
    return
