from asyncio import sleep
import contextlib
import random
import re
from collections import defaultdict

from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import MessageEvent, Message, Bot, MessageSegment
from nonebot import on_command, logger, get_bot
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot_plugin_apscheduler import scheduler

from .get_coin import MihoyoBBSCoin
from .exception_handler import exception_handler
from .db_util import add_auto_sign, add_coin_auto_sign, delete_auto_sign, delete_coin_auto_sign, delete_cookie_cache, delete_private_cookie, get_auto_sign, get_coin_auto_sign, get_private_cookie, get_private_stoken, insert_public_cookie, update_last_query, update_private_cookie, update_private_stoken
from .message_util import get_uid_in_msg, transform_uid
from .message_util import MessageBuild as MsgBd
from .cookie import addStoken, check_cookie, get_bind_game, get_sign_info, get_sign_list, sign

ys_help = on_command(
    'ys_help', aliases={'原神帮助'}, priority=1, block=True)

ysb = on_command('ysb', aliases={'原神绑定', '绑定cookie'}, priority=1, block=True)
ysb.__paimon_help__ = {
    "usage":     "ysb<cookie>",
    "introduce": "绑定私人cookie以开启更多功能",
    "priority":  1
}
ysbjc = on_command('ysbjc', aliases={
                   '原神绑定检查', '检查cookie绑定状态'}, priority=1, block=True)
ysbjc.__paimon_help__ = {
    "usage":     "ysbjc(uid)",
    "introduce": "检查私人cookie绑定状态，可检查指定的uid是否绑定cookie",
    "priority":  1
}
mys_sign = on_command('mys_sign', aliases={
                      'mys签到', '米游社签到'}, priority=1, block=True)
mys_sign_auto = on_command('mys_sign_auto', aliases={
                           'mys自动签到', '米游社自动签到'}, priority=1, block=True)
mys_sign_auto.__paimon_help__ = {
    "usage":     "mys自动签到<on|off uid>",
    "introduce": "*米游社原神区自动签到奖励获取",
    "priority":  1
}
mys_sign_all = on_command('mys_sign_all', aliases={
                          '全部重签'}, priority=1, permission=SUPERUSER, rule=to_me(), block=True)
add_public_ck = on_command('add_ck', aliases={
    '添加公共cookie', '添加公共ck'}, permission=SUPERUSER, priority=1, block=True)
delete_ck = on_command('delete_ck', aliases={
                       '删除ck', '删除cookie'}, priority=1, block=True)
get_mys_coin = on_command(
    'myb获取', aliases={'米游币获取', '获取米游币'}, priority=1, block=True)
get_mys_coin_auto = on_command(
    'myb自动获取', aliases={'米游币自动获取', '自动获取米游币'}, priority=1, block=True)
get_mys_coin_auto.__paimon_help__ = {
    "usage":     "myb自动获取<on|off uid>",
    "introduce": "自动获取米游币",
    "priority":  1
}
add_stoken = on_command('添加stoken', priority=1, block=True)
add_stoken.__paimon_help__ = {
    "usage":     "添加stoken[stoken]",
    "introduce": "添加stoken以获取米游币",
    "priority":  1
}

cookie_error_msg = '这个cookie无效哦，请旅行者确认是否正确\n获取cookie的教程：\ndocs.qq.com/doc/DQ3JLWk1vQVllZ2Z1\n'


