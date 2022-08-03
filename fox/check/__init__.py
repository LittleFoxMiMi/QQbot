import os
import aiofiles


async def qq_check(qq, p):
    if os.path.exists(p):
        async with aiofiles.open(p, "r", encoding='utf-8') as f:
            lines = await f.readlines()
            for line in lines:
                line = line.strip()
                if line == str(qq):
                    return True
    return False


async def files_writer(qq, args, p):
    if not os.path.exists(p) and args == "off":
        async with aiofiles.open(p, "w", encoding="utf-8") as f:
            pass
    if os.path.exists(p):
        async with aiofiles.open(p, "r", encoding='utf-8') as f:
            lines = await f.readlines()
        if args == "on":
            if str(qq)+"\n" not in lines:
                return "找不到对象喵！"
            else:
                lines.remove(str(qq)+"\n")
        else:
            if str(qq)+"\n" not in lines:
                lines.append(str(qq)+"\n")
            else:
                return "对象已存在喵！"
        async with aiofiles.open(p, "w", encoding='utf-8') as f:
            for line in lines:
                if str(line) != "\n":
                    await f.write(str(line))
    return "命令成功完成喵"
