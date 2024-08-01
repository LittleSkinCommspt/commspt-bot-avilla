from arclet.alconna.exceptions import SpecialOptionTriggered
from arclet.alconna.graia import CommandResult
from avilla.core import Context, Message


async def command_prehandler(ctx: Context, res: CommandResult, message: Message):
    if not res.result.error_info:
        return
    if isinstance(res.result.error_info, SpecialOptionTriggered):
        await ctx.scene.send_message(res.output or "NOTICE > Special Option Triggered", reply=message)
    await ctx.scene.send_message(f"> {res.result.error_info}\n\n请使用 {res.result.header_match.result} -h 查看帮助。")
