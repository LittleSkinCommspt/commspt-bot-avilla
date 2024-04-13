from avilla.core import Context, Notice, RequestEvent, SceneCreated
from avilla.core.tools.filter import Filter
from graia.saya.builtins.broadcast.shortcut import dispatch, listen
from loguru import logger

from commspt_bot_avilla.models.littleskin_api import LittleSkinUser
from commspt_bot_avilla.models.mongodb_data import UIDMapping
from commspt_bot_avilla.utils.adv_filter import from_groups_preset_general
from commspt_bot_avilla.utils.random_sleep import random_sleep
from commspt_bot_avilla.utils.setting_manager import S_


@listen(RequestEvent)
@dispatch(
    Filter()
    .dispatch(RequestEvent)
    .all(
        [
            lambda e: e.request.request_type
            in ["onebot11::group.add", "onebot11::group.invite"],
            lambda e: from_groups_preset_general()(e.context.scene),
        ]
    )
)
async def member_join_request(ctx: Context, event: RequestEvent):
    req = event.request
    applicant = int(req.sender["user"])
    if not req.message:
        return

    answer = req.message.splitlines()[-1].lstrip("答案：")
    logger.info(
        f"Member Join Request Event {req.request_type} id={req.id} was received. {applicant} > {answer}"
    )
    await ctx.scene.into(f"::group({S_.defined_qq.commspt_group})").send_message(
        f"新的入群申请待处理\n${applicant} > {answer}\n\nreq={req.id}/\n{req.request_type.removeprefix('onebot11::group.')}"
    )

    if not answer.isdecimal():  # UID 应为十进制纯数字
        return

    uid = int(answer)

    # more sleep is better
    await random_sleep(3)
    # qmail api verification
    if ltsk_qmail := await LittleSkinUser.qmail_api(applicant):
        if ltsk_qmail.uid == uid:
            # ok: pass verification
            await UIDMapping(uid=uid, qq=applicant, qmail_verified=True).update()
            logger.info(
                f"Member Join Request Event {req.request_type} was accepted. (QMAIL PASS) {applicant} > {answer}"
            )
            await req.accept()
            await random_sleep(1)
            await ctx.scene.into(
                f"::group({S_.defined_qq.commspt_group})"
            ).send_message("👆 已同意，因为 QMAIL API 验证通过")
            return

    # lstk uid check
    if not await LittleSkinUser.uid_info(uid):
        # failed: uid not exists
        logger.info(
            f"Member Join Request Event {req.request_type} was rejected. (UID NOT EXISTS) {applicant} > {answer}"
        )
        await req.reject("UID有误，再仔细看看")
        await random_sleep(1)
        await ctx.scene.into(f"::group({S_.defined_qq.commspt_group})").send_message(
            "👆 已拒绝，因为这个 UID 根本不存在"
        )

        return

    # failed: not pass verification
    logger.info(
        f"Member Join Request Event {req.request_type} was ignored. (GENERAL) {applicant} > {answer}"
    )
    await UIDMapping(uid=uid, qq=applicant).update()


@listen(SceneCreated)
@dispatch(
    Filter()
    .dispatch(SceneCreated)
    .all(
        [
            lambda e: from_groups_preset_general()(e.context.scene),
        ]
    )
)
async def member_join_welcome(ctx: Context, event: SceneCreated):
    message = [Notice(event.context.endpoint), " "]

    # add UID info
    if uid_mapping := await UIDMapping.fetch(qq=int(event.context.endpoint.user)):
        message.append(
            f"UID:{uid_mapping.uid} / QMAIL一致{'✅' if uid_mapping.qmail_verified else '❔'}\n"
        )

    if ltsk_user := await LittleSkinUser.uid_info(int(event.context.endpoint.user)):
        message.append(
            f"邮箱验证:{'✅' if ltsk_user.verified else '❌'}\n"
        )

    # add join announcement
    with open(".join-announcement.txt", encoding="utf-8") as f:
        join_announcement = f.read()
    message.append(join_announcement)

    # send
    await random_sleep(2)
    await ctx.scene.send_message(message)