@ysb.handle()
@exception_handler()
async def ysb_handler(event: MessageEvent, msg: Message = CommandArg()):
    cookie = msg.extract_plain_text().strip()
    if cookie == '':
        res = '获取cookie的教程：\ndocs.qq.com/doc/DQ3JLWk1vQVllZ2Z1\n获取到后，添加派蒙好友私聊发送ysb接复制到的cookie就行啦~'
        await ysb.finish(res, at_sender=True)
    else:
        cookie_info, mys_id = await get_bind_game(cookie)
        if not cookie_info or cookie_info['retcode'] != 0:
            msg = cookie_error_msg
            if event.message_type != 'private':
                msg += '\n当前是在群聊里绑定，建议旅行者添加派蒙好友私聊绑定!'
            await ysb.finish(msg, at_sender=True)
        else:
            uid = nickname = None
            for data in cookie_info['data']['list']:
                if data['game_id'] == 2:
                    uid = data['game_role_id']
                    nickname = data['nickname']
                    break
            if uid:
                await update_private_cookie(user_id=str(event.user_id), uid=uid, mys_id=mys_id, cookie=cookie)
                await update_last_query(str(event.user_id), uid, 'uid')
                await delete_cookie_cache(uid, key='uid', all=False)
                msg = f'{nickname}绑定成功啦!使用ys/ysa等指令和派蒙互动吧!'
                if event.message_type != 'private':
                    msg += '\n当前是在群聊里绑定，建议旅行者把cookie撤回哦!'
                await ysb.finish(MsgBd.Text(msg), at_sender=True)


@ysbjc.handle()
@exception_handler()
async def ysbjc_handler(event: MessageEvent, msg: Message = CommandArg()):
    cookie = await get_private_cookie(event.user_id)
    if len(cookie) == 0:
        await ysbjc.finish("旅行者当前未绑定私人cookie")
        return
    uid = transform_uid(str(msg))
    if not uid:
        await ysbjc.finish(f"旅行者当前已绑定{len(cookie)}条私人cookie")
        return
    for data in cookie:
        if data['uid'] == uid:
            await ysbjc.finish("旅行者已为此uid绑定私人cookie！")
            return
    await ysbjc.finish("旅行者还没有为此uid绑定私人cookie哦~")


@add_public_ck.handle()
@exception_handler()
async def add_public_ck_handler(event: MessageEvent, msg: Message = CommandArg()):
    cookie = str(msg).strip()
    if await check_cookie(cookie):
        await insert_public_cookie(cookie)
        await add_public_ck.finish('公共cookie添加成功啦,派蒙开始工作!')
    else:
        await add_public_ck.finish(cookie_error_msg)


@delete_ck.handle()
@exception_handler()
async def delete_ck_handler(event: MessageEvent):
    await delete_private_cookie(str(event.user_id))
    await delete_ck.finish('派蒙把你的私人cookie都删除啦!', at_sender=True)


@mys_sign.handle()
@exception_handler()
async def mys_sign_handler(event: MessageEvent, msg: Message = CommandArg()):
    uid, msg, user_id, use_cache = await get_uid_in_msg(event, msg)
    sign_list = await get_sign_list()
    sign_info = await get_sign_info(uid)
    if isinstance(sign_info, str):
        await mys_sign.finish(sign_info, at_sender=True)
    elif sign_info['data']['is_sign']:
        sign_day = sign_info['data']['total_sign_day'] - 1
        await mys_sign.finish(
            f'你今天已经签过到了哦,获得的奖励为:\n{sign_list["data"]["awards"][sign_day]["name"]} * {sign_list["data"]["awards"][sign_day]["cnt"]}',
            at_sender=True)
    else:
        sign_day = sign_info['data']['total_sign_day']
        sign_action = await sign(uid)
        for _ in range(5):
            if isinstance(sign_action, dict):
                if sign_action['data']['success'] == 0:
                    await mys_sign.finish(
                        f'签到成功,获得的奖励为:\n{sign_list["data"]["awards"][sign_day]["name"]} * {sign_list["data"]["awards"][sign_day]["cnt"]}',
                        at_sender=True)
                else:
                    await sleep(random.randint(3, 6))
            else:
                await mys_sign.finish(sign_action, at_sender=True)


