from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent
from nonebot.typing import T_State
from .homo_code import homo_it


homo = on_command(
    "homo", aliases={"恶臭论证"}, priority=1, block=True)


@homo.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = str(event.get_message()).strip().split(" ")
    if args != ['']:
        state["homo_number"] = args[0]


@homo.got("homo_number", prompt="需要被认证的数字")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    print(state["homo_number"])
    homo_result = await homo_it(state["homo_number"])
    await homo.finish(homo_result)
