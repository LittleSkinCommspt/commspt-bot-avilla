from pathlib import Path

import arrow
from avilla.core import (
    Context,
    Notice,
    RequestEvent,
    SceneCreated,
)
from avilla.core.elements import Picture
from avilla.core.resource import RawResource
from avilla.core.tools.filter import Filter
from graia.saya.builtins.broadcast.shortcut import dispatch, listen
from richuru import logger

from commspt_bot_avilla.models.littleskin_api import LittleSkinUser
from commspt_bot_avilla.models.mongodb_data import UIDMapping
from commspt_bot_avilla.models.render_user_info import RenderUserInfo
from commspt_bot_avilla.utils.adv_filter import (
    dispatcher_from_preset_general,
    dispatcher_from_preset_general_no_commspt,
    dispatcher_from_preset_only_cafe,
)
from commspt_bot_avilla.utils.random_sleep import random_sleep
from commspt_bot_avilla.utils.setting_manager import S_

ANNOUNCEMENT_FILE = Path.cwd() / ".join-announcement.txt"


# region member join request
# region main
@listen(RequestEvent)
@dispatcher_from_preset_general_no_commspt
@dispatch(
    Filter()
    .dispatch(RequestEvent)
    .assert_true(
        lambda e: e.request.request_type in ["onebot11::group.add", "onebot11::group.invite"],
    ),
)
async def member_join_request(ctx: Context, event: RequestEvent):
    req = event.request
    applicant = int(req.sender["user"])
    message: list[str] = []
    if not req.message:
        return

    answer = req.message.splitlines()[-1].removeprefix("答案：").strip()
    logger.info(f"Member Join Request Event {req.request_type} id={req.id} was received. {applicant} > {answer}")
    message.append(
        f"""新的入群申请 (Main)
» 申请人 {applicant}
» 答案     {answer}

id={req.id}""",
    )

    if not answer.isdecimal():  # UID 应为十进制纯数字
        logger.warning(
            f"(main) Member Join Request Event {req.request_type} was ignored. (ANSWER NOT DECIMAL) {applicant} > {answer}",
        )
        message.append("👀 答案不是纯数字，需手动处理")
        await ctx.scene.into(f"::group({S_.defined_qq.commspt_group})").send_message(
            "\n\n".join(m for m in message if m),
        )
        return

    uid = int(answer)

    # more sleep is better
    await random_sleep(3)
    # qmail api verification
    if (ltsk_qmail := await LittleSkinUser.qmail_api(applicant)) and ltsk_qmail.uid == uid:
        # ok: pass verification
        await UIDMapping(uid=uid, qq=applicant, qmail_verified=True).update()
        logger.success(
            f"(main) Member Join Request Event {req.request_type} was accepted. (QMAIL PASS) {applicant} > {answer}",
        )
        await req.accept()
        message.append("👆 已同意，因为 QMAIL API 验证通过")
        # await ctx.scene.into(f"::group({S_.defined_qq.commspt_group})").send_message(
        #     "\n\n".join(m for m in message if m),
        # )
        return

    # lstk uid check
    if not await LittleSkinUser.uid_info(uid):
        # failed: uid not exists
        logger.warning(
            f"(main) Member Join Request Event {req.request_type} was ignored. (UID NOT EXISTS) {applicant} > {answer}",
        )
        message.append("👀 这个 UID 根本不存在，需手动处理")
        await ctx.scene.into(f"::group({S_.defined_qq.commspt_group})").send_message(
            "\n\n".join(m for m in message if m),
        )
        return

    if email_uid := await LittleSkinUser.qmail_api(qq=applicant):
        may_current_uid = email_uid.uid
        message.append(f"ⓘ 可能才为正确对应的 UID: {may_current_uid}")

    # failed: not pass verification
    logger.warning(f"(main) Member Join Request Event {req.request_type} was ignored. (GENERAL) {applicant} > {answer}")
    await UIDMapping(uid=uid, qq=applicant).update()
    message.append("👀 请手动处理")

    await random_sleep(4)
    # remove empty string or None
    await ctx.scene.into(f"::group({S_.defined_qq.commspt_group})").send_message("\n\n".join(m for m in message if m))


