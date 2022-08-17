import subprocess
import os
import time

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.typing import T_State
from fox.check import qq_check

youtubedl = on_command("youtubedl", priority=1, block=True)
super_user = "./fox/data/config/superuser.txt"
download_path = "/home/qqbot/fox/data/youtubedl/"
video_info = "str"
download_args = ""
file_name = ""


@youtubedl.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    global download_args
    global file_name
    global video_info
    args = str(event.get_message()).strip().split(" ")
    args = args[1:]
    if not await qq_check(event.get_user_id(), super_user):
        await youtubedl.finish("你没有权限捏")
    len_args = len(args)
    download_args = f"cd {download_path} && yt-dlp "
    ffmpeg_args = ""
    url = ""
    name_args = "output"
    if len_args == 0:
        await youtubedl.finish("至少需要一个url参数")
    elif len_args > 5:
        await youtubedl.finish("传入了过多的参数！\nyoutubedl url [-f mp3] [-name name]")
    if "youtu.be" in args[0]:
        download_args += "-f bestaudio+bestvideo "
    else:
        download_args += "-f best "
    count = 0
    ext = ""
    for arg in args:
        count += 1
        if count > len(args):
            break
        if arg == "-f":
            if args[count] == "mp3":
                ext = args[count]
                ffmpeg_args = f"--recode-video {args[count]} "
            else:
                await youtubedl.finish("服务器只有1c1t，转码MP4会造成长达数个小时的主进程堵塞，只允许MP3捏。\n进程已退出。。。。")
        elif arg == "-name":
            name_args = args[count]
        elif arg[:4] == "HTTP" or arg[:4] == "http":
            url = arg
    file_name = name_args+"."+ext
    download_args += ffmpeg_args + f"-o '{name_args}.%(ext)s' " + url
    try:
        await clear_dir()
    except:
        await youtubedl.finish("清空download目录错误！")
    check_args = f"yt-dlp {args[0]} --get-title"
    video_info = await check_info(check_args)
    video_info = video_info.decode()
    video_info = video_info.replace("\n", "")
    await youtubedl.send(video_info)


async def check_info(args):
    try:
        info = subprocess.check_output(args, shell=True)
        return info
    except Exception as e:
        await youtubedl.finish("获取信息错误！\n错误代码是:"+str(e))


async def download(args):
    try:
        subprocess.check_call(args, shell=True)
    except Exception as e:
        await youtubedl.finish("download错误！\n错误代码是:"+str(e))


@youtubedl.got("check", prompt="是否确认下载？(y/n)")
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    check = str(event.get_message()).strip()
    if check == "y" or check == "Y":
        await youtubedl.send("正在下载。。。")
        await download(download_args)
        while True:
            filename = os.listdir(download_path)
            if len(filename) != 0:
                if len(filename) == 1:
                    name = filename[0]
                else:
                    name = file_name
                break
            else:
                await youtubedl.finish("未找到指定的文件")
        await youtubedl.send("正在上传。。。")
        await bot.call_api(api="upload_group_file", group_id=event.group_id, file=download_path+name, name=name)
    else:
        await youtubedl.finish("操作取消")


async def clear_dir():
    filename = os.listdir(download_path)
    for name in filename:
        os.remove(download_path+name)
