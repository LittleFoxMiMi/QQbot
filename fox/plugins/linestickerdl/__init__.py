from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.typing import T_State
from .stickerdl import sticker_download
from fox.check import qq_check


super_user = "./fox/data/config/superuser.txt"

linesticker = on_command(
    "line", aliases={"linesticker"}, priority=1, block=True)


@linesticker.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    args = str(event.get_message()).strip().split(" ")
    if not await qq_check(event.get_user_id(), super_user):
        linesticker.finish("你没有权限捏")
    if args != ['']:
        state["sticker_id"] = args[0]


@linesticker.got("sticker_id", prompt="need sticker pack id:")
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    code = await sticker_download(state["sticker_id"], linesticker, bot, event)
    if code != "OK":
        await linesticker.finish(code)
    else:
        await linesticker.send("下载完成")
