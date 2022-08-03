from PIL import Image, ImageDraw
import random
import os
import re
import aiohttp
from io import BytesIO

# 爬的概率 越大越容易爬 取值区间 [0, 100]
creep_limit = 80

_avatar_size = 139
_center_pos = (17, 180)

# _toppest = 164
# _downest = 504

base_path = './fox/data/creep'


async def get_at_qq(msg):
    for segment in msg:
        if segment['type'] == 'at':
            return segment['data']['qq']
    return False


async def creep(qq):
    creeped_who = qq
    id = random.randint(0, 52)

    whetherToClimb = await randomClimb()

    if not whetherToClimb:
        return base_path + '/image/不爬.jpg'

    avatar_img_url = 'http://q1.qlogo.cn/g?b=qq&nk={QQ}&s=640'.format(
        QQ=creeped_who)
    res = await getAvatar(avatar_img_url)
    avatar = Image.open(BytesIO(res)).convert('RGBA')
    avatar = await get_circle_avatar(avatar, 100)

    creep_img = Image.open(f'{base_path}/image/pa/爬{id}.jpg').convert('RGBA')
    creep_img = creep_img.resize((500, 500), Image.ANTIALIAS)
    creep_img.paste(avatar, (0, 400, 100, 500), avatar)
    await checkFolder(base_path + '/image/avatar')
    creep_img.save(f'{base_path}/image/avatar/{creeped_who}_creeped.png')

    return base_path + f'/image/avatar/{creeped_who}_creeped.png'


async def get_circle_avatar(avatar, size):
    avatar.thumbnail((size, size))

    scale = 5
    mask = Image.new('L', (size*scale, size*scale), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size * scale, size * scale), fill=255)
    mask = mask.resize((size, size), Image.ANTIALIAS)

    ret_img = avatar.copy()
    ret_img.putalpha(mask)

    return ret_img


async def randomClimb():
    randomNumber = random.randint(1, 100)
    if randomNumber < creep_limit:
        return True
    return False

# Picture tool


async def pictureCqCode(relativePosition):
    relativePosition = relativePosition.strip('./')
    back = relativePosition[relativePosition.find('/'):]
    filePath = 'file://' + os.path.dirname(__file__) + back
    filePath = re.sub(r'/plugins/creep','',filePath)
    return '[CQ:image,file=' + filePath + ']'


async def asyncGet(url, headers='', timeout=10):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as res:
            img = await res.read()
    return img


async def getAvatar(url):
    img = await asyncGet(url)
    return img


async def checkFolder(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
