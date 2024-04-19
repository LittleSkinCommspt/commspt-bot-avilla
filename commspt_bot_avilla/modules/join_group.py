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

    answer = req.message.splitlines()[-1].removeprefix("答案：").strip()
    logger.info(
        f"Member Join Request Event {req.request_type} id={req.id} was received. {applicant} > {answer}"
    )
    await ctx.scene.into(f"::group({S_.defined_qq.commspt_group})").send_message(
        f"""新的入群申请待处理
👉 申请人 {applicant}
👉 答案     {answer}

id={req.id}"""
    )

    if not answer.isdecimal():  # UID 应为十进制纯数字
        logger.info(
            f"Member Join Request Event {req.request_type} was ignored. (ANSWER NOT DECIMAL) {applicant} > {answer}"
        )
        await random_sleep()
        await ctx.scene.into(f"::group({S_.defined_qq.commspt_group})").send_message(
            "👆 答案不是纯数字，亦需手动处理 👀"
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
            f"Member Join Request Event {req.request_type} was ignored. (UID NOT EXISTS) {applicant} > {answer}"
        )
        await random_sleep()
        await ctx.scene.into(f"::group({S_.defined_qq.commspt_group})").send_message(
            "👆 这个 UID 根本不存在，亦需手动处理 👀"
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
        ltsk_user = await LittleSkinUser.uid_info(uid_mapping.uid)
        welcome_msg.append(f"UID: {uid_mapping.uid}  ")
        nofi_msg.append(f"UID: {uid_mapping.uid}")
        
        # if qmail verified (only noti)
        if uid_mapping.qmail_verified:
            nofi_msg.append("QMAIL ✅验证通过")
        elif ltsk_user:
            nofi_msg.append(f"QMAIL {'❔与 QQ 号不匹配' if ltsk_user.email.lower().endswith('@qq.com') else '❌非 QQ 邮箱'}")
            
        if ltsk_user:
            # check whether email contains uppercase letters (only noti)
            if ltsk_user.email.lower() != ltsk_user.email:
                nofi_msg.append("⚠️ 该用户的邮箱含有大写字母")

            # add LTSK email verification status (only noti)
            nofi_msg.append(
                f"邮箱验证 {'✅已验证' if ltsk_user.verified else '❌未验证'} ({ltsk_user.email})"
            )
        else:
            # UID not exists
            nofi_msg.append("❌这个 UID 根本不存在")
    else:
        nofi_msg.append("🈚 未找到 UIDMapping 信息")

    await random_sleep(3)
    # send noti to commspt group
    await ctx.scene.into(f"::group({S_.defined_qq.commspt_group})").send_message(
        "\n".join(nofi_msg)
    )

    # add join announcement
    with open(".join-announcement.txt", encoding="utf-8") as f:
        join_announcement = f.read()
    welcome_msg.append(f"\n{join_announcement}")

    # send to main group
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
