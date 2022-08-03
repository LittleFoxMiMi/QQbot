import execjs
import aiofiles

js_ad = "./fox/plugins/homohomo/homo.js"


async def js_load():
    async with aiofiles.open(js_ad, "r", encoding="utf-8")as f:
        text = await f.read()
    return text


async def homo_it(number):
    content=await js_load()
    js = execjs.compile(content)
    return js.call("homo", int(number))
