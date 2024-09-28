from arclet.alconna import Alconna, Args, CommandMeta
from arclet.alconna.graia import Match, alcommand
from avilla.core import Context, Message

from commspt_bot_avilla.models.const import get_csl_player, get_ygg_player
from commspt_bot_avilla.utils.adv_filter import dispatcher_from_preset_cafe
from commspt_bot_avilla.utils.setting_manager import S_


async def check_pro_exists(player_name: str) -> bool:
    return bool(await get_ygg_player(player_type="pro", player_name=player_name))


async def check_ltsk_ygg_exists(player_name: str) -> bool:
    return bool(await get_ygg_player(player_type="ltsk", player_name=player_name))


async def check_ltsk_csl_exists(player_name: str) -> bool:
    csl_player = await get_csl_player(player_name=player_name)
    return (bool(csl_player) and (csl_player.player_existed or False)) or False


async def check_ltsk_orogin_ygg_exists(player_name: str) -> bool:
    return bool(await get_ygg_player(player_type="ltsk", player_name=player_name, origin=True))


async def check_ltsk_origin_csl_exists(player_name: str) -> bool:
    csl_player = await get_csl_player(player_name=player_name, origin=True)
    return (bool(csl_player) and (csl_player.player_existed or False)) or False


async def get_ygg_skin_hash(player_name: str) -> tuple[str | None, str | None]:
    player = await get_ygg_player(player_type="ltsk", player_name=player_name)
    if not player:
        return None, None
    return player.skin.hash if player.skin else None, player.cape.hash if player.cape else None


async def get_csl_skin_hash(player_name: str) -> tuple[str | None, str | None]:
    player = await get_csl_player(player_name=player_name)
    if not player:
        return None, None
    return player.skin_hash, player.cape_hash


async def get_ygg_origin_skin_hash(player_name: str) -> tuple[str | None, str | None]:
    player = await get_ygg_player(player_type="ltsk", player_name=player_name)
    if not player:
        return None, None
    return player.skin.hash if player.skin else None, player.cape.hash if player.cape else None


async def get_csl_origin_skin_hash(player_name: str) -> tuple[str | None, str | None]:
    player = await get_csl_player(player_name=player_name)
    if not player:
        return None, None
    return player.skin_hash, player.cape_hash


def translate_bool(value: bool, yes_word: str = "", no_word: str = "不") -> str:
    return yes_word if value else no_word


@alcommand(
    Alconna(
        f"{S_.command_prompt}check",
        Args["player_name#角色名", str],
        meta=CommandMeta(
            description="Check player profile, such as existence and skin hash.",
            usage=f"{S_.command_prompt}check <player_name>",
            example=f"{S_.command_prompt}check jeb_",
        ),
    ),
)
@dispatcher_from_preset_cafe
async def check_profile(ctx: Context, message: Message, player_name: Match[str]):
    csl_exists = await check_ltsk_csl_exists(player_name=player_name.result)
    ygg_exists = await check_ltsk_ygg_exists(player_name=player_name.result)

    origin_csl_exists = await check_ltsk_origin_csl_exists(player_name=player_name.result)
    origin_ygg_exists = await check_ltsk_orogin_ygg_exists(player_name=player_name.result)

    if not csl_exists and not ygg_exists and not origin_csl_exists and not origin_ygg_exists:
        await ctx.scene.send_message("Player not found.", reply=message)
        return

    messages = [f"「{player_name.result}」的检查报告"]

    if not csl_exists or not ygg_exists:
        messages.append(
            f"> 此玩家在 Yggdrasil 缓存中{translate_bool(ygg_exists)}存在，在 CSL 缓存中却{translate_bool(csl_exists)}存在",
        )

    if not origin_csl_exists or not origin_ygg_exists:
        messages.append(
            f"> 此玩家在 Yggdrasil 非缓存中{translate_bool(origin_ygg_exists)}存在，在 CSL 非缓存中却{translate_bool(origin_csl_exists)}存在",
        )

    if origin_csl_exists and not csl_exists:
        messages.append("> 此玩家的 CSL 档案在缓存中不存在")
    if origin_ygg_exists and not ygg_exists:
        messages.append("> 此玩家的 Yggdrasil 档案在缓存中不存在")

    csl_skin_hash, csl_cape_hash = await get_csl_skin_hash(player_name=player_name.result)
    ygg_skin_hash, ygg_cape_hash = await get_ygg_skin_hash(player_name=player_name.result)

    origin_csl_skin_hash, origin_csl_cape_hash = await get_csl_origin_skin_hash(player_name=player_name.result)
    origin_ygg_skin_hash, origin_ygg_cape_hash = await get_ygg_origin_skin_hash(player_name=player_name.result)

    if csl_skin_hash != ygg_skin_hash:
        messages.append("> 此玩家的皮肤在缓存两端中并不一致")
    if csl_cape_hash != ygg_cape_hash:
        messages.append("> 此玩家的披风在缓存两端中并不一致")

    if origin_csl_skin_hash != origin_ygg_skin_hash:
        messages.append("> 此玩家的皮肤在非缓存两端中并不一致")
    if origin_csl_cape_hash != origin_ygg_cape_hash:
        messages.append("> 此玩家的披风在非缓存两端中并不一致")

    if origin_csl_skin_hash != csl_skin_hash:
        messages.append("> 此玩家的 CSL 皮肤在缓存中与实际不一致")
    if origin_csl_cape_hash != csl_cape_hash:
        messages.append("> 此玩家的 CSL 披风在缓存中与实际不一致")
    if origin_ygg_skin_hash != ygg_skin_hash:
        messages.append("> 此玩家的 Yggdrasil 皮肤在缓存中与实际不一致")
    if origin_ygg_cape_hash != ygg_cape_hash:
        messages.append("> 此玩家的 Yggdrasil 披风在缓存中与实际不一致")

    if await check_pro_exists(player_name=player_name.result):
        messages.append("> 存在以此角色名命名的正版玩家")

    if len(messages) == 1:
        messages.append("🎉 一切正常！")
    await ctx.scene.send_message("\n".join(messages), reply=message)
