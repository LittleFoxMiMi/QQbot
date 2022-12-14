import functools
from json import JSONDecodeError
import re
from nonebot import get_bot, logger
from nonebot.adapters.onebot.v11 import ActionFailed
from nonebot.exception import FinishedException

# 异常处理装饰器


def exception_handler():
    def wrapper(func):

        @functools.wraps(func)
        async def wrapped(**kwargs):
            event = kwargs['event']
            try:
                await func(**kwargs)
            except FinishedException:
                raise
            except ActionFailed:
                logger.exception('账号可能被风控，消息发送失败')
                await get_bot().send(event, f'派蒙可能被风控，也可能是没有该图片资源，消息发送失败')
            except JSONDecodeError:
                await get_bot().send(event, '派蒙获取信息失败，重试一下吧')
            # except IndexError or KeyError as e:
            #     await get_bot().send(event, f'派蒙获取信息失败，请确认参数无误，{e}')
            # except TypeError or AttributeError as e:
            #     await get_bot().send(event, f'派蒙好像没有该UID的绑定信息， {e}')
            except FileNotFoundError as e:
                file_name = re.search(r'\'(.*)\'', str(e)).group(1)
                file_name = file_name.replace('\\\\', '/').split('/')
                file_name = file_name[-2] + '\\' + file_name[-1]
                await get_bot().send(event, f"派蒙缺少{file_name}资源，请联系开发者补充")
            except Exception as e:
                await get_bot().send(event, f'派蒙好像出了点问题，{e}')

        return wrapped

    return wrapper
