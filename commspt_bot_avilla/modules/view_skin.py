from arclet.alconna import Alconna, Args
from avilla.core import Context, Message
from avilla.core import Picture, RawResource
from arclet.alconna.graia import alcommand, Match

from yggdrasil_mc.client import YggdrasilMC
from datetime import datetime

from commspt_bot_avilla.utils.adv_filter import dispatcher_from_preset_general
from commspt_bot_avilla.utils.skinrendermcapi import request_skinrendermc, process_image

from httpx import HTTPStatusError
from pytz import timezone

# region utils
LS_YGG = YggdrasilMC("https://littleskin.cn/api/yggdrasil")
MJ_YGG = YggdrasilMC()
TZ_SHANGHAI = timezone("Asia/Shanghai")
# endregion


@alcommand(Alconna("%view", Args["player_name", str]))
@alcommand(Alconna("%view.ls", Args["player_name", str]))
@dispatcher_from_preset_general
async def cmd_view_ygg(ctx: Context, message: Message, player_name: Match[str]):
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
        await ctx.scene.send_message(
            f"SkinRenderMC API Error, Code: {e.response.status_code}", reply=message
        )
        return

    skin_hash = player.skin.hash[:8] if player.skin and player.skin.hash else None
    skin_model = (
        player.skin.metadata.model if player.skin and player.skin.metadata else None
    )
    cape_hash = player.cape.hash[:8] if player.cape and player.cape.hash else None

    await ctx.scene.send_message(
        Picture(
            RawResource(
                process_image(
                    image,
                    f"Skin {skin_hash} ({skin_model}), Cape {cape_hash} / {datetime.now(TZ_SHANGHAI).isoformat()}, via SkinRenderMC, LittleSkin",
                )
            )
        )
    )


@alcommand(Alconna("%view.pro", Args["player_name", str]))
@dispatcher_from_preset_general
async def cmd_view_pro(ctx: Context, message: Message, player_name: Match[str]):
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
        await ctx.scene.send_message(
            f"SkinRenderMC API Error, Code: {e.response.status_code}", reply=message
        )
        return

    skin_hash = player.skin.hash[:8] if player.skin and player.skin.hash else None
    skin_model = (
        player.skin.metadata.model if player.skin and player.skin.metadata else None
    )
    cape_hash = player.cape.hash[:8] if player.cape and player.cape.hash else None

    await ctx.scene.send_message(
        Picture(
            RawResource(
                process_image(
                    image,
                    f"Skin {skin_hash} ({skin_model}), Cape {cape_hash} | {datetime.now(TZ_SHANGHAI).isoformat()}, via SkinRenderMC, Pro",
                )
            )
        )
    )
