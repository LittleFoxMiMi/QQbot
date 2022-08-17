from .data_source import get_reply
from .config import Config
import traceback
import os
from loguru import logger
from nonebot import on_command, require
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Message, MessageEvent, GroupMessageEvent, Bot
from nonebot.typing import T_State
from nonebot.log import logger


__plugin_meta__ = PluginMetadata(
    name="成分姬",
    description="查询B站用户关注的VTuber成分",
    usage="查成分 B站用户名/UID",
    config=Config,
    extra={
        "unique_name": "ddcheck",
        "example": "查成分 小南莓Official",
        "author": "meetwq <meetwq@gmail.com>",
        "version": "0.1.11",
    },
)


ddcheck = on_command("查成分", block=True, priority=12)


@ddcheck.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = str(event.get_message()).strip().split(" ")
    args = args[1:]
    if len(args) == 1:
        text = args[0]
    if not text:
        await ddcheck.finish()

    try:
        code = await get_reply(text)
    except:
        logger.warning(traceback.format_exc())
        await ddcheck.finish("出错了，请稍后再试")

    if code != 0:
        await ddcheck.finish(code)

    if isinstance(event, GroupMessageEvent):
        await bot.call_api(api="send_group_msg", group_id=event.group_id, message=f"[CQ:image,file=file:///{os.path.abspath('./fox/data/ddcheck/out.jpg')}]")
    else:
        await bot.call_api(api="send_msg", user_id=event.get_user_id(), message=f"[CQ:image,file=file:///{os.path.abspath('./fox/data/ddcheck/out.jpg')}]")
