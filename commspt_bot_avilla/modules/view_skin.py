from datetime import datetime
from time import time

from arclet.alconna import Alconna, Args, CommandMeta
from arclet.alconna.graia import Match, alcommand
from avilla.core import Context, Message, Picture, RawResource
from httpx import HTTPStatusError

from commspt_bot_avilla.models.const import TZ_SHANGHAI, PlayerNotFoundError, get_ygg_player
from commspt_bot_avilla.utils.adv_filter import dispatcher_from_preset_cafe
from commspt_bot_avilla.utils.setting_manager import S_
from commspt_bot_avilla.utils.skinrendermcapi import process_image, request_skinrendermc


@alcommand(
    Alconna(
        f"{S_.command_prompt}view",
        Args["player_name#角色名", str],
        meta=CommandMeta(
            description="查看玩家皮肤",
            usage=f"{S_.command_prompt}view <player_name>",
            example=f"{S_.command_prompt}view SerinaNya",
        ),
    )
)
@alcommand(
    Alconna(
        f"{S_.command_prompt}view.ygg",
        Args["player_name#角色名", str],
        meta=CommandMeta(
            description="查看玩家皮肤 (LittleSkin)",
            usage=f"{S_.command_prompt}view.ygg <player_name>",
            example=f"{S_.command_prompt}view.ygg SerinaNya",
        ),
    )
)
@dispatcher_from_preset_cafe
async def cmd_view_ygg(ctx: Context, message: Message, player_name: Match[str]):
    start_time = time()
    try:
        player = await get_ygg_player(player_type="ltsk", player_name=player_name.result)
    except PlayerNotFoundError:
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
    cost_time = end_time - start_time

    now_time = datetime.now(TZ_SHANGHAI).isoformat()

    await ctx.scene.send_message(
        Picture(
            RawResource(
                process_image(
                    image,
                    f"{cost_time:.3f}s / Skin {skin_hash} ({skin_model}), Cape {cape_hash} / {now_time}, via SkinRenderMC, LittleSkin",  # noqa: E501
                )
            )
        )
    )


@alcommand(
    Alconna(
        "%view.pro",
        Args["player_name#角色名", str],
        meta=CommandMeta(
            description="查看玩家皮肤 (Pro)",
            usage=r"%view.pro <player_name>",
            example=r"%view.pro SerinaNya",
        ),
    )
)
@dispatcher_from_preset_cafe
async def cmd_view_pro(ctx: Context, message: Message, player_name: Match[str]):
    start_time = time()
    try:
        player = await get_ygg_player(player_type="pro", player_name=player_name.result)
    except PlayerNotFoundError:
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
    cost_time = end_time - start_time

    now_time = datetime.now(TZ_SHANGHAI).isoformat()

    await ctx.scene.send_message(
        Picture(
            RawResource(
                process_image(
                    image,
                    f"{cost_time:.3f}s / Skin {skin_hash} ({skin_model}), Cape {cape_hash} / {now_time}, via SkinRenderMC, Pro",  # noqa: E501
                )
            )
        )
    )
