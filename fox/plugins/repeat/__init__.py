from fox.check import files_writer, qq_check
from nonebot.plugin import on_command, on_message
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.typing import T_State
from .repeater import *

repeat_message = on_message(
    permission=GROUP,
    priority=5,
    block=True,
)
ban_group = "./fox/data/repeater_data/ban_group.txt"
super_user = "./fox/data/config/superuser.txt"


@repeat_message.handle()
async def repeat_message_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    if event.to_me:
        return
    msg = str(event.get_message())
    qun = str(event.group_id)
    if await qq_check(qun, ban_group):
        return
    if await mre(qun, msg):
        await repeat_message.send(msg)


repeat_ban = on_command("repeat", rule=None, block=True)


@repeat_ban.handle()
async def repeater_ban(bot: Bot, event: GroupMessageEvent, state: T_State):
    args = str(event.get_message()).strip()
    qun = event.group_id
    if args == "":
        if await qq_check(qun, ban_group):
            await repeat_ban.finish(f"群{qun}的复读功能已经禁用")
        else:
            await repeat_ban.finish(f"群{qun}的复读功能已开启")
    elif args == "off" or args == "on":
        if await qq_check(event.user_id, super_user):
            await repeat_ban.finish(await files_writer(qun, args, ban_group))
        else:
            await repeat_ban.finish("你没有权限捏")
    else:
        await repeat_ban.finish("参数错误")
