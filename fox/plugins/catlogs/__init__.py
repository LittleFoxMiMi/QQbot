from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot.typing import T_State
from fox.check import qq_check
from .showlogs import read_last_line

super_user = "./fox/data/config/superuser.txt"
bot_log_path = "/www/server/panel/plugin/supervisor/log"
cq_log_path = "/home/qqbot/logs"

catlogs = on_command("catlogs", aliases={"showlogs"}, priority=1, block=True)


@catlogs.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = str(event.get_message()).strip()
    if not await qq_check(event.get_user_id(), super_user):
        catlogs.finish("你没有权限捏")
    if args != "":
        try:
            line = int(args)
        except:
            await catlogs.finish("参数错误！")
    else:
        line = 5
    cq_log = await read_last_line(cq_log_path, line)
    bot_log = await read_last_line(bot_log_path, line)
    await catlogs.send(cq_log)
    await catlogs.finish(bot_log)
