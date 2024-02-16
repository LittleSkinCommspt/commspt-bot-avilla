from avilla.core import Context, Message
from avilla.core.builtins.command import AvillaCommands
from avilla.core.elements import Notice
from avilla.core.tools.filter import Filter
from loguru import logger

from commspt_bot_avilla.models.mongodb_data import UIDMapping
from commspt_bot_avilla.utils.adv_filter import by_admin_only
from commspt_bot_avilla.utils.random_sleep import random_sleep

cmd = AvillaCommands(need_tome=False, remove_tome=True)

default_dispatchers = [
    Filter.cx.client.assert_true(by_admin_only()),
]


@cmd.on(r"%uid {target}", dispatchers=default_dispatchers)
async def cmd_uid(cx: Context, target: Notice, message: Message):
    target_qq = int(target.target["member"])
    logger.info(f"UID search: {target_qq}")
    uid_mapping = await UIDMapping.fetch(qq=target_qq)
    logger.info(f"UID search: {target_qq} -> {uid_mapping}")
    await random_sleep()
    if uid_mapping:
        await cx.scene.send_message(
            f"QQ {target_qq} UID {uid_mapping.uid} QMAIL {'✅' if uid_mapping.qmail_verified else '❌'}",
            reply=message,
        )
    else:
        await cx.scene.send_message(f"找不到 {target_qq} 在缓存中的 UID", reply=message)
