from littlepaimon_utils import aiorequests
import asyncio
import json
import base64
import time
import httpx
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
noon_content = "25%5B0%5D%5B0%5D%5Bname%5D=form%5B25%5D%5Bfield_1588750276_2934%5D%5B%5D&25%5B0%5D%5B0%5D%5Bvalue%5D=36.6&25%5B0%5D%5B1%5D%5Bname%5D=form%5B25%5D%5Bfield_1588750304_5363%5D%5B%5D&25%5B0%5D%5B1%5D%5Bvalue%5D=%E6%B5%99%E6%B1%9F%E7%9C%81+%E5%98%89%E5%85%B4%E5%B8%82+%E5%B9%B3%E6%B9%96%E5%B8%82+%E6%98%A5%E6%99%96%E8%B7%AF+500%E5%8F%B7+%E9%9D%A0%E8%BF%91%E5%B9%B3%E6%B9%96%E5%B8%82%E7%AC%AC%E4%B8%80%E4%BA%BA%E6%B0%91%E5%8C%BB%E9%99%A2+&25%5B0%5D%5B2%5D%5Bname%5D=form%5B25%5D%5Bfield_1588750323_2500%5D%5B%5D&25%5B0%5D%5B2%5D%5Bvalue%5D=%E6%98%AF&25%5B0%5D%5B3%5D%5Bname%5D=form%5B25%5D%5Bfield_1588750343_3510%5D%5B%5D&25%5B0%5D%5B3%5D%5Bvalue%5D=%E5%90%A6&25%5B0%5D%5B4%5D%5Bname%5D=form%5B25%5D%5Bfield_1588750363_5268%5D%5B%5D&25%5B0%5D%5B4%5D%5Bvalue%5D="
current_content = ""


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
    headers = {
        "Host": "f.yiban.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; LM-F100 Build/QKQ1.200719.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.69 Mobile Safari/537.36;webank/h5face;webank/1.0 yiban_android/5.0.12",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "authorization": "Bearer 7ddaad13f1d6c5ebd404c91b8d46be8a",
        "appversion": "5.0.12",
        "logintoken": "7ddaad13f1d6c5ebd404c91b8d46be8a",
        "signature": "UBfR234+qAy70MTcciL12lOYTvDDRZZbIhPXn9dU2THMiFDkOISmWaYEVi5DNXeK/v2F9TUvlzzGEtI5OKwQSw",
        "X-Requested-With": "com.yiban.app",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "loginToken=7ddaad13f1d6c5ebd404c91b8d46be8a; client=android; https_waf_cookie=ed07fcc4-a4f0-495daf19a294173d8b6a5435c0753fc89302; _YB_OPEN_V2_0=2lf0210P27PLou0h; yibanM_user_token=7ddaad13f1d6c5ebd404c91b8d46be8a",
    }
    req1 = await aiorequests.get("https://f.yiban.cn/iapp610661", headers=headers)
    print("易班登录认证1："+req1.status_code)
    if req1.status_code != 302:
        return 1
    req2 = await aiorequests.get(
        "https://f.yiban.cn/iapp/index?act=iapp610661", headers=headers)
    print("易班登录认证2："+req2.status_code)
    if req2.status_code != 302:
        return 1
    return 0


async def sust_auth():
    headers = {
        "Host": "yiban.sust.edu.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; LM-F100 Build/QKQ1.200719.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.69 Mobile Safari/537.36;webank/h5face;webank/1.0 yiban_android/5.0.12",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "X-Requested-With": "com.yiban.app",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "PHPSESSID=9a42777bd25bbc36364eb0ef9cc90171",
    }
    req = await aiorequests.get("http://yiban.sust.edu.cn/v4/yibanapi/?verify_request=e9412e43ceef2a1832f481fd316649ad4267daa3a39e74a00171597acaa0a19840f92336864cc39e6f54a6e3fe57459d9d8c30a535c44fbdabfdf7a17814565b0268ab6a2c5d9e929ba494b8e6e3c59b006d4ffbf33d242666adefbaa69d14e7dcdb494e14f4f533460c1b2dca1963b95eef89b4f01d1adf17c0e0b1a45c16bdf5ce47d212a0d02e3963cd44555a7f48fb44b70e6e73b433429f38b02aefdf333c5df6f0b861b09cc7699ae916939935de2eea0f3264a6de5af0560f5a211aef0281a079e638243f90e315c7e238155481f6f5dac46036233e696f2543a9e25c6529228b25c73161e2624bf51dc48c013dee910087c1e83ec17b2fbb51f263a25d4527a8a1f100dba5c5e42055258dba423b20c2efe647e23caad5c598a79e72b59fde8ee6b2832a1cb0a5293c724281&yb_uid=30780000", headers=headers, timeout=30)
    print("sust登录认证1："+req.status_code)
    if req.status_code != 302:
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
        "Cookie": "PHPSESSID=9a42777bd25bbc36364eb0ef9cc90171",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    req = await aiorequests.post(
        "http://yiban.sust.edu.cn/v4/public/index.php/admin/login/captcha.html", headers=headers, timeout=30)
    print("获取验证码："+req.status_code)
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
        "Cookie": "PHPSESSID=9a42777bd25bbc36364eb0ef9cc90171",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    req = await aiorequests.post(f"http://yiban.sust.edu.cn/v4/public/index.php/Index/formtime/add.html?desgin_id=25&list_id=12&verify={captcha_info['captcha_code']}&uniqid={captcha_info['captcha_id']}", headers=headers, data=current_content, timeout=30)
    print("提交表单："+req.status_code)
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


async def yiban():
    await time_set()
    if await auth():
        return ("易班验证失败！")
    for i in range(5):
        try:
            print(f"sust验证（{i}/5）")
            if await sust_auth():
                return ("sust验证失败")
            else:
                break
        except Exception as e:
            if isinstance(e, httpx.ReadTimeout):
                print("sust认证超时，正在重试。。。")
                continue
            return e
        continue
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
        continue
    for i in range(5):
        try:
            print(f"提交表单（{i}/5）")
            result = await post_form(captcha_info)
            if result == "验证码错误":
                continue
            return result
        except Exception as e:
            if isinstance(e, httpx.ReadTimeout):
                print("提交表单超时，正在重试。。。")
                continue
            return e
        continue


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(yiban())
