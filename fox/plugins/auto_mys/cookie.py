import hashlib
import json
import random
import re
import string
from time import time
from littlepaimon_utils import aiorequests
from nonebot import logger

from .db_util import delete_cookie_cache, get_private_cookie, limit_public_cookie, update_cookie_cache
from .message_util import send_cookie_delete_msg


async def get_bind_game(cookie):
    finduid = re.search(r'account_id=(\d{6,12})', cookie)
    if not finduid:
        finduid = re.search(r'ltuid=(\d{6,12})', cookie)
        if not finduid:
            return None, None
    uid = finduid.group(1)
    url = 'https://api-takumi-record.mihoyo.com/game_record/card/wapi/getGameRecordCard'
    headers = get_headers(q=f'uid={uid}', cookie=cookie)
    params = {
        "uid": uid
    }
    resp = await aiorequests.get(url=url, headers=headers, params=params)
    data = resp.json()
    return data, uid


# 获取签到奖励列表
async def get_sign_list():
    url = 'https://api-takumi.mihoyo.com/event/bbs_sign_reward/home'
    headers = {
        'x-rpc-app_version': '2.11.1',
        'User-Agent':        'Mozilla/5.0 (Linux; Android 10; LM-F100 Build/QKQ1.200719.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/106.0.5249.79 Mobile Safari/537.36 miHoYoBBS/2.34.2',
        'x-rpc-client_type': '5',
        'Referer':           'https://webstatic.mihoyo.com/'
    }
    params = {
        'act_id': 'e202009291139501'
    }
    resp = await aiorequests.get(url=url, headers=headers, params=params)
    data = resp.json()
    return data

# 获取今日签到信息


async def get_sign_info(uid):
    server_id = "cn_qd01" if uid[0] == '5' else "cn_gf01"
    url = 'https://api-takumi.mihoyo.com/event/bbs_sign_reward/info'
    cookie = await get_own_cookie(uid, action='查询米游社签到')
    if not cookie:
        return f'你的uid{uid}没有绑定对应的cookie,使用ysb绑定才能用米游社签到哦!'
    headers = {
        'x-rpc-app_version': '2.11.1',
        'x-rpc-client_type': '5',
        'Origin':            'https://webstatic.mihoyo.com',
        'Referer':           'https://webstatic.mihoyo.com/',
        'Cookie':            cookie['cookie'],
        'User-Agent':        'Mozilla/5.0 (Linux; Android 10; LM-F100 Build/QKQ1.200719.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/106.0.5249.79 Mobile Safari/537.36 miHoYoBBS/2.34.2',
    }
    params = {
        'act_id': 'e202009291139501',
        'region': server_id,
        'uid':    uid
    }
    resp = await aiorequests.get(url=url, headers=headers, params=params)
    data = resp.json()
    if await check_retcode(data, cookie, uid):
        return data
    else:
        return f'你的uid{uid}的cookie已过期,需要重新绑定哦!'

# 执行签到操作


async def sign(uid):
    server_id = "cn_qd01" if uid[0] == '5' else "cn_gf01"
    url = 'https://api-takumi.mihoyo.com/event/bbs_sign_reward/sign'
    cookie = await get_own_cookie(uid, action='米游社签到')
    if not cookie:
        return f'你的uid{uid}没有绑定对应的cookie,使用ysb绑定才能用米游社签到哦!'
    headers = get_sign_headers(cookie['cookie'])
    json_data = {
        'act_id': 'e202009291139501',
        'uid':    uid,
        'region': server_id
    }
    for i in range(2):
        logger.info(f"---UID{uid}的签到尝试第{i}次，共3次---")
        resp = await aiorequests.post(url=url, headers=headers, json=json_data)
        if resp.status_code == 429:
            time.sleep(10)  # 429同ip请求次数过多，尝试sleep10s进行解决
            logger.warning(f'429 Too Many Requests ，即将进入下一次请求')
            continue
        data = resp.json()
        if i == 2:
            logger.info(f"UID{uid}的原神签到失败了！")
            return f'你的uid{uid}的米游社签到失败，原因是遭遇验证码捏。'
        if data["retcode"] == 0 and data["data"]["success"] == 1:
            logger.info("侦测到验证码")
            validate = await get_validate(data["data"]["gt"], data["data"]["challenge"])
            if validate != "":
                headers["x-rpc-challenge"] = data["data"]["challenge"]
                headers["x-rpc-validate"] = validate
                headers["x-rpc-seccode"] = f'{validate}|jordan'
            time.sleep(random.randint(6, 15))
        else:
            break
    logger.info(f'---UID{uid}的签到状态码为{data["retcode"]}，结果为{data["message"]}---')
    if await check_retcode(data, cookie, uid):
        return data
    else:
        return f'你的uid{uid}的cookie已过期,需要重新绑定哦!'


