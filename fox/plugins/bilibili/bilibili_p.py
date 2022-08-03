import time
import aiofiles
import aiohttp
import ujson

list_adress = "./fox/data/bilibili/list.json"


async def data_load(json_ad):
    async with aiofiles.open(json_ad, "r", encoding="utf-8")as f:
        text = await f.read()
        data = ujson.loads(text)
    return data


async def aio_get(url):
    try:
        async with aiohttp.ClientSession(
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"},
                timeout=aiohttp.ClientTimeout(total=8)) as session:
            async with session.get(str(url)) as resp:
                text = await resp.text()
                result = ujson.loads(text)
        return result
    except Exception as e:
        pass


async def get_live_room_id(mid):
    data = await aio_get(
        'https://api.bilibili.com/x/space/acc/info?mid='+str(mid)+'&jsonp=jsonp')
    data = data['data']
    roomid = 0
    try:
        roomid = data['live_room']['roomid']
    except:
        pass
    return roomid


async def GetDynamicStatus(uid, nickname):
    cards_data = await aio_get(
        'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid='+str(uid)+'offset_dynamic_id=0')
    cards_data = cards_data['data']['cards']
    #print('Success get')
    try:
        async with aiofiles.open('./fox/data/bilibili/dynamic/'+str(uid)+'Dynamic', 'r') as f:
            last_dynamic_str = await f.read()
    except Exception as err:
        last_dynamic_str = ''
        pass
    if last_dynamic_str == '':
        last_dynamic_str = cards_data[1]['desc']['dynamic_id_str']
    print(nickname+"上一条动态是："+str(last_dynamic_str))
    index = 0
    content_list = []
    cards_data[0]['card'] = ujson.loads(
        cards_data[0]['card'])
    nowtime = time.time().__int__()
    # card是字符串，需要重新解析
    while last_dynamic_str != cards_data[index]['desc']['dynamic_id_str']:
        # print(cards_data[index]['desc'])
        try:
            if nowtime-cards_data[index]['desc']['timestamp'] > 400:
                break
            if (cards_data[index]['desc']['type'] == 64):
                content_list.append(nickname + '发了新专栏「' + cards_data[index]
                                    ['card']['title'] + '」并说： ' + cards_data[index]['card']['dynamic'])
            else:
                if (cards_data[index]['desc']['type'] == 8):
                    content_list.append(nickname + '发了新视频「' + cards_data[index]
                                        ['card']['title'] + '」并说： ' + cards_data[index]['card']['dynamic'])
                else:
                    if ('description' in cards_data[index]['card']['item']):
                        # 这个是带图新动态
                        content_list.append(
                            nickname + '发了新动态： ' + cards_data[index]['card']['item']['description'])
                        # print('Fuck')
                        # CQ使用参考：[CQ:image,file=http://i1.piimg.com/567571/fdd6e7b6d93f1ef0.jpg]
                        for pic_info in cards_data[index]['card']['item']['pictures']:
                            content_list.append(
                                '[CQ:image,file='+pic_info['img_src']+']')
                    else:
                        # 这个表示转发，原动态的信息在 cards-item-origin里面。里面又是一个超级长的字符串……
                        # origin = json.loads(cards_data[index]['card']['item']['origin'],encoding='gb2312') 我也不知道这能不能解析，没试过
                        #origin_name = 'Fuck'
                        if 'origin_user' in cards_data[index]['card']:
                            origin_name = cards_data[index]['card']['origin_user']['info']['uname']
                            content_list.append(
                                nickname + '转发了「' + origin_name + '」的动态并说： ' + cards_data[index]['card']['item']['content'])
                        else:
                            # 这个是不带图的自己发的动态
                            content_list.append(
                                nickname + '发了新动态： ' + cards_data[index]['card']['item']['content'])
            content_list.append('本条动态地址为'+'https://t.bilibili.com/' +
                                cards_data[index]['desc']['dynamic_id_str'])
        except Exception as err:
            print('PROCESS ERROR')
            pass
        index += 1
        if len(cards_data) == index:
            break
        cards_data[index]['card'] = ujson.loads(cards_data[index]['card'])
    async with aiofiles.open('./fox/data/bilibili/dynamic/'+str(uid)+'Dynamic', 'w')as f:
        await f.write(cards_data[0]['desc']['dynamic_id_str'])
    return content_list


async def GetLiveStatus(uid):
    live_data = await aio_get(
        'https://api.live.bilibili.com/room/v1/Room/get_info?device=phone&;platform=ios&scale=3&build=10000&room_id=' + str(uid))
    try:
        async with aiofiles.open('./fox/data/bilibili/live/'+str(uid)+'Live', 'r') as f:
            last_live_str = await f.read()
    except Exception as err:
        last_live_str = '0'
        pass
    try:
        live_data = live_data['data']
        now_live_status = str(live_data['live_status'])
        live_title = live_data['title']
    except:
        now_live_status = '0'
        pass
    async with aiofiles.open('./fox/data/bilibili/live/'+str(uid)+'Live', 'w') as f:
        await f.write(now_live_status)
    if last_live_str != '1':
        if now_live_status == '1':
            return live_title
    return ''


async def group_query(q_group_id, data):
    result = ""
    for i in data["data"]:
        for group_id in i["group_id"]:
            if group_id == q_group_id:
                result += i["nickname"]+f"：space.bilibili.com/{i['uid']}\n"
                break
    if result == "":
        return f"群{q_group_id}尚未订阅任何b站up主..."
    else:
        return f"群{q_group_id}目前正在订阅：\n{result[0:len(result)-1]}"


async def describe_writer(data, args, q_nickname, q_uid, q_group_id):
    for i in data["data"]:
        if q_uid == i["uid"]:
            for group in i["group_id"]:
                if group == q_group_id:
                    if args == "add":
                        return f"本群已经订阅了{q_nickname}"
                    if args == "del":
                        if len(i["group_id"]) != 1:
                            i["group_id"].remove(q_group_id)
                            return str(await write_down(data, q_nickname, q_uid))
                        else:
                            data["data"].remove(i)
                            return str(await write_down(data, q_nickname, q_uid))
                    break
            if args == "add":
                i["group_id"].append(q_group_id)
                return str(await write_down(data, q_nickname, q_uid))
            else:
                return f"本群并没有订阅{q_nickname}"
    if args == "add":
        new_up = dict(uid=q_uid, nickname=q_nickname, group_id=[q_group_id])
        data["data"].append(new_up)
        return str(await write_down(data, q_nickname, q_uid))
    else:
        return f"没有找到{q_uid}"


async def write_down(data, q_nickname, q_uid):
    try:
        async with aiofiles.open(list_adress, "w") as f:
            text = ujson.dumps(data)
            await f.write(text)
        return f"已修改{q_nickname}：space.bilibili.com/{q_uid}"
    except Exception as e:
        return "文件写入错误！"
