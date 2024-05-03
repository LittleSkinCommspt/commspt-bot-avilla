import re
from typing import Literal

from arclet.alconna import Alconna, Args, CommandMeta
from arclet.alconna.graia import Match, alcommand
from avilla.core import (
    Context,
    Message,
    RequestCapability,
    Selector,
    Text,
)
from avilla.core.tools.filter import Filter
from graia.saya.builtins.broadcast.shortcut import dispatch
from loguru import logger

from commspt_bot_avilla.utils.adv_filter import (
    dispatcher_from_preset_commspt,
    dispather_by_admin_only,
)
from commspt_bot_avilla.utils.random_sleep import random_sleep
from commspt_bot_avilla.utils.setting_manager import S_


# region do join action
@alcommand(
    Alconna(
        r"do",
        Args["action", Literal["accept", "reject"]][
            "reason", str, "答案错误，再仔细看看"
        ],
        meta=CommandMeta(
            description="处理入群请求 (commspt only)",
            usage="do <accept|reject> [reason]",
            example="do accept",
            author="SerinaNya",
        ),
    )
)
@dispather_by_admin_only
@dispatcher_from_preset_commspt
@dispatch(
    Filter().dispatch(Message).assert_true(lambda message: message.reply is not None)
)
async def do_action_join(
    ctx: Context,
    message: Message,
    action: Match[Literal["accept", "reject"]],
    reason: Match[str],
):
    logger.info("received do action (join group request)")

    # check origin message
    if not message.reply:
        await ctx.scene.send_message(
            "需要回复一条申请提示消息以进行处理", reply=message
        )
        return
    origin_message = await ctx.pull(Message, message.reply)
    origin_raw_text = origin_message.content.get_first(Text).text
    req_match = re.search(r"^id=(.*)$", origin_raw_text, re.MULTILINE)
    applicant_match = re.search(r"申请人\s*(.*)$", origin_raw_text, re.MULTILINE)

    # if check failed then kill
    if not (
        origin_raw_text.startswith("新的入群申请") and req_match and applicant_match
    ):
        return

    reqid = req_match.group(1)
    applicant = applicant_match.group(1)
    logger.info(
        f"do action (join group request): {action.result=}, {reason.result=}, {applicant=}, {reqid=}"
    )

    # make selector
    scene = Selector().land("qq").group("")
    selector = scene.request(f"onebot11::group.{reqid.split('_')[0]}@{reqid}")

    # Fn action
    await random_sleep(3)
    match action.result:
        case "accept":
            await ctx[RequestCapability.accept](selector)
            logger.info("accepted")
        case "reject":
            await ctx[RequestCapability.reject](selector, reason=reason.result)
            logger.info("rejected")
    await ctx.scene.send_message(f"{action.result}ed {applicant}", reply=message)


# endregion
