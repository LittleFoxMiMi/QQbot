from nonebot.rule import to_me
from .pixiv_p import download_pic, lolicon_api
from fox.check import files_writer, qq_check
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, GROUP
from nonebot.plugin import on_command
from nonebot.adapters import Bot
from nonebot.typing import T_State

pixiv = on_command('来点涩图', block=True, permission=GROUP, aliases={"来点色图"})


ban_group = ban_group = "./fox/data/pixiv/ban_group.txt"
r18_group = "./fox/data/pixiv/r18_group.txt"
super_user = "./fox/data/config/superuser.txt"

help_text = "可选参数 [R18] 只有管理员允许才能启用\n\
可选参数 [tag] 用tag来限定范围，可以用 | 来使用多个tag，有简易的限定词转换\n\
例如：来点涩图 r18 tag=vtb \n\
管理员请@机器人使用pixiv_admin命令进行管理\n\n\
vtb = > 虚拟YouTuber | VTuber\n\
fgo = > Fate/GrandOrder | Fate/Grand Order | FateGrandOrder\n\
pcr = > 公主连结 | 公主连结Re: Dive | プリンセスコネクト\n\
gbf = > 碧蓝幻想\n\
舰b = > 碧蓝航线 | AzurLane\n\
舰c = > 舰队collection\n\
少前 = > 少女前线 | girlsfrontline"


@pixiv.handle()
async def pi(bot: Bot, event: GroupMessageEvent, state: T_State):
    args = str(event.get_message()).strip().split(" ")
    args = args[1:]
    if len(args) != 0:
        if len(args) > 2:
            await pixiv.send("过多的参数！")
        elif args[0] == "?" or args[0] == "help":
            await pixiv.finish(help_text)
    if await qq_check(event.group_id, ban_group):
        await pixiv.finish("不许ghs喵！")
    await pixiv.send("loading...")
    r18 = 0
    tag = ""
    if len(args) != 0:
        for par in args:
            if par == "r18" or par == "R18":
                r18 = 1
            elif "tag=" in par:
                tag = par[4:]
            else:
                pixiv.finish("错误的参数！使用help来查看帮助捏")
    if r18 == 1:
        if not await qq_check(event.group_id, r18_group):
            await pixiv.finish("不许R18喵！")
    url = await lolicon_api(r18, tag)
    if len(url) != 2:
        err = str(url)
        await pixiv.finish(f"工口发生！api调用失败捏！\n{err}")
    if await download_pic(url[0], url[1]) == "err":
        await pixiv.finish("工口发生！图片下载失败捏")
    await bot.call_api(api="send_group_msg", group_id=event.group_id, message="[CQ:image,file=file:///home/qqbot/fox/data/pixiv/image/_tt.jpg]")
    return


pixiv_r18 = on_command("pixiv_admin", rule=to_me(), block=True)


@pixiv_r18.handle()
async def p_admin(bot: Bot, event: GroupMessageEvent, state: T_State):
    args = str(event.get_message()).strip().split(" ")
    args = args[1:]
    if len(args) != 1:
        await pixiv_r18.finish("参数错误捏\nban,allow,ban_r18,allow_r18")
    arg = args[0]
    if not await qq_check(event.get_user_id(), super_user):
        await pixiv_r18.finish("你没有权限捏")
    if arg == "ban":
        result = await files_writer(event.group_id, "off", ban_group)
    elif arg == "allow":
        result = await files_writer(event.group_id, "on", ban_group)
    elif arg == "allow_r18":
        result = await files_writer(event.group_id, "off", r18_group)
    elif arg == "ban_r18":
        result = await files_writer(event.group_id, "on", r18_group)
    else:
        await pixiv_r18.finish("参数错误捏\nban,allow,ban_r18,allow_r18")
    await pixiv_r18.finish(result)
