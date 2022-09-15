from littlepaimon_utils import aiorequests
import asyncio
import json
import base64
import aiofiles
import ujson
import time
import httpx
#from yiban import Yiban as YB
from .ddddocr import DdddOcr

ocr = DdddOcr()

path = "./fox/data/auto_yiban/"
morning_key = "YDS2TEB8SppLt40SvtJhdy6DU__ygPczBahLcCSrpLcIOI36WqfnBAcSexv_vGtfgfHs==UaMkVOlI5lDd3SQXt6Wkh==DRyhENrXujBjpy8G7L6_jmU7lZYQXO0hZYxCK1KrhTkoVTq6KSslmicuHqdaPb9ZAgEh_IcpCWBXGXjw="
noon_key = "btkWjauvkXGUjfWzImC39IBfNk7cOBJ3ned91IBzwwn_ftUgv6fzNgV_lbTmwRKvrvIVsguEuS0RxAqUMthJRcIgv55v9Dry60WAp4yrPOA7Pbhw4X9hHULmi1ETm9it==mW_met31KPM3Gzdjtvwuxd3_ivL==39GJEuhPfGzJUQ="
current_key = ""
morning_design = "24"
noon_design = "25"
current_design = ""
morning_content = "24%5B0%5D%5B0%5D%5Bname%5D=form%5B24%5D%5Bfield_1588749561_2922%5D%5B%5D&24%5B0%5D%5B0%5D%5Bvalue%5D=36.5&24%5B0%5D%5B1%5D%5Bname%5D=form%5B24%5D%5Bfield_1588749738_1026%5D%5B%5D&24%5B0%5D%5B1%5D%5Bvalue%5D=%E6%B5%99%E6%B1%9F%E7%9C%81+%E5%98%89%E5%85%B4%E5%B8%82+%E5%B9%B3%E6%B9%96%E5%B8%82+%E6%9D%BE%E6%9E%AB%E6%B8%AF%E8%B7%AF+616%E5%8F%B7+%E9%9D%A0%E8%BF%91%E4%B9%9D%E9%BE%99%E8%8A%B1%E8%8B%91+&24%5B0%5D%5B2%5D%5Bname%5D=form%5B24%5D%5Bfield_1588749759_6865%5D%5B%5D&24%5B0%5D%5B2%5D%5Bvalue%5D=%E6%98%AF&24%5B0%5D%5B3%5D%5Bname%5D=form%5B24%5D%5Bfield_1588749842_2715%5D%5B%5D&24%5B0%5D%5B3%5D%5Bvalue%5D=%E5%90%A6&24%5B0%5D%5B4%5D%5Bname%5D=form%5B24%5D%5Bfield_1588749886_2103%5D%5B%5D&24%5B0%5D%5B4%5D%5Bvalue%5D="
noon_content = "25%5B0%5D%5B0%5D%5Bname%5D=form%5B25%5D%5Bfield_1588750276_2934%5D%5B%5D&25%5B0%5D%5B0%5D%5Bvalue%5D=36.6&25%5B0%5D%5B1%5D%5Bname%5D=form%5B25%5D%5Bfield_1588750304_5363%5D%5B%5D&25%5B0%5D%5B1%5D%5Bvalue%5D=%E6%B5%99%E6%B1%9F%E7%9C%81+%E5%98%89%E5%85%B4%E5%B8%82+%E5%B9%B3%E6%B9%96%E5%B8%82+%E6%9D%BE%E6%9E%AB%E6%B8%AF%E8%B7%AF+616%E5%8F%B7+%E9%9D%A0%E8%BF%91%E4%B9%9D%E9%BE%99%E8%8A%B1%E8%8B%91+&25%5B0%5D%5B2%5D%5Bname%5D=form%5B25%5D%5Bfield_1588750323_2500%5D%5B%5D&25%5B0%5D%5B2%5D%5Bvalue%5D=%E6%98%AF&25%5B0%5D%5B3%5D%5Bname%5D=form%5B25%5D%5Bfield_1588750343_3510%5D%5B%5D&25%5B0%5D%5B3%5D%5Bvalue%5D=%E5%90%A6&25%5B0%5D%5B4%5D%5Bname%5D=form%5B25%5D%5Bfield_1588750363_5268%5D%5B%5D&25%5B0%5D%5B4%5D%5Bvalue%5D="
current_content = ""
yiban_token = ""


