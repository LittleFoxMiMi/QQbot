from .huoZiYinShua import huoZiYinShua
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot.typing import T_State

path = "./fox/plugins/otto"
wav_path = "./fox/data/otto"

otto = on_command("otto", aliases={"电棍"}, priority=1, block=True)


@otto.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = str(event.get_message()).strip()
    if args == "":
        words = "欧内的手好汉"
    else:
        words = args
    await get_audio(words)
    await bot.call_api(api="send_group_msg", group_id=event.group_id, message="[CQ:record,file=file:///home/qqbot/fox/data/otto/Output.wav]")


async def get_audio(words):
    HZYS = huoZiYinShua(path+"/sources/", path+"/dictionary.csv")
    HZYS.export(words, wav_path+"/Output.wav")
