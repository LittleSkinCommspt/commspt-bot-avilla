from typing import Literal, Optional

from arclet.alconna import Alconna, Args
from arclet.alconna.graia import Match, alcommand
from avilla.core import Context, Message, Notice, RequestEvent, SceneCreated, Selector
from avilla.core.elements import Reference
from avilla.core.tools.filter import Filter
from graia.saya.builtins.broadcast.shortcut import dispatch, listen
from loguru import logger

from commspt_bot_avilla.models.littleskin_api import LittleSkinUser
from commspt_bot_avilla.models.mongodb_data import UIDMapping
from commspt_bot_avilla.utils.adv_filter import (
    dispatcher_from_preset_general,
    dispather_by_admin_only,
)
from commspt_bot_avilla.utils.random_sleep import random_sleep
from commspt_bot_avilla.utils.setting_manager import S_


# region member join request
@listen(RequestEvent)
@dispatcher_from_preset_general
@dispatch(
    Filter()
    .dispatch(RequestEvent)
    .assert_true(
        lambda e: e.request.request_type
        in ["onebot11::group.add", "onebot11::group.invite"],
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
        f"""新的入群申请待处理
👉 申请人 {applicant}
👉 答案    {answer}

id={req.id}"""
    )

    if not answer.isdecimal():  # UID 应为十进制纯数字
        if req.request_type != "onebot11::group.invite":
            # 非邀请，正常流程应拒绝
            await req.reject("UID应为纯数字，再仔细看看")
            await random_sleep(2)
            await ctx.scene.into(
                f"::group({S_.defined_qq.commspt_group})"
            ).send_message("👆 已拒绝，因为 UID 不是纯数字")
        else:
            # 邀请加群，可能身份特殊，不能直接拒绝
            await random_sleep()
            await ctx.scene.into(
                f"::group({S_.defined_qq.commspt_group})"
            ).send_message(
                "👆 虽然填写的 UID 不是纯数字，但是此请求为邀请加群，请手动处理"
            )
        return

    uid = int(answer)

    # more sleep is better
    await random_sleep(3)
    # MARK: qmail api verification
    if ltsk_qmail := await LittleSkinUser.qmail_api(applicant):
        if ltsk_qmail.uid == uid:
            # ok: pass verification
            await UIDMapping(uid=uid, qq=applicant, qmail_verified=True).update()
            logger.info(
                f"Member Join Request Event {req.request_type} was accepted. (QMAIL PASS) {applicant} > {answer}"
            )
            await req.accept()
            await random_sleep()
            await ctx.scene.into(
                f"::group({S_.defined_qq.commspt_group})"
            ).send_message("👆 已同意，因为 QMAIL API 验证通过")
            return

    # MARK: lstk uid check
    if not await LittleSkinUser.uid_info(uid):
        # failed: uid not exists
        logger.info(
            f"Member Join Request Event {req.request_type} was rejected. (UID NOT EXISTS) {applicant} > {answer}"
        )
        await req.reject("UID 有误，再仔细看看")
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


# endregion


# region member join welcome
@listen(SceneCreated)
@dispatcher_from_preset_general
async def member_join_welcome(ctx: Context, event: SceneCreated):
    welcome_msg = [Notice(event.context.endpoint), " "]
    nofi_msg = [f"用户已入群 > {event.context.endpoint.user}"]

    # add UID info
    if uid_mapping := await UIDMapping.fetch(qq=int(event.context.endpoint.user)):
        welcome_msg.append(f"UID: {uid_mapping.uid}  ")
        nofi_msg.append(f"UID: {uid_mapping.uid}")
        nofi_msg.append(
            f"QMAIL {'✅一致性校验通过' if uid_mapping.qmail_verified else '❔'}"
        )

    # add LTSK email verification status (only noti)
        if ltsk_user := await LittleSkinUser.uid_info(uid_mapping.uid):
            nofi_msg.append(
                f"邮箱验证 {'✅已验证' if ltsk_user.verified else f'❌未验证 ({ltsk_user.email})'}"
            )

    # send noti to commspt group
    await ctx.scene.into(f"::group({S_.defined_qq.commspt_group})").send_message(
        "\n".join(nofi_msg)
    )

    # add join announcement
    with open(".join-announcement.txt", encoding="utf-8") as f:
        join_announcement = f.read()
    welcome_msg.append(f"\n{join_announcement}")

    # send
    await random_sleep(2)
    await ctx.scene.send_message(welcome_msg)


# endregion


# disabled for now
@alcommand(
    Alconna(
        r"do join",
        Args["action", Literal["accpet", "reject"]]["reason", Optional[str], None],
    )
)
@dispatcher_from_preset_general
@dispather_by_admin_only
async def do_join_action(
    ctx: Context,
    message: Message,
    action: Match[Literal["accpet", "reject"]],
    reason: Match[Optional[str]],
):
    ref = message.content.get_first(Reference).message
    scene = Selector().land("qq").user()
    match action.result:
        case "accept":
            await ctx.accept()
        case "reject":
            await ctx.reject()
    ...
