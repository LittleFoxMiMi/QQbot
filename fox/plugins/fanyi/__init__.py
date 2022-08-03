from nonebot.typing import T_State
from .fanyi_source import *
from nonebot.plugin import on_command
from nonebot.adapters.cqhttp.event import Event
from nonebot.adapters import Bot
import re


fanyi = on_command("翻译", block=True)


@fanyi.handle()
async def fanyi_p(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    ag = args.split(" ")
    if len(ag) < 2:
        await fanyi.finish("参数错误捏\n本命令的参数为：\n翻译 [次数] [原文]")
    try:
        t = int(re.sub("次", "", ag[0]))/3+1
    except Exception as e:
        await fanyi.finish("参数错误捏\n本命令的参数为：\n翻译 [次数] [原文]")
    s_msg = ag[1]
    if s_msg == "":
        await fanyi.finish("内容为空！")
    if t > 17:
        await fanyi.finish("你想把服务器卡死啊kora！！")
    else:
        await fanyi.send("正在翻译...")
        try:
            for i in range(int(t)):
                s_msg = await baidu_api(s_msg, 'jp')
                s_msg = await baidu_api(s_msg, 'en')
                s_msg = await baidu_api(s_msg, 'zh')
        except Exception as e:
            await fanyi.finish("Net Err!")
        await fanyi.finish(s_msg)
