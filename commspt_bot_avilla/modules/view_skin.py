from arclet.alconna import Alconna, Args, CommandMeta
from avilla.core import Context, Message
from avilla.core import Picture, RawResource
from arclet.alconna.graia import alcommand, Match

from yggdrasil_mc.client import YggdrasilMC
from datetime import datetime
from time import time

from commspt_bot_avilla.utils.adv_filter import dispatcher_from_preset_cafe
from commspt_bot_avilla.utils.skinrendermcapi import request_skinrendermc, process_image
from commspt_bot_avilla.utils.setting_manager import S_

from httpx import HTTPStatusError
from pytz import timezone

# region utils
LS_YGG = YggdrasilMC("https://littleskin.cn/api/yggdrasil")
MJ_YGG = YggdrasilMC()
TZ_SHANGHAI = timezone("Asia/Shanghai")
# endregion


@alcommand(
    Alconna(
        f"{S_.command_prompt}view",
        Args["player_name", str],
        meta=CommandMeta(
            description="查看玩家皮肤",
            usage=f"{S_.command_prompt}view <player_name>",
            example=f"{S_.command_prompt}view SerinaNya",
            author="SerinaNya",
        ),
    )
)
@alcommand(
    Alconna(
        f"{S_.command_prompt}view.ygg",
        Args["player_name", str],
        meta=CommandMeta(
            description="查看玩家皮肤 (LittleSkin)",
            usage=f"{S_.command_prompt}view.ygg <player_name>",
            example=f"{S_.command_prompt}view.ygg SerinaNya",
            author="SerinaNya",
        ),
    )
)
@dispatcher_from_preset_cafe
async def cmd_view_ygg(ctx: Context, message: Message, player_name: Match[str]):
    start_time = time()
    try:
        player = await LS_YGG.by_name_async(player_name.result)
    except ValueError:
        _message = f"「{player_name.result}」不存在"
        await ctx.scene.send_message(_message, reply=message)
        return

    skin_url = player.skin.url if player.skin else None
    cape_url = player.cape.url if player.cape else None
    name_tag = player.name

    try:
        image = await request_skinrendermc(
            skin_url=str(skin_url) if skin_url else None,
            cape_url=str(cape_url) if cape_url else None,
            name_tag=name_tag,
        )
    except HTTPStatusError as e:
        await ctx.scene.send_message(f"SkinRenderMC API Error, Code: {e.response.status_code}", reply=message)
        return

    skin_hash = player.skin.hash[:8] if player.skin and player.skin.hash else None
    skin_model = player.skin.metadata.model if player.skin and player.skin.metadata else None
    cape_hash = player.cape.hash[:8] if player.cape and player.cape.hash else None

    end_time = time()
    const_time = end_time - start_time

    await ctx.scene.send_message(
        Picture(
            RawResource(
                process_image(
                    image,
                    f"({const_time:.3f}s) Skin {skin_hash} ({skin_model}), Cape {cape_hash} / {datetime.now(TZ_SHANGHAI).isoformat()}, via SkinRenderMC, LittleSkin",
                )
            )
        )
    )


@alcommand(
    Alconna(
        "%view.pro",
        Args["player_name", str],
        meta=CommandMeta(
            description="查看玩家皮肤 (Pro)",
            usage=r"%view.pro <player_name>",
            example=r"%view.pro SerinaNya",
            author="SerinaNya",
        ),
    )
)
@dispatcher_from_preset_cafe
async def cmd_view_pro(ctx: Context, message: Message, player_name: Match[str]):
    start_time = time()
    try:
        player = await MJ_YGG.by_name_async(player_name.result)
    except ValueError:
        _message = f"「{player_name.result}」不存在"
        await ctx.scene.send_message(_message, reply=message)
        return

    skin_url = player.skin.url if player.skin else None
    cape_url = player.cape.url if player.cape else None
    name_tag = player.name

    try:
        image = await request_skinrendermc(
            skin_url=str(skin_url) if skin_url else None,
            cape_url=str(cape_url) if cape_url else None,
            name_tag=name_tag,
        )
    except HTTPStatusError as e:
        await ctx.scene.send_message(f"SkinRenderMC API Error, Code: {e.response.status_code}", reply=message)
        return

    skin_hash = player.skin.hash[:8] if player.skin and player.skin.hash else None
    skin_model = player.skin.metadata.model if player.skin and player.skin.metadata else None
    cape_hash = player.cape.hash[:8] if player.cape and player.cape.hash else None

    end_time = time()
    const_time = end_time - start_time

    await ctx.scene.send_message(
        Picture(
            RawResource(
                process_image(
                    image,
                    f"({const_time:.3f}s) Skin {skin_hash} ({skin_model}), Cape {cape_hash} / {datetime.now(TZ_SHANGHAI).isoformat()}, via SkinRenderMC, Pro",
                )
            )
        )
    )
