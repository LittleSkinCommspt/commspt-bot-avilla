import pkgutil

import richuru
from avilla.core import Avilla
from creart import it
from graia.broadcast import Broadcast
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour
from loguru import logger
from rich.markdown import Markdown

from commspt_bot_avilla.utils.setting_manager import S_


def main():
    richuru.install()

    broadcast = it(Broadcast)
    saya = Saya(broadcast)
    saya.install_behaviours(BroadcastBehaviour(broadcast))

    # saya load modules

    logger.info("Loading Saya modules...")

    with saya.module_context():
        for module_info in pkgutil.iter_modules(["commspt_bot_avilla/modules"]):
            logger.info(
                f"- module: {module_info.name}",
                rich=Markdown(f"# module: `{module_info.name}`"),
            )
            saya.require(f"commspt_bot_avilla.modules.{module_info.name}")
            logger.info("------", rich=Markdown("---"))

    # apply protocols

    avilla = Avilla()
    if S_.dev_mode:
        from avilla.console.protocol import ConsoleProtocol

        avilla.apply_protocols(ConsoleProtocol())
    else:
        from avilla.onebot.v11.protocol import OneBot11ForwardConfig, OneBot11Protocol

        config = OneBot11ForwardConfig(**S_.connection.model_dump())
        logger.info(f"Protocol connection config: {config}")
        avilla.apply_protocols(OneBot11Protocol().configure(config))

    # finally launch

    avilla.launch()