@mys_sign_auto.handle()
@exception_handler()
async def mys_sign_auto_handler(event: MessageEvent, msg: Message = CommandArg()):
    if event.message_type == 'group':
        remind_id = str(event.group_id)
    elif event.message_type == 'private':
        remind_id = 'q' + str(event.user_id)
    else:
        await mys_sign_auto.finish('自动签到功能暂时不支持频道使用哦')
    msg = str(msg).strip()
    find_uid = re.search(r'(?P<uid>(1|2|5)\d{8})', msg)
    if not find_uid:
        await mys_sign_auto.finish('请把正确的需要帮忙签到的uid给派蒙哦!', at_sender=True)
    else:
        uid = find_uid.group('uid')
        find_action = re.search(r'(?P<action>开启|启用|打开|关闭|禁用|on|off)', msg)
        if find_action:
            if find_action.group('action') in ['开启', '启用', '打开', 'on']:
                cookie = await get_private_cookie(uid, key='uid')
                if not cookie:
                    await mys_sign_auto.finish('你的该uid还没绑定cookie哦，先用ysb绑定吧!', at_sender=True)
                await add_auto_sign(str(event.user_id), uid, remind_id)
                await mys_sign_auto.finish('开启米游社自动签到成功,派蒙会在每日0点帮你签到', at_sender=True)
            elif find_action.group('action') in ['关闭', '禁用', 'off']:
                await delete_auto_sign(str(event.user_id), uid)
                await mys_sign_auto.finish('关闭米游社自动签到成功', at_sender=True)
        else:
            await mys_sign_auto.finish('指令错误，在后面加 开启/关闭 来使用哦', at_sender=True)


@mys_sign_all.handle()
async def sign_all():
    await auto_sign()


@scheduler.scheduled_job('cron', hour=4, minute=0, misfire_grace_time=10)
async def auto_sign():
    data = await get_auto_sign()
    if data:
        ann = defaultdict(lambda: defaultdict(list))
        logger.info('---派蒙开始执行米游社自动签到---')
        sign_list = await get_sign_list()
        for user_id, uid, remind_id in data:
            sign_info = await get_sign_info(uid)
            if isinstance(sign_info, str):
                with contextlib.suppress(Exception):
                    await delete_auto_sign(user_id, uid)
                    if remind_id.startswith('q'):
                        await get_bot().send_private_msg(user_id=remind_id[1:],
                                                         message=f'你的uid{uid}签到失败，请重新绑定cookie再开启自动签到')
                    else:
                        ann[remind_id]['失败'].append(f'.UID{uid}')
            elif sign_info['data']['is_sign']:
                logger.info(f'---qq{user_id}的UID{uid}已经签过，跳过---')
            else:
                for _ in range(5):
                    sign_result = await sign(uid)
                    if isinstance(sign_result, dict):
                        # success为0则说明没有出现验证码，不为0则有验证码，等待5-10秒再重试，重试最多5次
                        if sign_result['data']['success'] == 0:
                            await sleep(1)
                            sign_info = await get_sign_info(uid)
                            sign_day = sign_info['data']['total_sign_day'] - 1
                            with contextlib.suppress(Exception):
                                if remind_id.startswith('q'):
                                    await get_bot().send_private_msg(user_id=remind_id[1:],
                                                                     message=f'你的uid{uid}自动签到成功!签到奖励为{sign_list["data"]["awards"][sign_day]["name"]}*{sign_list["data"]["awards"][sign_day]["cnt"]}')
                                else:
                                    ann[remind_id]['成功'].append(
                                        f'.UID{uid}-{sign_list["data"]["awards"][sign_day]["name"]}*{sign_list["data"]["awards"][sign_day]["cnt"]}')
                            break
                        else:
                            await sleep(random.randint(5, 10))
            await sleep(random.randint(20, 35))
        for group_id, content in ann.items():
            group_str = '米游社自动签到结果：\n'
            for type, ann_list in content.items():
                if ann_list:
                    group_str += f'签到{type}：\n'
                    for u in ann_list:
                        group_str += str(ann_list.index(u) + 1) + u + '\n'
            try:
                await get_bot().send_group_msg(group_id=group_id, message=group_str)
                await sleep(random.randint(5, 10))
            except Exception as e:
                logger.error(f'米游社签到结果发送失败：{e}')


