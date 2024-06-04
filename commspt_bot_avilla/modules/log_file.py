from avilla.core import Context, File, Message, MessageChain, MessageReceived
from avilla.core.tools.filter import Filter
from avilla.standard.core.file import FileData
from graia.saya.builtins.broadcast.shortcut import dispatch, listen
from loguru import logger
from rich import print

from commspt_bot_avilla.utils.adv_filter import dispatcher_from_preset_general


@listen(MessageReceived)
@dispatcher_from_preset_general
@dispatch(Filter().dispatch(Message).assert_true(lambda m: File in m.content))
async def process_log_file(ctx: Context, chain: MessageChain):
    logger.info("Received file from allowed group.")
    """
    received unsupported event: {'self_id': 111111111, 'user_id': 222222222, 'time': 1712930226, 'message_id': -2147456816, 'real_id': -2147456816,
         'message_type': 'group', 'sender': {'user_id': 222222222, 'nickname': '222222222', 'card': '222222222', 'role': 'owner'}, 'raw_message':
         '[CQ:file,file=log.log,path=,file_id=/936bc82d-1314-4520-93fd-000000000000,file_size=10507]', 'font': 14, 'sub_type': 'normal',   
         'message': [{'data': {'file': 'log.log', 'path': '', 'file_id': '/936bc82d-1314-4520-93fd-000000000000', 'file_size': '10507'},   
         'type': 'file'}], 'message_format': 'array', 'post_type': 'message', 'group_id': 333333333}
    """
    file = chain.get_first(File)
    print(await ctx.pull(FileData, file.resource.to_selector()))