async def time_set():
    global current_key
    global current_design
    global current_content
    now_localtime = time.strftime("%H:%M:%S", time.localtime())
    if "06:00:00" < now_localtime < "10:00:00":
        current_key = morning_key
        current_design = morning_design
        current_content = morning_content
    else:
        current_key = noon_key
        current_design = noon_design
        current_content = noon_content


async def auth():
    headers1 = {
        "Host": "f.yiban.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; LM-F100 Build/QKQ1.200719.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.69 Mobile Safari/537.36;webank/h5face;webank/1.0 yiban_android/5.0.12",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "authorization": f"Bearer {yiban_token}",
        "appversion": "5.0.12",
        "logintoken": yiban_token,
        "X-Requested-With": "com.yiban.app",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": f"loginToken={yiban_token}; client=android",
    }
    req1 = await aiorequests.get("https://f.yiban.cn/iapp610661", headers=headers1)
    print("易班登录认证1："+str(req1.status_code))
    if req1.status_code != 302:
        return "1"
    cookie1 = str(req1.cookies).split(" ")[1]
    headers2 = {
        "Host": "f.yiban.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; LM-F100 Build/QKQ1.200719.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.69 Mobile Safari/537.36;webank/h5face;webank/1.0 yiban_android/5.0.12",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "authorization": f"Bearer {yiban_token}",
        "appversion": "5.0.12",
        "logintoken": yiban_token,
        "X-Requested-With": "com.yiban.app",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": f"loginToken={yiban_token}; client=android; {cookie1}",
    }
    req2 = await aiorequests.get(
        "https://f.yiban.cn/iapp/index?act=iapp610661", headers=headers2)
    print("易班登录认证2："+str(req2.status_code))
    if req2.status_code != 302:
        return "1"
    return req2.headers.get("location")


async def sust_auth1(location):
    headers = {
        "Host": "yiban.sust.edu.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; LM-F100 Build/QKQ1.200719.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.69 Mobile Safari/537.36;webank/h5face;webank/1.0 yiban_android/5.0.12",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "X-Requested-With": "com.yiban.app",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": f"PHPSESSID={yiban_token}",
    }
    req = await aiorequests.get(location, headers=headers, timeout=30)
    print("sust登录认证1："+str(req.status_code))
    if req.status_code != 302:
        return "1"
    return req.headers.get("location")


async def sust_auth2(location):
    headers = {
        "Host": "yiban.sust.edu.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; LM-F100 Build/QKQ1.200719.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.69 Mobile Safari/537.36;webank/h5face;webank/1.0 yiban_android/5.0.12",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "X-Requested-With": "com.yiban.app",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": f"PHPSESSID={yiban_token}",
    }
    location = "http://yiban.sust.edu.cn/v4"+location[2:]
    req = await aiorequests.get(location, headers=headers, timeout=30)
    print("sust登录认证2："+str(req.status_code))
    if req.status_code != 200:
        return 1
    return 0


