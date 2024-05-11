from arclet.alconna import Alconna, CommandMeta
from arclet.alconna.graia import alcommand
from avilla.core import Context, Message

from commspt_bot_avilla.models.version_api import (
    AuthlibInjectorLatest,
    CustomSkinLoaderLatest,
)


@alcommand(
    Alconna(
        r"%csl.latest",
        meta=CommandMeta(
            description="获取 CustomSkinLoader 最新版本信息",
            usage=r"%csl.latest",
            example=r"%csl.latest",
            author="SerinaNya",
        ),
    )
)
async def _(ctx: Context, message: Message):
    csl_latest = await CustomSkinLoaderLatest.get()
    await ctx.scene.send_message(
        f"「CustomSkinLoader」\n当前最新版本 > {csl_latest.version}\n\n{csl_latest.downloads.generate_download_text()}",
        reply=message,
    )


@alcommand(
    Alconna(
        r"%ygg.latest",
        meta=CommandMeta(
            description="获取 Yggdrasil 最新版本信息",
            usage=r"%ygg.latest",
            example=r"%ygg.latest",
            author="SerinaNya",
        ),
    )
)
async def _(ctx: Context, message: Message):
    ygg_latest = await AuthlibInjectorLatest.get()
    await ctx.scene.send_message(
        f"「AuthlibInjector」\n当前最新版本 > {ygg_latest.version}\n\n下载地址 > {ygg_latest.download_url}",
        reply=message,
    )
