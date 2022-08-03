import random
import hashlib
import ujson
import urllib
import aiohttp


async def baidu_api(words, lang):
    appid = '20210223000705381'  # 你的appid
    secretKey = '8M_0WCXUuHuvZZw43GUN'  # 你的密钥
    myurl = '/api/trans/vip/translate'
    fromLang = 'auto'  # 原文语种
    toLang = lang  # 译文语种
    salt = random.randint(32768, 65536)
    q = words
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = "https://api.fanyi.baidu.com"+myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    async with aiohttp.ClientSession(
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"},
            timeout=aiohttp.ClientTimeout(total=8)) as session:
        async with session.get(str(myurl)) as resp:
            text = await resp.text()
            result = ujson.loads(text)
    result = result['trans_result'][0]['dst']
    return result
