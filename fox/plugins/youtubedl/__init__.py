import subprocess
import os
import time

from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.typing import T_State
from fox.check import qq_check

youtubedl = on_command("youtubedl", priority=1, block=True)
super_user = "./fox/data/config/superuser.txt"
download_path = "/home/qqbot/fox/data/youtubedl/"


@youtubedl.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    args = str(event.get_message()).strip().split(" ")
    if not await qq_check(event.get_user_id(), super_user):
        await youtubedl.finish("你没有权限捏")
    len_args = len(args)
    download_args = f"cd {download_path} && yt-dlp "
    ffmpeg_args = "--recode-video mp4 "
    name_args = 'output'
    if args == [""]:
        await youtubedl.finish("至少需要一个url参数")
    elif len_args > 3:
        await youtubedl.finish("传入了过多的参数！\nyoutubedl url [mp3/mp4] [name]")
    if "youtu.be" in args[0]:
        download_args += "-f bestaudio+bestvideo "
    else:
        download_args += "-f best "
    if len_args == 2:
        await youtubedl.finish("传入了过少的参数！\nyoutubedl url [mp3/mp4] [name]")
    if len_args == 3:
        ffmpeg_args = f"--recode-video {args[1]} "
        name_args = args[2]
    download_args += ffmpeg_args + f"-o '{name_args}.%(ext)s' " + args[0]
    try:
        await clear_dir()
    except:
        await youtubedl.finish("清空download目录错误！")
    await youtubedl.send("正在下载。。。")
    await download(download_args)
    while True:
        filename = os.listdir(download_path)
        if len(filename) != 0:
            if len_args > 1:
                if filename[0] == name_args+'.'+args[1]:
                    break
            else:
                if filename[0] == 'output.mp4':
                    break
        else:
            print("sleep one sec...")
            time.sleep(1)
    name = filename[0]
    time.sleep(5)
    await bot.call_api(api="upload_group_file", group_id=event.group_id, file=download_path+name, name=name)


async def download(args):
    try:
        subprocess.check_call(args, shell=True)
    except Exception as e:
        await youtubedl.finish("download错误！\n错误代码是:"+str(e))


async def clear_dir():
    filename = os.listdir(download_path)
    for name in filename:
        os.remove(download_path+name)
