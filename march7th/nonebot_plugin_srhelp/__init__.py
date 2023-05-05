from typing import Dict, Set

from nonebot import on_command, require
from nonebot.adapters import Bot, Event
from nonebot.log import logger
from nonebot.plugin import Plugin, PluginMetadata, get_loaded_plugins

require("nonebot_plugin_saa")
require("nonebot_plugin_srbind")
require("nonebot_plugin_mys_api")

from nonebot_plugin_saa import Image, MessageFactory, Text

from .get_img import get_srhelp_img

__plugin_meta__ = PluginMetadata(
    name="StarRailHelp",
    description="崩坏：星穹铁道帮助信息查询",
    usage="""\
查看帮助:   srhelp
""",
    extra={
        "version": "1.0",
    },
)

srhelp = on_command("srhelp", aliases={"星铁帮助", "星铁功能"}, priority=2, block=True)


@srhelp.handle()
async def _():
    plugin_set: Set[Plugin] = get_loaded_plugins()
    plugin_info: Dict[str, Dict[str, str]] = {}
    for plugin in plugin_set:
        try:
            name = (
                plugin.metadata.name
                if plugin.metadata and plugin.metadata.name
                else plugin.module.__getattribute__("__help_plugin_name__")
            )
        except:
            name = plugin.name
        if name.startswith("StarRail"):
            plugin_info[name] = {}
            plugin_info[name]["description"] = (
                plugin.metadata.description
                if plugin.metadata and plugin.metadata.description
                else plugin.module.__getattribute__("__help_plugin_description__")
            )
            plugin_info[name]["usage"] = (
                plugin.metadata.usage
                if plugin.metadata and plugin.metadata.usage
                else plugin.module.__getattribute__("__help_plugin_usage__")
            )
    logger.debug(plugin_info)
    img = await get_srhelp_img(plugin_info)
    if img:
        msg_builder = MessageFactory([Image(img)])
    else:
        msg_builder = MessageFactory([Text("帮助图片绘制失败，请稍后重试")])
    await msg_builder.send()
    await srhelp.finish()