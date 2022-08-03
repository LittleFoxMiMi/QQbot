from .banban import *
from fox.check import files_writer, qq_check
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot

admin_progress = on_command("admin", block=True, permission=GROUP)

super_user = "./fox/data/config/superuser.txt"
ban_path = "./fox/data/ban/"


@admin_progress.handle()
async def admin_pro(bot: Bot, event: GroupMessageEvent, state: T_State):
    args = str(event.get_message()).strip()
    if not await qq_check(event.get_user_id(), super_user):
        if not await qq_check(event.get_user_id(), ban_path+str(event.group_id)):
            await admin_progress.finish("你没有权限捏")
    if args == "":
        await admin_progress.finish("admin命令的语法是：\nadmin ban [时间] @某人\nadmin kick @某人\nadmin add @某人（添加权限）\nadmin del @某人（取消权限）\n")
    my_data = await bot.call_api(api="get_group_member_info", group_id=event.group_id, user_id=bot.self_id)
    if my_data["role"] == "member":
        admin_progress.finish("我没有权限捏")
    ag = args.split(" ")
    qq = await get_qq(args)
    if qq == "err":
        await admin_progress.finish("找不到对象捏")
    user_data = await bot.call_api(api="get_group_member_info", group_id=event.group_id, user_id=qq)
    if ag[0] == "ban" or ag[0] == "kick":
        if user_data["role"] != "member":
            await admin_progress.finish("对方是群主或管理")
        if await qq_check(qq, super_user):
            await admin_progress.finish("不可以口主人！")
    nickname = user_data["nickname"]
    if ag[0] == "ban":
        time = await get_time(ag[1])
        if time == "err":
            await admin_progress.finish("时间错误捏\n请用s、m、h、d来结尾\n0s为取消禁言")
        else:
            await bot.call_api(api="set_group_ban", group_id=event.group_id, user_id=qq, duration=time)
            await admin_progress.finish(f"已禁言{nickname}{time}s")
    elif ag[0] == "kick":
        await bot.call_api(api="set_group_kick", group_id=event.group_id, user_id=qq)
        await admin_progress.finish("命令成功完成")
    elif ag[0] == "add":
        await admin_progress.finish(await files_writer(qq, "off", ban_path+str(event.group_id)+".txt"))
    elif ag[0] == "del":
        await admin_progress.finish(await files_writer(qq, "on", ban_path+str(event.group_id)+".txt"))
    else:
        await admin_progress.finish("参数错误捏")