async def get_validate(gt, challenge):
    header = {
        "Accept": "*/*",
        "X-Requested-With": "com.mihoyo.hyperion",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; LM-F100 Build/QKQ1.200719.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/106.0.5249.79 Mobile Safari/537.36 miHoYoBBS/2.34.2",
        "Referer": "https://webstatic.mihoyo.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    validate = ""
    req = await aiorequests.get(
        f"https://api.geetest.com/ajax.php?gt={gt}&challenge={challenge}&lang=zh-cn&pt=3&client_type=web_mobile",
        headers=header)
    print(req.text)
    if req.status_code == 200:
        data = json.loads(req.text.replace("(", "").replace(")", ""))
        if "success" in data["status"] and "success" in data["data"]["result"]:
            validate = data["data"]["validate"]
    return validate


def get_sign_headers(cookie):
    headers = {
        'User_Agent':        'Mozilla/5.0 (Linux; Android 10; MIX 2 Build/QKQ1.190825.002; wv) AppleWebKit/537.36 ('
                             'KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Mobile Safari/537.36 '
                             'miHoYoBBS/2.34.1',
        'Cookie':            cookie,
        'x-rpc-device_id':   random_hex(32),
        'Origin':            'https://webstatic.mihoyo.com',
        'X_Requested_With':  'com.mihoyo.hyperion',
        'DS':                get_old_version_ds(mhy_bbs=True),
        'x-rpc-client_type': '5',
        'Referer':           'https://webstatic.mihoyo.com/bbs/event/signin-ys/index.html?bbs_auth_required=true&act_id=e202009291139501&utm_source=bbs&utm_medium=mys&utm_campaign=icon',
        'x-rpc-app_version': '2.34.1'
    }
    return headers


def get_old_version_ds(mhy_bbs: bool = False) -> str:
    """
    生成米游社旧版本headers的ds_token
    """
    if mhy_bbs:
        s = '9nQiU3AV0rJSIBWgdynfoGMGKaklfbM7'
    else:
        s = 'z8DRIUjNDT7IT5IZXvrUAxyupA1peND9'
    t = str(int(time()))
    r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
    c = md5(f"salt={s}&t={t}&r={r}")
    return f"{t},{r},{c}"

# 米游社爬虫headers


def get_headers(cookie, q='', b=None):
    headers = {
        'DS':                get_ds(q, b),
        'Origin':            'https://webstatic.mihoyo.com',
        'Cookie':            cookie,
        'x-rpc-app_version': "2.11.1",
        'User-Agent':        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS '
                             'X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.11.1',
        'x-rpc-client_type': '5',
        'Referer':           'https://webstatic.mihoyo.com/'
    }
    return headers


def get_ds(q: str = '', b: dict = None, mhy_bbs_sign: bool = False) -> str:
    """
    生成米游社headers的ds_token
    :param q: 查询
    :param b: 请求体
    :param mhy_bbs_sign: 是否为米游社讨论区签到
    :return: ds_token
    """
    br = json.dumps(b) if b else ''
    if mhy_bbs_sign:
        s = 't0qEgfub6cvueAPgR5m9aQWWVciEer7v'
    else:
        s = 'xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs'
    t = str(int(time()))
    r = str(random.randint(100000, 200000))
    c = md5(f'salt={s}&t={t}&r={r}&b={br}&q={q}')
    return f'{t},{r},{c}'

# md5加密


def md5(text: str) -> str:
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


def random_text(length: int) -> str:
    """
    生成指定长度的随机字符串
    :param length: 长度
    :return: 随机字符串
    """
    return ''.join(random.sample(string.ascii_lowercase + string.digits, length))

# 生成随机字符串


def random_hex(length):
    result = hex(random.randint(0, 16 ** length)).replace('0x', '').upper()
    if len(result) < length:
        result = '0' * (length - len(result)) + result
    return result


# 检查cookie是否有效，通过查看个人主页来判断
async def check_cookie(cookie):
    url = 'https://bbs-api.mihoyo.com/user/wapi/getUserFullInfo?gids=2'
    headers = {
        'DS':                get_ds(),
        'Origin':            'https://webstatic.mihoyo.com',
        'Cookie':            cookie,
        'x-rpc-app_version': "2.11.1",
        'x-rpc-client_type': '5',
        'Referer':           'https://webstatic.mihoyo.com/'
    }
    res = await aiorequests.get(url=url, headers=headers)
    res = res.json()
    if res['retcode'] != 0:
        return False
    else:
        return True

# 获取可用的私人cookie


async def get_own_cookie(uid='', mys_id='', action=''):
    if uid:
        cookie = (await get_private_cookie(uid, 'uid'))
    elif mys_id:
        cookie = (await get_private_cookie(mys_id, 'mys_id'))
    else:
        cookie = None
    if not cookie:
        return None
    else:
        cookie = cookie[0]
        logger.info(
            f'---派蒙调用用户{cookie[0]}的uid{cookie[2]}私人cookie执行{action}操作---')
        return {'type': 'private', 'user_id': cookie[0], 'cookie': cookie[1], 'uid': cookie[2], 'mys_id': cookie[3]}


# 检查数据返回状态，10001为ck过期了，10101为达到每日30次上线了
async def check_retcode(data, cookie, uid):
    if data['retcode'] == 10001 or data['retcode'] == -100:
        await delete_cookie_cache(cookie['cookie'], cookie['type'])
        await send_cookie_delete_msg(cookie)
        return False
    elif data['retcode'] == 10101:
        if cookie['type'] == 'public':
            logger.info(f'{cookie["no"]}号公共cookie达到了每日30次查询上限')
            await limit_public_cookie(cookie['cookie'])
            await delete_cookie_cache(cookie['cookie'], key='cookie')
        elif cookie['type'] == 'private':
            logger.info(
                f'用户{cookie["user_id"]}的uid{cookie["uid"]}私人cookie达到了每日30次查询上限')
            return '私人cookie达到了每日30次查询上限'
        return False
    else:
        await update_cookie_cache(cookie['cookie'], uid, 'uid')
        return True

# 添加stoken


async def addStoken(stoken, uid):
    login_ticket = re.search(r'login_ticket=([0-9a-zA-Z]+)', stoken)
    if login_ticket:
        login_ticket = login_ticket.group(0).split('=')[1]
    else:
        return None, None, None, '你的cookie中没有login_ticket字段哦，请重新获取'
    ck = await get_private_cookie(uid, key='uid')
    if not ck:
        return None, None, None, '你还没绑定私人cookie哦，请先用ysb绑定吧'
    ck = ck[0][1]
    mys_id = re.search(r'account_id=(\d*)', ck)
    if mys_id:
        mys_id = mys_id.group(0).split('=')[1]
    else:
        return None, None, None, '你的cookie中没有account_id字段哦，请重新获取'
    raw_data = await get_stoken_by_login_ticket(login_ticket, mys_id)
    try:
        stoken = raw_data['data']['list'][0]['token']
    except TypeError:
        return None, None, None, '该stoken无效获取过期了，请重新获取'
    s_cookies = 'stuid={};stoken={}'.format(mys_id, stoken)
    return s_cookies, mys_id, raw_data, 'OK'


async def get_stoken_by_login_ticket(loginticket, mys_id):
    req = await aiorequests.get(url='https://api-takumi.mihoyo.com/auth/api/getMultiTokenByLoginTicket',
                                params={
                                    'login_ticket': loginticket,
                                    'token_types':  '3',
                                    'uid':          mys_id
                                })
    return req.json()
