import aiofiles
import os
import ujson

data_adress = './fox/data/repeater_data/data.json'

async def mre(qun, msg):
    msg = str(msg)
    if msg.find(".jpg") != -1 or msg.find(".JPG") != -1:
        return 0
    mark = 0
    match = 0
    data = await data_load(data_adress)
    for i in data["data"]:
        if qun == i["group_id"]:
            match = 1
            if i["msg"] == msg:
                if i["times"] == 0:
                    i["times"] += 1
                    mark = 1
                    break
                elif i["times"] == 1:
                    break
            else:
                i["msg"] = msg
                i["times"] = 0
                break
    if match == 0:
        new_qun = dict(group_id=qun, msg=msg, times=0)
        data["data"].append(new_qun)
    print(await write_down(data))
    return mark


async def data_load(json_ad):
    async with aiofiles.open(json_ad, "r", encoding="utf-8")as f:
        text = await f.read()
        data = ujson.loads(text)
    return data


async def write_down(data):
    try:
        async with aiofiles.open(data_adress, "w") as f:
            text = ujson.dumps(data)
            await f.write(text)
    except Exception as e:
        return "文件写入错误！"
