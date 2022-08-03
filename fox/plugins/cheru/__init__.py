from nonebot.adapters.cqhttp.event import Event
from nonebot.typing import T_State
from .cheru_p import *
from nonebot.plugin import on_command, on_keyword
from nonebot.adapters import Bot

cheru_it = on_command("切噜一下", block=True)


@cheru_it.handle()
async def cheru_encode(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    if len(msg) > 500:
        await cheru_it.finish('切、切噜太长切不动切噜噜……')
    else:
        await cheru_it.finish('切噜～♪'+str2cheru(msg))

cheru_de = on_keyword(keywords=["切噜～♪"], block=True)


@cheru_de.handle()
async def cheru_decode(bot: Bot, event: Event, state: T_State):
    msg = str(event.raw_message).strip()
    if msg[0:4] != '切噜～♪':
        return
    msg = msg[4:]
    if len(msg) > 1500:
        result = '切、切噜太长切不动切噜噜……'
    else:
        result = '切噜噜是：\n' + cheru2str(msg)
    await cheru_de.finish(result)
