from avilla.core import Context, Message
from avilla.core.builtins.command import AvillaCommands
from avilla.core.elements import Element, Picture
from avilla.core.tools.filter import Filter
from loguru import logger

from commspt_bot_avilla.utils.adv_filter import from_groups_preset_general
from commspt_bot_avilla.utils.random_sleep import random_sleep

cmd = AvillaCommands()


default_dispatchers = [
    Filter.cx.client.all([from_groups_preset_general()]),
]


def register(
    command: str, response: str | Element | list[str | Element], reply: bool = False
):
    """
    ### Simple Response：将简易响应注册到对应的命令事件，可选是否回复触发消息

    Args:
        command (str): The command to register.
        response (str | Element | list[str | Element]): The response to send when the command is triggered.
        reply (bool, optional): Flag indicating whether to reply to the triggering message. Defaults to False.

    Returns:
        None
    """
    logger.info(f"- ✅ {command}")

    # send simple response message
    async def _simple_response(cx: Context, message: Message):
        await random_sleep()
        await cx.scene.send_message(response, reply=message if reply else None)

    # register to command events
    cmd.on(
        command,
        dispatchers=default_dispatchers,
    )(_simple_response)


logger.info("registering simple response...")


register(r"%ping", "在", reply=True)

register(
    r"%cafe",
    [
        Picture("assets/honoka cafe ng.png"),
        "本群不允许闲聊，可以加入 Honoka Café 和大家一起水群。群号：651672723。",
    ],
)

register(r"%browser", Picture("assets/browser.png"), reply=True)

register(
    r"%log.csl",
    "CustomSkinLoader 的日志位于 .minecraft/CustomSkinLoader/CustomSkinLoader.log，请将文件直接发送至群内。",
)

register(
    r"%log.mc",
    "请使用启动器的「测试游戏」功能启动游戏，并在复现问题后导出日志发送至群内。如果问题与外置登录有关，请在启动器的「JVM 参数（Java 虚拟机参数）」设置中填入 -Dauthlibinjector.debug",
)

register(
    r"%pay",
    """在群里和大佬吹牛逼帮助不了你的问题？
https://afdian.net/@tnqzh123
买一对一帮助服务即可快速解决你的问题！""",
)

register(
    r"%csl.config",
    """若安装了 CustomSkinLoader 后无法正确加载皮肤，可能是当前角色名被同名正版优先加载，可通过以下方法手动修改 CustomSkinLoader 的加载顺序：
https://ln.putton.net/bH3
""",
)
