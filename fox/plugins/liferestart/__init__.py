import random
import traceback
import re

from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent
from nonebot.typing import T_State
from .TalentManager import TalentManager
from .Life import Life

liferestart = on_command("liferestart", aliases={
                         "人生重开", "人生重开模拟器"}, priority=1, block=True)

Life.load("./fox/data/liferestarter")
life = Life()
talent_list = []
talent_point = 20


@liferestart.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = str(event.get_message()).strip().split(" ")
    if args is not None:
        if args[0] == "修仙":
            life.talent.talents.append(TalentManager.talentDict[1048])
            life.talent.talents.append(TalentManager.talentDict[1065])
            life.talent.talents.append(TalentManager.talentDict[1134])
        else:
            liferestart.finish("未知的参数")
    life.setErrorHandler(lambda e: traceback.print_exc())
    life.setTalentHandler(lambda ts: random.choice(ts).id)
    global talent_list
    talent_list = random.sample(
        range(1001, 1000+len(TalentManager.talentDict)), 10)
    talent_list_words = ""
    for i in range(10):
        talent_list_words += str(i)+"、" + \
            str(TalentManager.talentDict[talent_list[i]])+"\n"
    await liferestart.send(talent_list_words)


@liferestart.args_parser
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = str(event.get_message()).strip()
    if args == "cancel" or args == "取消":
        await liferestart.finish("operation canceled")


@liferestart.got("talent_choose", prompt="选择你的三个天赋,发送序号空格隔开")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    global talent_point
    choose = str(event.get_message()).strip().split(" ")
    if len(choose) != 3:
        await liferestart.reject("选择的天赋数量不正确！")
    if len(choose) != len(set(choose)):
        await liferestart.reject("参数重复！发送“取消”以终止本次游玩")
    for i in choose:
        try:
            if int(i) >= 0 and int(i) <= 9:
                life.talent.talents.append(
                    TalentManager.talentDict[talent_list[int(i)]])
                talent_point += int(
                    TalentManager.talentDict[talent_list[int(i)]].status)
            else:
                await liferestart.reject("出现了非法的参数！发送“取消”以终止本次游玩")
        except Exception as e:
            await liferestart.reject("出现了非法的参数！发送“取消”以终止本次游玩")
    talent_list_words = "已选择天赋:\n"
    for i in life.talent.talents:
        talent_list_words += str(i)+"\n"
    await liferestart.send(talent_list_words)
    #event["talent_choose"] = "done"


@liferestart.got("property_choose", prompt=f"选择天赋加点（颜智体钱基础{talent_point}点空格隔开）")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    global life
    global talent_list
    global talent_point
    choose = str(event.get_message()).strip().split(" ")
    if len(choose) != 4:
        await liferestart.reject("参数数量错误！发送“取消”以终止本次游玩")
    total = 0
    try:
        for i in choose:
            total += int(i)
        if total != talent_point:
            await liferestart.reject(f"天赋点总和不是{talent_point}！请重新输入！发送“取消”以终止本次游玩")
    except:
        await liferestart.reject("出现了非法的参数！发送“取消”以终止本次游玩")
    prop_list = {
        'CHR': choose[0],
        'INT': choose[1],
        'STR': choose[2],
        'MNY': choose[3]
    }
    life.setPropertyhandler(prop_list)
    life.setproperty(prop_list)
    # life.choose()
    msgall = []
    msg = ""
    count = 0
    head_old = ""
    for i in life.run():
        head = re.findall("/.*?】", i[0])[0]
        if head == head_old:
            msg += "\n"+re.findall("【.*?岁", i[0])[0]+"】"
        else:
            head_old = head
            msg += "\n"+i[0]+"\n"
        msg += f'{"——".join(i[1:])}'
        msgall.append(msg)
        msg = ""
    len_msg = len(msgall)-1
    for i in range(len_msg+1):
        count += 1
        msg += msgall[len_msg-i]
        if count >= 50:
            await liferestart.send(msg)
            count = 0
            msg = ""
    life = Life()
    talent_list = []
    talent_point = 20
    await liferestart.finish(msg)