async def get_img():
    headers = {
        "Accept": "*/*",
        "Content-Length": "0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"http://yiban.sust.edu.cn/v4/public/index.php/index/formtime/form.html?desgin_id={current_design}&list_id=12&key={current_key}",
        "Host": "yiban.sust.edu.cn",
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip,deflate',
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; LM-F100 Build/QKQ1.200719.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.69 Mobile Safari/537.36;webank/h5face;webank/1.0 yiban_android/5.0.12",
        "Cookie": f"PHPSESSID={yiban_token}",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    req = await aiorequests.post(
        "http://yiban.sust.edu.cn/v4/public/index.php/admin/login/captcha.html", headers=headers, timeout=30)
    print("获取验证码："+str(req.status_code))
    data = json.loads(req.text)
    img = data["data"]["image"]
    captcha_id = data["data"]["uniqid"]
    await base64_to_img(img[22:], "img")
    captcha_code = await ddocr("img.png")
    return {
        "captcha_id": captcha_id,
        "captcha_code": captcha_code,
    }


async def post_form(captcha_info):
    headers = {
        "Accept": "*/*",
        "Origin": "http://yiban.sust.edu.cn",
        "Content-Length": str(len(current_content)),
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"http://yiban.sust.edu.cn/v4/public/index.php/index/formtime/form.html?desgin_id={current_design}&list_id=12&key={current_key}",
        "Host": "yiban.sust.edu.cn",
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip,deflate',
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; LM-F100 Build/QKQ1.200719.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.69 Mobile Safari/537.36;webank/h5face;webank/1.0 yiban_android/5.0.12",
        "Cookie": f"PHPSESSID={yiban_token}",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    req = await aiorequests.post(f"http://yiban.sust.edu.cn/v4/public/index.php/Index/formtime/add.html?desgin_id={current_design}&list_id=12&verify={captcha_info['captcha_code']}&uniqid={captcha_info['captcha_id']}", headers=headers, data=current_content, timeout=30)
    print("提交表单："+str(req.status_code))
    if req.status_code == 302:
        return "提交表单302错误"
    data = json.loads(req.text)
    print(data)
    return data["msg"]


async def base64_to_img(base64_str, file_name):
    with open(path+f'{file_name}.png', 'wb') as file:
        jiema = base64.b64decode(base64_str)  # 解码
        file.write(jiema)  # 将解码得到的数据写入到图片中


async def ddocr(file_name):
    with open(path+file_name, 'rb') as f:
        image = f.read()
    res = ocr.classification(image)
    return res


async def get_captcha():
    for i in range(5):
        try:
            print(f"获取验证码（{i}/5）")
            captcha_info = await get_img()
            break
        except Exception as e:
            if isinstance(e, httpx.ReadTimeout):
                print("验证码超时，正在重试。。。")
                continue
            return e
    return captcha_info


async def yiban():
    global yiban_token
    user = await data_load(path+"user_info.json")
    if not user:
        return ("文件读取错误")
    yiban_token = user["user_token"]
    await time_set()
    location = await auth()
    if location == "1":
        # print("易班验证失败！尝试重新登录")
        #yb = YB(user["phone_number"], user["password"])
        #yiban_token = yb.get_user_access_token()
        # location = await auth()
        if location == "1":
            return ("易班验证失败！")
        #user["user_token"] = yiban_token
        # await write_down(path+"user_info.json", user)
    for i in range(5):
        try:
            print(f"sust验证1（{i}/5）")
            sust_location = await sust_auth1(location)
            if sust_location == "1":
                return ("sust验证1失败")
            else:
                break
        except Exception as e:
            if isinstance(e, httpx.ReadTimeout):
                print("sust认证1超时，正在重试。。。")
                continue
            return e
    for i in range(5):
        try:
            print(f"sust验证2（{i}/5）")
            if await sust_auth2(sust_location):
                return ("sust验证2失败")
            else:
                break
        except Exception as e:
            if isinstance(e, httpx.ReadTimeout):
                print("sust认证2超时，正在重试。。。")
                continue
            return e
    captcha_info = await get_captcha()
    for i in range(8):
        try:
            print(f"提交表单（{i}/8）")
            result = await post_form(captcha_info)
            if result == "验证码错误":
                captcha_info = await get_captcha()
                i = 0
                continue
            if result == "SU":
                continue
            return result
        except Exception as e:
            if isinstance(e, httpx.ReadTimeout):
                print("提交表单超时，正在重试。。。")
                continue
            return e


async def data_load(json_ad):
    try:
        async with aiofiles.open(json_ad, "r", encoding="utf-8")as f:
            text = await f.read()
            data = ujson.loads(text)
        return data
    except:
        print("文件读取错误！")


async def write_down(json_ad, data):
    try:
        async with aiofiles.open(json_ad, "w") as f:
            text = ujson.dumps(data)
            await f.write(text)
        print("token已更新")
    except Exception as e:
        print("文件写入错误！")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(yiban())
