from avilla.core import Context, Message
from avilla.core.builtins.command import AvillaCommands
from avilla.core.elements import Picture
from graia.amnesia.message import Element
from avilla.core.tools.filter import Filter
from loguru import logger

from commspt_bot_avilla.utils.adv_filter import from_groups_preset_general
from commspt_bot_avilla.utils.random_sleep import random_sleep
from commspt_bot_avilla.utils.setting_manager import S_

cmd = AvillaCommands()


default_dispatchers = [
    Filter.cx.client.all([from_groups_preset_general()]),
]


# region register
def register(command: str, response: str | Element | list[str | Element], reply: bool = False):
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
        command=S_.command_prompt + command,
        dispatchers=default_dispatchers,
        need_tome=False,
        remove_tome=False,
    )(_simple_response)


# endregion

logger.info("registering simple response...")


register("ping", "在", reply=True)

# region ot
register(
    "cafe",
    [
        Picture("assets/images/honoka cafe ng.png"),
        "本群不允许闲聊，可以加入 Honoka Café 和大家一起水群。\n群号 👉🏻 651672723。",
    ],
)
# endregion

# region log
register("browser", Picture("assets/images/browser.png"), reply=True)

register(
    "log.csl",
    "CustomSkinLoader 的日志位于 .minecraft/CustomSkinLoader/CustomSkinLoader.log，请将文件直接发送至群内。",
)

register(
    "log.mc",
    "请使用启动器的「测试游戏」功能启动游戏，并在复现问题后导出日志发送至群内。如果问题与外置登录有关，请在启动器的「JVM 参数（Java 虚拟机参数）」设置中填入 -Dauthlibinjector.debug",
)

# region 过渡区
register(
    "csl.log",
    "CustomSkinLoader 的日志位于 .minecraft/CustomSkinLoader/CustomSkinLoader.log，请将文件直接发送至群内。",
)
# endregion

# endregion

# region csl
register(
    "csl.config",
    """若安装了 CustomSkinLoader 后无法正确加载皮肤，可能是当前角色名被同名正版优先加载，可通过以下方法手动修改 CustomSkinLoader 的加载顺序：
https://manual.littlesk.in/newbee/mod#edit-csl-config""",
)
# endregion

# region other
register(
    "pay",
    """在群里和大佬吹牛逼帮助不了你的问题？
https://afdian.net/a/tnqzh123
买一对一帮助服务即可快速解决你的问题！""",
)

register(
    "manual",
    [
        Picture("assets/images/rtfm.png"),
        """请仔细阅读 LittleSkin 用户使用手册，特别是「常见问题解答」！
https://manual.littlesk.in/""",
    ],
)

register(
    "pro_verify",
    """目前在 LittleSkin 验证正版后会产生如下影响：
· 在主页上获得一个「正版」（英文为「Pro」）徽标
· 赠送您 1000 积分；
· 在皮肤站内取回您的正版 ID 对应的角色（如果您的 ID 已被人抢注）。

请注意，无论是否进行正版验证，您的 LittleSkin 外置登录账号始终不具备正版的属性，性质 **仍为离线账号**。
您无法将 LittleSkin 外置登录账号代替正版账号使用。""",
)

register(
    "ygg.online_mode",
    """请确认服务器正确配置 authlib-injector 并将 online-mode 设为 true，否则请使用 CustomSkinLoader。
如果服务器未开启「正版验证」则所有登录方式都会被服务器视为离线模式处理；
即服务器自行生成 UUID，且不会向验证服务器（皮肤站 / 正版）获取材质。
详细：https://manual.littlesk.in/yggdrasil/""",
)

register(
    "cape_format",
    """「不是有效的披风文件」
LittleSkin 对于披风文件的格式要求如下：
· png 格式文件；
· 宽高比需为 2:1；
· 为 64x32 的整倍数。""",
)

register(
    "network",
    """「登录失败：身份验证服务器目前正在停机维护」
「无法验证用户名」
「验证服务器他们宕了吗？」：
玄学的网络问题会导致此情况的出现，请优先检查您的网络环境和使用的域名是否为 littleskin.cn，并在重启游戏后再次尝试登录。

如果您位于福建省，有概率因为地区性的 DNS 污染而导致无法连接到 LittleSkin。
此时请您查阅群公告以解决此问题。
有时部分无法连接的问题也可通过群公告的教程解决。""",
)
# endregion
