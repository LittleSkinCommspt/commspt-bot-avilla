from avilla.core import Context, MessageReceived, File, MessageChain

from avilla.core.tools.filter import Filter
from graia.saya.builtins.broadcast.shortcut import dispatch, listen
from loguru import logger
from commspt_bot_avilla.utils.adv_filter import from_groups_preset_general

from rich import print

@listen(MessageReceived)
@dispatch(
    Filter()
    .dispatch(MessageReceived)
    .assert_true(lambda e: from_groups_preset_general()(e.context.scene))
    .assert_true(lambda e: File in e.message.content)
)
async def process_log_file(ctx: Context, chain: MessageChain):
    logger.info("Received file from allowed group.")
    # file = chain.get_first(File)
    # print(await ctx.pull(File, file.resource.to_selector()))