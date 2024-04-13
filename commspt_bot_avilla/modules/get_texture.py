from uuid import UUID

from avilla.core.builtins.command import AvillaCommands
from avilla.core import Context, Message, Notice
from avilla

from yggdrasil_mc.client import YggdrasilMC
from yggdrasil_mc.models import 

# region utils
LS_YGG = YggdrasilMC("https://littleskin.cn/api/yggdrasil")
# endregion

cmd = AvillaCommands(need_tome=False, remove_tome=False)

@cmd.on(r"%ygg {player_name: str}")
async def cmd_ygg(cx: Context, target: Notice, message: Message, player_name: str):
    try:
        player = await LS_YGG.by_name_async(player_name)
    except ValueError:
        _message = f"「{player_name}」不存在"
        _ = await cx.scene.send_message(_message, reply=message)
        return
    player_uuid = player.id
    _message = f"""「{player_name}」
Skin: {player.skin.hash[:8] if player.skin and player.skin.hash else None} [{player.skin.metadata.model if player.skin and player.skin.metadata else None}]
Cape: {player.cape.hash[:8] if player.cape and player.cape.hash else None}
UUID: {UUID(player_uuid).hex}"""
    _ = await cx.scene.send_message(_message, reply=message)