# endregion
# region cafe
@listen(RequestEvent)
@dispatcher_from_preset_only_cafe
async def _(ctx: Context, event: RequestEvent):
    req = event.request
    applicant = int(req.sender["user"])
    message: list[str] = []
    if not req.message:
        return

    answer = req.message.splitlines()[-1].removeprefix("答案：").strip()
    logger.info(f"(cafe) Member Join Request Event {req.request_type} id={req.id} was received. {applicant} > {answer}")
    message.append(
        f"""新的入群申请 (Cafe)
» 申请人 {applicant}
» 答案     {answer}

id={req.id}""",
    )

    if not answer.isdecimal():  # UID 应为十进制纯数字
        logger.warning(
            f"(cafe) Member Join Request Event {req.request_type} was ignored. (ANSWER NOT DECIMAL) {applicant} > {answer}",
        )
        message.append("👀 答案不是纯数字，需手动处理")
        await ctx.scene.into(f"::group({S_.defined_qq.littleskin_cafe})").send_message(
            "\n\n".join(m for m in message if m),
        )
        return

    uid = int(answer)

    # more sleep is better
    await random_sleep(3)

    # lstk uid check
    if not await LittleSkinUser.uid_info(uid):
        # failed: uid not exists
        logger.warning(
            f"(cafe) Member Join Request Event {req.request_type} was ignored. (UID NOT EXISTS) {applicant} > {answer}",
        )
        message.append("👀 这个 UID 根本不存在，需手动处理")
        await ctx.scene.into(f"::group({S_.defined_qq.littleskin_cafe})").send_message(
            "\n\n".join(m for m in message if m),
        )
        return

    # general: approve
    mapping_uid = await UIDMapping.fetch(qq=applicant)
    status = "✅" if (mapping_uid and mapping_uid.uid == uid) else "⚠️"
    await req.accept()
    await ctx.scene.into(f"::group({S_.defined_qq.littleskin_cafe})").send_message(
        f"(RESULT) Mapping {status}: QQ {applicant} -> UID {uid}",
    )


# endregion


# region member join welcome
@listen(SceneCreated)
@dispatcher_from_preset_general
async def member_join_welcome(ctx: Context, event: SceneCreated):
    welcome_msg = [Notice(event.context.endpoint), " "]
    nofi_msg = [f"用户已入群 > {event.context.endpoint.user}"]

    uid_mapping = await UIDMapping.fetch(qq=int(event.context.endpoint.user))

    # add UID info
    if uid_mapping:
        welcome_msg.append(f"UID: {uid_mapping.uid}  ")
        nofi_msg.append(f"UID: {uid_mapping.uid}")

    # add join announcement
    join_announcement = ANNOUNCEMENT_FILE.read_text(encoding="UTF-8")
    welcome_msg.append(f"\n{join_announcement}")

    # send to main group
    await random_sleep(2)
    await ctx.scene.send_message(welcome_msg)

    # render image

    if uid_mapping:
        image: bytes | None = None  # pre define
        ltsk_user = await LittleSkinUser.uid_info(uid_mapping.uid)
        # if qmail verified (only noti)
        if uid_mapping.qmail_verified:
            nofi_msg.append("QMAIL ✅ 验证通过")
        elif ltsk_user:
            nofi_msg.append(
                f"QMAIL {'❔ 与 QQ 号不匹配' if ltsk_user.email.lower().endswith('@qq.com') else '❌ 非 QQ 邮箱'}",
            )

        if ltsk_user:
            # check whether email contains uppercase letters (only noti)
            if ltsk_user.email.lower() != ltsk_user.email:
                nofi_msg.append("⚠️ 邮箱含有大写字母")

            # add LTSK email verification status (only noti)
            nofi_msg.append(f"邮箱验证 {'✅ 已验证' if ltsk_user.verified else '❌ 未验证'} ({ltsk_user.email})")

            # add registration time (only noti)
            reg_time = arrow.get(ltsk_user.register_at).to("Asia/Shanghai").format("YYYY-MM-DD HH:mm:ss")
            nofi_msg.append(f"注册时间: {reg_time}")

            # resay: if user was banned
            if ltsk_user.permission == -1:
                nofi_msg.append("❌ 账号被封禁")

            # render image
            render = RenderUserInfo(**ltsk_user.model_dump(), qq=int(event.context.endpoint.user))
            image = await render.get_image()
        else:
            # UID not exists
            nofi_msg.append("❌ 这个 UID 根本不存在")
    else:
        nofi_msg.append("🈚 未找到 UIDMapping 信息")

    await random_sleep(3)
    # send noti to commspt group
    await ctx.scene.into(f"::group({S_.defined_qq.notification_channel})").send_message(
        [Picture(RawResource(image)) if image else "", "\n".join(nofi_msg)],
    )


# endregion
