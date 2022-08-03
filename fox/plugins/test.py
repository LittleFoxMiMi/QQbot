from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import time

test = on_command("test", rule=to_me(), aliases={"测试"}, block=True)


@test.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["par"] = args


@test.got("par", prompt="1.获取系统时间\n2.测试命令")
async def test_handle(bot: Bot, event: Event, state: T_State):
    par = state["par"]
    msg = await test_mission(par)
    await test.finish(msg)


async def test_mission(par):
    if par == "1":
        localtime = time.asctime(time.localtime(time.time()))
        return localtime
    elif par == "2":
        return "test"
    else:
        return "错误的参数"
