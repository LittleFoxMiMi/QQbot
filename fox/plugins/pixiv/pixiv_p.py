import ujson
import re
from PIL import Image
import aiohttp
import aiofiles


async def lolicon_api(r18, tag):
    myurl = '?tag=' + tag + '&r18=' + str(r18)
    try:
        async with aiohttp.ClientSession(
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"},
                timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get("https://api.lolicon.app/setu/v2"+myurl) as resp:
                temp = await resp.text()
                result = ujson.loads(temp)
        if str(result)=="{'error': '', 'data': []}":
            return "没有找到该tag捏"
        return [result['data'][0]['urls']['original'], result['data'][0]['pid']]
    except Exception as e:
        return result


async def download_pic(url, pid):
    url = re.sub("i.pixiv.re", "i.pximg.net", url)
    print(url)
    try:
        async with aiohttp.ClientSession(
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36", "referer": "https://www.pixiv.net/member_illust.php?mode=medium&illust_id="+str(pid)},
                timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(url) as resp:
                img = await resp.read()
    except Exception as e:
        return "err"
    f_type = re.findall(r'[^\.]\w*$', url)[0]
    file_name = f"_tt.{f_type}"
    async with aiofiles.open('./fox/data/pixiv/image/'+file_name, "wb") as f:
        await f.write(img)
    temp = Image.open(r'./fox/data/pixiv/image/'+file_name)
    temp = temp.convert('RGB')
    temp.rotate(180).save(r'./fox/data/pixiv/image/_tt.jpg', quality=95)