@scheduler.scheduled_job('cron', hour=4, minute=0, misfire_grace_time=10)
async def coin_auto_sign():
    data = await get_coin_auto_sign()
    ann = defaultdict(lambda: defaultdict(list))
    if data:
        logger.info('---派蒙开始执行米游币自动获取---')
        for user_id, uid, remind_id in data:
            await sleep(random.randint(20, 35))
            sk = await get_private_stoken(uid, key='uid')
            try:
                stoken = sk[0][4]
                get_coin_task = MihoyoBBSCoin(stoken, user_id, uid)
                data = await get_coin_task.run()
                if get_coin_task.state is False:
                    await delete_coin_auto_sign(user_id, uid)
                    if remind_id.startswith('q'):
                        await get_bot().send_private_msg(user_id=remind_id[1:],
                                                         message=f'你的uid{uid}米游币获取失败，请重新绑定stoken再开启')
                    else:
                        ann[remind_id]['失败'].append(f'.UID{uid}')
                else:
                    if remind_id.startswith('q'):
                        await get_bot().send_private_msg(user_id=remind_id[1:],
                                                         message=f'你的uid{uid}米游币自动获取成功')
                    else:
                        ann[remind_id]['成功'].append(f'.UID{uid}')
            except:
                await delete_coin_auto_sign(user_id, uid)
                if remind_id.startswith('q'):
                    await get_bot().send_private_msg(user_id=remind_id[1:],
                                                     message=f'你的uid{uid}米游币获取失败，请重新绑定stoken再开启')
                logger.info('该成员未绑定stoken 获取失败, 已删除自动获取任务')
        for group_id, content in ann.items():
            group_str = '米游币自动获取结果：\n'
            for type, ann_list in content.items():
                if ann_list:
                    group_str += f'{type}：\n'
                    for u in ann_list:
                        group_str += str(ann_list.index(u) + 1) + u + '\n'
            try:
                await get_bot().send_group_msg(group_id=group_id, message=group_str)
                await sleep(random.randint(3, 8))
            except Exception as e:
                logger.error(f'米游币自动获取结果发送失败：{e}')


@get_mys_coin.handle()
@exception_handler()
async def get_mys_coin_handler(event: MessageEvent, msg: Message = CommandArg()): \
        # 获取UID
    uid, msg, user_id, use_cache = await get_uid_in_msg(event, msg)
    if not uid:
        await get_mys_coin.finish('没有找到你的uid哦')
    sk = await get_private_stoken(uid, key='uid')
    if not sk:
        await get_mys_coin.finish('请旅行者先添加cookie和stoken哦')
    cookie = sk[0][1]
    if not cookie:
        await get_mys_coin.finish('你的该uid还没绑定cookie哦，先用ysb绑定吧')
    stoken = sk[0][4]
    await get_mys_coin.send('开始执行米游币获取，请稍等哦~')
    get_coin_task = MihoyoBBSCoin(stoken, str(event.user_id), uid)
    data = await get_coin_task.run()
    msg = "米游币获取完成\n" + data
    await get_mys_coin.finish(msg)


