from fox.check import qq_check
from nonebot.typing import T_State
from .bilibili_p import *
from nonebot import get_bots
from nonebot_plugin_apscheduler import scheduler
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.plugin import on_command

list_adress = "./fox/data/bilibili/list.json"
super_user = "./fox/data/config/superuser.txt"


@scheduler.scheduled_job('interval', seconds=180)
async def main():
    bot = get_bots()["3126986401"]
    data = await data_load(list_adress)
    for i in data["data"]:
        try:
            dynamic_content = await GetDynamicStatus(i["uid"], i["nickname"])
        except Exception as e:
            print("pilipili network error")
            continue
        for group_id in i["group_id"]:
            for content in dynamic_content:
                await bot.call_api(
                    api="send_group_msg",
                    group_id=group_id,
                    message=content)
        room_id = await get_live_room_id(i["uid"])
        live_status = await GetLiveStatus(room_id)
        if live_status != '':
            for group_id in i["group_id"]:
                await bot.call_api(
                    api="send_group_msg",
                    group_id=group_id,
                    message=i["nickname"] +
                    ' 开播啦啦啦！！！ ' + live_status
                )

bili_describe = on_command('b站订阅', block=True, permission=GROUP, aliases={
                           "B站订阅", "bilibili订阅"})


@bili_describe.handle()
async def bili_admin(bot: Bot, event: GroupMessageEvent, state: T_State):
    if not await qq_check(event.get_user_id(), super_user):
        bili_describe.finish("你没有权限捏")
    data = await data_load(list_adress)
    args = str(event.get_message()).strip()
    ag = args.split(" ")
    if args == "":
        await bili_describe.finish(message=str(await group_query(event.group_id, data)))
    try:
        if ag[0] == "添加订阅":
            nickname = ag[1]
            uid = ag[2]
            if len(str(await aio_get(f'https://api.bilibili.com/x/space/acc/info?mid={uid}&jsonp=jsonp'))) < 50:
                await bili_describe.finish("404 Uid Not Found!\n你大概是输错了罢。。。\n      对话已关闭")
            else:
                await bili_describe.finish(str(await describe_writer(data, "add", nickname, uid, event.group_id)))
        elif ag[0] == "取消订阅":
            uid = ag[2]
            await bili_describe.finish(str(await describe_writer(data, "del", "", uid, event.group_id)))
    except Exception as e:
        if len(ag) < 3:
            await bili_describe.finish("参数错误捏\n正确的命令格式为\n'b站订阅 | 取消/添加订阅 | 昵称 | uid'")
