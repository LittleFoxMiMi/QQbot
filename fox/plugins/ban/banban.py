import re

ban_path = "./fox/data/ban/"


async def get_qq(msg):
    temp = re.search('\[CQ:at,qq=.*?]', msg)
    if not temp:
        return "err"
    qq = temp[0]
    qq = re.sub('\[CQ:at,qq=', '', qq)
    qq = re.sub(']', '', qq)
    return qq


async def get_time(msg):
    time = ""
    t = -1
    for num in msg:
        if num >= '0' and num <= '9':
            time += num
            continue
        if num == 's':
            t = int(time)
            break
        elif num == 'm':
            t = int(time)*60
            break
        elif num == 'h':
            t = int(time)*3600
            break
        elif num == 'd':
            t = int(time)*3600*24
            break
        else:
            return "err"
    if t == -1:
        return "err"
    else:
        return t
