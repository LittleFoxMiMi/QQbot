import os
import re
import aiofiles
import aiohttp
import codecs
import shutil
import subprocess

savepath = "./fox/data/line/"


async def sticker_download(pack_id, linesticker, bot, event):
    pack_meta = await get_pack_meta(pack_id)
    if pack_meta=="err":
        return f"找不到id为'{pack_id}'的贴纸包"
    name_string = """"en":"""  # folder name will take pack's English title
    pack_name = get_pack_name(name_string, pack_meta)
    pack_name = decode_escapes(pack_name)
    pack_name = pack_name.strip()
    await linesticker.send(f"正在下载 {pack_name}")
    await clear_dir()
    sticker_path = validate_savepath(pack_name)
    id_string = """"id":"""
    list_ids = []
    current_id, start_index = 0, 0  # [4] Why have start_index included
    while start_index != -1:
        start_index, current_id, pack_meta = get_ids(id_string, pack_meta)
        # "Passing by assignment" mutable vs. immutable. Any reassignments done in called function will not reflect on return. But manipulating the parameter will reflect. # noqa: E501
        list_ids.append(current_id)
    list_ids.pop()  # [4] Why pop
    if """"hasAnimation":true""" in pack_meta:
        if await get_gif(pack_id, list_ids, sticker_path) == "err":
            return "下载gif失败"
    else:
        if await get_png(list_ids, sticker_path) == "err":
            return "下载图片失败"
    shutil.make_archive(savepath+"Sticker", "zip", sticker_path)
    await bot.call_api(api="upload_group_file", group_id=event.group_id, file=sticker_path+".zip", name=pack_name+".zip")
    return "OK"


async def clear_dir():
    shutil.rmtree(savepath)
    os.mkdir(savepath)
    

def get_pack_name(name_string, pack_meta):
    start_index = pack_meta.find(name_string)
    end_index = pack_meta.find(',', start_index + 1)
    sticker_name = pack_meta[start_index+len(name_string)+1:end_index-1]  # lower bound needs +1 to exclude the beginning " mark. -1 to make upper bound the , which is excluded from the range # noqa: E501
    return sticker_name


def get_ids(id_string, pack_meta):
    start_index = pack_meta.find(id_string)
    end_index = pack_meta.find(",", start_index + 1)
    sticker_id = pack_meta[start_index+len(id_string):end_index]
    return start_index, sticker_id, pack_meta[end_index:]


def validate_savepath(pack_name):
    decoded_name = decode_escapes(pack_name)
    save_name = "".join(i for i in decoded_name if i not in r'\/:*?"<>|')
    os.makedirs(savepath+str(save_name), exist_ok=True)  # exist_ok = True doesn't raise exception if directory exists. Files already in directory are not erased # noqa: E501
    return savepath+save_name


async def get_gif(pack_id, list_ids, sticker_path):
    for x in list_ids:
        save_path = sticker_path + '/'+str(x) + '.apng'
        url = 'https://stickershop.line-scdn.net/products/0/0/1/{}/iphone/animation/{}@2x.png'.format(pack_id, x)  # noqa: E501
        if await download_pic(url, save_path) == "err":
            return "err"
        #subprocess.check_output(f"ffmpeg -i '{save_path}' -f gif '{save_path[:-4]}.gif'", shell=True)
        subprocess.check_output(f"ffmpeg -v warning -i '{save_path}' -vf 'fps=15,scale=320:-1:flags=lanczos,palettegen' -y '{savepath}palette.png' && ffmpeg -v warning -i '{save_path}' -i '{savepath}palette.png' -lavfi 'fps=15,scale=320:-1:flags=lanczos [x]; [x][1:v] paletteuse' -y '{save_path[:-5]}.gif'", shell=True)
        os.remove(save_path)

async def get_png(list_ids, sticker_path):
    for x in list_ids:
        save_path = sticker_path + '/'+str(x) + '.png'
        url = 'https://stickershop.line-scdn.net/stickershop/v1/sticker/{}/iphone/sticker@2x.png'.format(x)  # noqa: E501
        if await download_pic(url, save_path) == "err":
            return "err"


async def get_pack_meta(pack_id):

    pack_url = "https://stickershop.line-scdn.net/products/0/0/1/{}/android/productInfo.meta".format(pack_id)  # noqa: E501
    async with aiohttp.ClientSession(
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"},
            timeout=aiohttp.ClientTimeout(total=10)) as session:
        async with session.get(pack_url) as resp:
            if resp.status == 200:
                return await resp.text()
            else:
                return "err"


unicode_sanitizer = re.compile(r'''  # compile pattern into object, use with match()
    ( \\U........      # 8-digit hex escapes, backslash U followed by 8 non-newline characters  # noqa: E501
    | \\u....          # 4-digit hex escapes, bksl u followed by 4 non-newline characters  # noqa: E501
    | \\x..            # 2-digit hex escapes, bksl x followed by 2 non-newline characters  # noqa: E501
    | \\[0-7]{1,3}     # Octal escapes, bksl followed by 1 to 3 numbers within range of 0-7  # noqa: E501
    | \\N\{[^}]+\}     # Unicode characters by name, uses name index
    | \\[\\'"abfnrtv]  # Single-character escapes, e.g. tab, backspace, quotes
    )''', re.VERBOSE)  # re.UNICODE not necessary in Py3, matches Unicode by default. re.VERBOSE allows separated sections  # noqa: E501


def decode_escapes(orig):
    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')
    return unicode_sanitizer.sub(decode_match, orig)  # sub returns string with replaced patterns  # noqa: E501


async def download_pic(url, path):
    try:
        async with aiohttp.ClientSession(
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"},
                timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(url) as resp:
                img = await resp.read()
    except Exception as e:
        return "err"
    async with aiofiles.open(path, "wb") as f:
        await f.write(img)
