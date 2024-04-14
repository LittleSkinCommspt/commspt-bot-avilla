import pkgutil

import richuru
from arclet.alconna.avilla import AlconnaAvillaAdapter
from arclet.alconna.graia import AlconnaBehaviour, AlconnaGraiaService
from avilla.core import Avilla
from creart import it
from graia.broadcast import Broadcast
from graia.saya import Saya
from launart import Launart
from loguru import logger

from commspt_bot_avilla.utils.setting_manager import S_


def main():
    richuru.install()

    # region init launart
    manager = Launart()
    saya = it(Saya)
    broadcast = it(Broadcast)
    it(AlconnaBehaviour)
    manager.add_component(
        AlconnaGraiaService(AlconnaAvillaAdapter, global_remove_tome=True)
    )
    # endregion

    # region saya load modules
    logger.info("Loading Saya modules...")

    with saya.module_context():
        for module_info in pkgutil.iter_modules(["commspt_bot_avilla/modules"]):
            logger.info(
                f"- module: {module_info.name}",
            )
            saya.require(f"commspt_bot_avilla.modules.{module_info.name}")
    # endregion

    # region apply protocols
    avilla = Avilla(broadcast=broadcast, launch_manager=manager)
    if S_.dev_mode:
        from avilla.console.protocol import ConsoleProtocol

        avilla.apply_protocols(ConsoleProtocol())
    else:
        from avilla.onebot.v11.protocol import OneBot11ForwardConfig, OneBot11Protocol

        config = OneBot11ForwardConfig(**S_.connection.model_dump())
        logger.info(f"Protocol connection config: {config}")
        avilla.apply_protocols(OneBot11Protocol().configure(config))
    # endregion

    avilla.launch()
