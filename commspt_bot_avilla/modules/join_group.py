from avilla.core import Context, MemberCreated, Notice, RequestReceived
from avilla.core.tools.filter import Filter
from graia.saya.builtins.broadcast.shortcut import dispatch, listen
from loguru import logger

from commspt_bot_avilla.models.littleskin_api import LittleSkinUser
from commspt_bot_avilla.models.mongodb_data import UIDMapping
from commspt_bot_avilla.utils.adv_filter import from_groups_preset_general
from commspt_bot_avilla.utils.random_sleep import random_sleep


@listen(RequestReceived)
@dispatch(
    Filter()
    .dispatch(RequestReceived)
    .all(
        [
            lambda e: e.request.request_type == "elizabeth::member_join",
            lambda e: from_groups_preset_general()(e.context.scene),
        ]
    )
)
async def member_join_request(ctx: Context, event: RequestReceived):
    req = event.request
    applicant = int(req.sender["contact"])
    if not req.message:
        return

    answer = req.message.splitlines()[-1].lstrip("答案：")
    logger.info(f"Event member_join was received. {applicant} : {answer}")

    if not answer.isdecimal():  # UID 应为十进制纯数字
        return

    uid = int(answer)

    # more sleep is better
    await random_sleep(3)
    # qmail api verification
    if ltsk_user := await LittleSkinUser.qmail_api(applicant):
        if ltsk_user.uid == uid:
            # ok: pass verification
            await UIDMapping(uid=uid, qq=applicant, qmail_verified=True).update()
            await req.accept()
            logger.info(f"Event member_join was accepted. {applicant} : {answer}")
            return

    # failed: not pass verification
    logger.info(f"Event member_join was ignored. {applicant} : {answer}")
    await UIDMapping(uid=uid, qq=applicant).update()


@listen(MemberCreated)
@dispatch(
    Filter()
    .dispatch(MemberCreated)
    .all(
        [
            lambda e: from_groups_preset_general()(e.context.scene),
        ]
    )
)
async def member_join_welcome(ctx: Context, event: MemberCreated):
    message = [Notice(ctx.client), "  "]

    # add UID info
    if uid_mapping := await UIDMapping.fetch(qq=int(ctx.client["member"])):
        message.append(
            f"UID:{uid_mapping.uid} {'✅' if uid_mapping.qmail_verified else '❔'}"
        )

    # add join announcement
    with open(".join-announcement.txt", encoding="utf-8") as f:
        join_announcement = f.read()
    message.append(join_announcement)

    # send
    await random_sleep(2)
    await ctx.scene.send_message(message)
