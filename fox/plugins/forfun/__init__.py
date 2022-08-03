from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.plugin import on_keyword
from nonebot.typing import T_State
from .fun_source import *
from nonebot.adapters import Bot

love_true = on_keyword(keywords=["我永远喜欢"], block=True, permission=GROUP)


@love_true.handle()
async def love_p(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = str(event.raw_message).strip()
    name = re.sub('我永远喜欢', '', msg)
    user_data = await bot.call_api(api="get_group_member_info", group_id=event.group_id, user_id=event.user_id)
    nickname = user_data["card"]
    if nickname == "":
        nickname = user_data["nickname"]
    await love_true.finish(await love(name, nickname))

dog_true = on_keyword(keywords=["的狗"], block=False, permission=GROUP)


@dog_true.handle()
async def dog_p(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = str(event.raw_message).strip()
    name = await dog_name_get(msg)
    if name == "":
        return
    user_data = await bot.call_api(api="get_group_member_info", group_id=event.group_id, user_id=event.user_id)
    nickname = user_data["card"]
    if nickname == "":
        nickname = user_data["nickname"]
    rand = random.randint(0, 1)
    if rand == 0:
        dog_msg = await dog(name, nickname)
    else:
        dog_msg = await dog_dairy(name, nickname)
    await dog_true.finish(dog_msg)
