# https://github.com/he0119/CoolQBot/blob/master/src/plugins/roll/data.py
""" roll 点插件
NGA 风格 ROLL 点
掷骰子
"""
import re

from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import MessageEvent

from .NGARoll import *

# region roll
roll_cmd = on_command('roll', block=True, aliases={"Roll", "ROLL"})
roll_cmd.__doc__ = """
roll
NGA 风格 ROLL 点
roll 一次点数100
/roll d100
roll 两次点数100和两次点数50
/roll 2d100+2d50
"""


@roll_cmd.handle()
async def roll_handle_first_receive(bot: Bot, event: MessageEvent,
                                    state: T_State):
    args = str(event.message).strip()

    # 检查是否符合规则
    match = re.match(r'^([\dd+\s]+?)$', args)

    if args and match:
        state['input'] = args


@roll_cmd.args_parser
async def roll_args_parser(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()

    # 检查是否符合规则
    match = re.match(r'^([\dd+\s]+?)$', args)

    if not args:
        await roll_cmd.reject('ROLL点方式不能为空捏，请重新输入')

    if not match:
        await roll_cmd.reject('参数错误捏，请重新输入')

    state[state['_current_key']] = args


@roll_cmd.got(
    'input',
    prompt='欢迎使用 NGA 风格 ROLL 点插件\n请问你想怎么 ROLL 点\n你可以输入 d100\n也可以输入 2d100+2d50')
async def roll_handle(bot: Bot, event: MessageEvent, state: T_State):
    input_str = state['input']
    str_data = roll_dices(input_str)
    await roll_cmd.finish(str_data, at_sender=True)
