from nonebot_plugin_apscheduler import scheduler
from nonebot import get_bot, on_command
from nonebot.adapters.onebot.v11 import MessageEvent

from .auth import yiban

user_id = "1216878448"

yiban_da = on_command('易班打卡', priority=1, block=True)


@yiban_da.handle()
async def _(event: MessageEvent):
    await yiban_da.send("执行手动打卡")
    try:
        result = await yiban()
    except Exception as e:
        result = str(type(e))
    await yiban_da.finish(result)


async def auto_yiban():
    try:
        result = await yiban()
    except Exception as e:
        result = str(type(e))
    await get_bot().send_private_msg(user_id=user_id, message=result)


scheduler.add_job(
    func=auto_yiban,
    trigger="cron",
    hour=6,
    minute=2,
    id="auto_yiban_morning",
    args=(),
    misfire_grace_time=30
)

scheduler.add_job(
    func=auto_yiban,
    trigger="cron",
    hour=12,
    minute=2,
    id="auto_yiban_noon",
    args=(),
    misfire_grace_time=30
)
