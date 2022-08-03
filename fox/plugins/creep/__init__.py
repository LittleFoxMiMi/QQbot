from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.typing import T_State
from .creepit import *
from nonebot.plugin import on_keyword
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.adapters import Bot
from fox.check import qq_check

super_user = "./fox/data/config/superuser.txt"

creeper = on_keyword(keywords=["爬", "爪巴"], permission=GROUP, block=True)


@creeper.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = event.get_message()
    qq = await get_at_qq(msg)
    if qq:
        if await qq_check(qq, super_user):
            qq = event.get_user_id()
        outPath = await creep(qq)
        sendMsg = await pictureCqCode(outPath)
        await bot.call_api(api="send_group_msg", group_id=event.group_id, message=sendMsg)
