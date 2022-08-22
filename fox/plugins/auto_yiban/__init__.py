from ast import arg
from email import message
from nonebot_plugin_apscheduler import scheduler
from nonebot import get_bot

from .auth import yiban

user_id = "1216878448"


async def auto_yiban():
    try:
        result = await yiban()
    except Exception as e:
        result = str(type(e))
    await get_bot().send_private_msg(user_id, message=result)


scheduler.add_job(
    func=auto_yiban,
    trigger="cron",
    hour=6,
    id="auto_yiban_morning",
    args=(),
    misfire_grace_time=30
)

scheduler.add_job(
    func=auto_yiban,
    trigger="cron",
    hour=12,
    id="auto_yiban_noon",
    args=(),
    misfire_grace_time=30
)