@get_mys_coin_auto.handle()
@exception_handler()
async def get_mys_coin_auto_handler(event: MessageEvent, msg: Message = CommandArg()):
    if event.message_type == 'group':
        remind_id = str(event.group_id)
    elif event.message_type == 'private':
        remind_id = 'q' + str(event.user_id)
    else:
        await get_mys_coin_auto.finish('米游币自动获取功能暂时不支持频道使用哦')
    msg = msg.extract_plain_text().strip()
    find_uid = re.search(r'(?P<uid>(1|2|5)\d{8})', msg)
    if not find_uid:
        await get_mys_coin_auto.finish('请把正确的需要帮忙获取的uid给派蒙哦!', at_sender=True)
    else:
        uid = find_uid.group('uid')
        find_action = re.search(r'(?P<action>开启|启用|打开|关闭|禁用|on|off)', msg)
        if find_action:
            if find_action.group('action') in ['开启', '启用', '打开', 'on']:
                sk = await get_private_stoken(uid, key='uid')
                stoken = sk[0][4]
                if not stoken:
                    await get_mys_coin_auto.finish('你的该uid还没绑定stoken哦，先用添加stoken绑定吧!', at_sender=True)
                await add_coin_auto_sign(str(event.user_id), uid, remind_id)
                await get_mys_coin_auto.finish('开启米游币自动获取成功,派蒙会在每日0点帮你签到', at_sender=True)
            elif find_action.group('action') in ['关闭', '禁用', 'off']:
                await delete_coin_auto_sign(str(event.user_id), uid)
                await get_mys_coin_auto.finish('关闭米游币自动获取成功', at_sender=True)
        else:
            await get_mys_coin_auto.finish('指令错误，在后面加 开启/关闭 来使用哦', at_sender=True)


@add_stoken.handle()
@exception_handler()
async def add_stoken_handler(event: MessageEvent, msg: Message = CommandArg()):
    stoken = msg.extract_plain_text().strip()
    if stoken == '':
        res = '获取stoken的教程：\ndocs.qq.com/doc/DQ3JLWk1vQVllZ2Z1\n获取到后，添加派蒙好友私聊发送ysb接复制到的cookie就行啦~'
        await add_stoken.finish(res, at_sender=True)
    else:
        uid = (await get_private_cookie(event.user_id, key='user_id'))[0][2]
        stoken, mys_id, stoken_info, m = await addStoken(stoken, uid)
        if not stoken_info and not mys_id:
            await add_stoken.finish(m)
        if not stoken_info or stoken_info['retcode'] != 0:
            msg = cookie_error_msg
            if event.message_type != 'private':
                msg += '\n当前是在群聊里绑定，建议旅行者添加派蒙好友私聊绑定!'
            await add_stoken.finish(msg, at_sender=True)
        else:
            if uid:
                await update_private_stoken(user_id=str(event.user_id), uid=uid, mys_id=mys_id, cookie='',
                                            stoken=stoken)
                await update_last_query(str(event.user_id), uid, 'uid')
                msg = f'stoken绑定成功啦!'
                if event.message_type != 'private':
                    msg += '\n当前是在群聊里绑定，建议旅行者把stoken撤回哦!'
                await add_stoken.finish(MsgBd.Text(msg), at_sender=True)


@ys_help.handle()
async def _(event: MessageEvent):
    help_info = '''
    鉴于cookie和stoken的特殊性，建议私聊完成绑定。
    关于这两个的获取，详见
    docs.qq.com/doc/DQ3JLWk1vQVllZ2Z1
    --------
    [ysb cookie]绑定你的私人cookie以开启高级功能
    [删除ck]删除你的私人cookie
    需要cookie来执行签到
    [mys签到]手动进行一次米游社原神签到
    [mys自动签到开启uid/关闭]开启米游社原神自动签到
    --------
    [添加stoken+stoken]添加stoken
    需要stoken来执行米游币获取
    [myb获取]手动进行一次米游币获取
    [myb自动获取开启uid/关闭]开启米游币原神自动获取
    --------
    需要cookie ！较为复杂，详见
    https://blog.ethreal.cn/archives/yysgettoken
    云原神 绑定/bind : 绑定云原神的token
    云原神 信息/info: 查询云原神账户信息
    云原神 签到/sign: 手动签到所绑定的uid（一般绑定之后默认开启自动签到）
    云原神解绑 解绑cookie并取消自动签到
    --------
    需要stoken
    myb 跟随派蒙的指引录入兑换计划
    myb_info 查看当前的兑换计划
    myb_delete 删除你的所有兑换计划
    '''
    await ys_help.finish(help_info)
