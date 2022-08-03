import re
import os
import ujson
import aiofiles
import random
import datetime


async def readJson(p):
    if not os.path.exists(p):
        return "err"
    async with aiofiles.open(p, 'r', encoding='utf-8') as f:
        content = await f.read()
    content = ujson.loads(content)
    return content


def getdate(beforeOfDay):
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=-beforeOfDay)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%m月%d日')
    return re_date


async def dog(name, nickname):
    path = "./fox/data/forfun/dog.json"
    content = await readJson(path)
    if content == "err":
        return content
    msg = random.choice(content["text"])
    msg = msg["content"]
    temp = re.sub('{name}', name, msg)
    return re.sub('{nickname}', nickname, temp)


async def dog_dairy(name, nickname):
    path = "./fox/data/forfun/dog_dairy.json"
    content = await readJson(path)
    if content == "err":
        return content
    msg = random.choice(content["text"])
    msg = msg["content"]
    msg = re.sub('{name}', name, msg)
    msg = re.sub('{nickname}', nickname, msg)
    date_list = []
    all_day = 21
    for i in range(all_day):
        date_list.append(getdate(all_day-i))
    for i in date_list:
        msg = re.sub('{date}', i, msg, count=1)
    return msg


async def love(name, nickname):
    path = "./fox/data/forfun/love.json"
    content = await readJson(path)
    if content == "err":
        return content
    msg = random.choice(content["text"])
    msg = msg["content"]
    temp = re.sub('{name}', name, msg)
    temp = re.sub('{nickname}', nickname, temp)
    return temp


async def dog_name_get(msg):
    doge = re.search('我想做.*?的狗|我好想做.*?的狗|我想当.*?的狗|我好想当.*?的狗', msg)
    if doge != None:
        name = doge[0]
        name = re.sub('我想做', '', name, count=1)
        name = re.sub('的狗', '', name, count=1)
        name = re.sub('我想当', '', name, count=1)
        name = re.sub('我好想当', '', name, count=1)
        name = re.sub('我好想做', '', name, count=1)
        return name
    else:
        return ""
