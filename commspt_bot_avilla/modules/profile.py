from arclet.alconna import Alconna, Args, CommandMeta
from arclet.alconna.graia import Match, alcommand
from avilla.core import Context, Message
from httpx import HTTPStatusError
from yggdrasil_mc.client import YggdrasilMC

from commspt_bot_avilla.utils.adv_filter import dispatcher_from_preset_cafe
from commspt_bot_avilla.utils.random_sleep import random_sleep
from commspt_bot_avilla.utils.setting_manager import S_

# region utils
LS_YGG = YggdrasilMC("https://littleskin.cn/api/yggdrasil")
PRO_YGG = YggdrasilMC()
# endregion


# region %ygg
@alcommand(
    Alconna(
        f"{S_.command_prompt}ygg",
        Args["player_name", str],
        meta=CommandMeta(
            description="查询 Yggdrasil 玩家信息",
            usage=r"%ygg <player_name>",
            example=r"%ygg SerinaNya",
            author="SerinaNya",
        ),
    ),
)
@dispatcher_from_preset_cafe
async def cmd_ygg(ctx: Context, message: Message, player_name: Match[str]):
    try:
        player = await LS_YGG.by_name_async(player_name.result)
    except ValueError:
        _message = f"「{player_name.result}」不存在"
        await ctx.scene.send_message(_message, reply=message)
        return
    except HTTPStatusError as e:
        _message = f"请求错误: {e.response.status_code}"
        await ctx.scene.send_message(_message, reply=message)
        return
    # success
    skin_model = player.skin.metadata.model if player.skin and player.skin.metadata else None

    _message = f"""「{player.name}」的资料 - 来自 Yggdrasil API

» Skin ({skin_model}): {player.skin.hash if player.skin and player.skin.hash else None}

» Cape: {player.cape.hash if player.cape and player.cape.hash else None}

» UUID: {player.id}"""

    await random_sleep(2)
    await ctx.scene.send_message(_message, reply=message)


# endregion


# region %pro
@alcommand(
    Alconna(
        f"{S_.command_prompt}pro",
        Args["player_name", str],
        meta=CommandMeta(
            description="查询 Pro 玩家信息",
            usage=r"%ygg <player_name>",
            example=r"%ygg SerinaNya",
            author="SerinaNya",
        ),
    ),
)
@dispatcher_from_preset_cafe
async def cmd_pro(ctx: Context, message: Message, player_name: Match[str]):
    try:
        player = await PRO_YGG.by_name_async(player_name.result)
    except ValueError:
        _message = f"「{player_name.result}」不存在"
        await ctx.scene.send_message(_message, reply=message)
        return
    except HTTPStatusError as e:
        _message = f"请求错误: {e.response.status_code}"
        await ctx.scene.send_message(_message, reply=message)
        return
    # success
    skin_model = player.skin.metadata.model if player.skin and player.skin.metadata else None

    _message = f"""「{player.name}」的资料 - 来自 Pro

» Skin ({skin_model}): {player.skin.hash if player.skin and player.skin.hash else None}

» Cape: {player.cape.hash if player.cape and player.cape.hash else None}

» UUID: {player.id}"""

    await random_sleep(2)
    await ctx.scene.send_message(_message, reply=message)


# endregion
