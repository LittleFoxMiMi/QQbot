# 更新cookie
from datetime import datetime
import os
import sqlite3

db_path = os.path.abspath('./fox/data/paimon/')+"/user_data.db"


async def update_private_cookie(user_id, uid='', mys_id='', cookie='', stoken=''):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS private_cookies
        (
            user_id TEXT NOT NULL,
            uid TEXT NOT NULL,
            mys_id TEXT,
            cookie TEXT,
            stoken TEXT,
            PRIMARY KEY (user_id, uid)
        );''')
    cursor.execute('REPLACE INTO private_cookies VALUES (?, ?, ?, ?, ?);',
                   (user_id, uid, mys_id, cookie, stoken))
    conn.commit()
    conn.close()

# 更新user_id最后查询的uid


async def update_last_query(user_id, value, key='uid'):
    t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS last_query(
        user_id TEXT PRIMARY KEY NOT NULL,
        uid TEXT,
        mys_id TEXT,
        last_time datetime);''')
    cursor.execute(
        f'REPLACE INTO last_query (user_id, {key}, last_time) VALUES ("{user_id}", "{value}", "{t}");')
    conn.commit()
    conn.close()


# 删除cookie缓存
async def delete_cookie_cache(value='', key='cookie', all=False):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        if all:
            cursor.execute('DROP TABLE cookie_cache;')
        else:
            cursor.execute(f'DELETE FROM cookie_cache WHERE {key}="{value}";')
        conn.commit()
        conn.close()
    except:
        pass

# 获取user_id最后查询的uid


async def get_last_query(user_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS last_query(
        user_id TEXT PRIMARY KEY NOT NULL,
        uid TEXT,
        last_time datetime);''')
    cursor.execute('SELECT uid FROM last_query WHERE user_id=?;', (user_id,))
    uid = cursor.fetchone()
    conn.close()
    return uid[0] if uid else None


# 通过key(如user_id, uid)获取私人cookie
async def get_private_cookie(value, key='user_id'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS private_cookies
        (
            user_id TEXT NOT NULL,
            uid TEXT NOT NULL,
            mys_id TEXT,
            cookie TEXT,
            stoken TEXT,
            PRIMARY KEY (user_id, uid)
        );''')
    cursor.execute(
        f'SELECT user_id, cookie, uid, mys_id FROM private_cookies WHERE {key}="{value}";')
    cookie = cursor.fetchall()
    conn.close()
    return cookie

# 插入公共cookie


async def insert_public_cookie(cookie):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS public_cookies 
    (
        no int IDENTITY(1,1) PRIMARY KEY,
        cookie TEXT,
        status TEXT
    );''')
    cursor.execute(
        'INSERT OR IGNORE INTO public_cookies (cookie, status) VALUES (?,"OK");', (cookie,))
    conn.commit()
    conn.close()

# 删除私人cookie


async def delete_private_cookie(user_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS private_cookies
        (
            user_id TEXT NOT NULL,
            uid TEXT NOT NULL,
            mys_id TEXT,
            cookie TEXT,
            stoken TEXT,
            PRIMARY KEY (user_id, uid)
        );''')
    cursor.execute('DELETE FROM private_cookies WHERE user_id=?', (user_id,))
    conn.commit()
    conn.close()

# 设置公共cookie到上限


async def limit_public_cookie(cookie):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS public_cookies(
        no int IDENTITY(1,1) PRIMARY KEY,
        cookie TEXT,
        status TEXT);''')
    cursor.execute(
        'UPDATE public_cookies SET status="limited30" WHERE cookie=?;', (cookie,))
    conn.commit()
    conn.close()

# 更新cookie缓存


async def update_cookie_cache(cookie, value, key='uid'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS cookie_cache(
        uid TEXT PRIMARY KEY NOT NULL,
        mys_id TEXT,
        cookie TEXT);''')
    cursor.execute(
        f'REPLACE INTO cookie_cache ({key}, cookie) VALUES ("{value}", "{cookie}");')
    conn.commit()
    conn.close()


async def add_auto_sign(user_id, uid, group_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bbs_sign
    (
        user_id TEXT NOT NULL,
        uid TEXT NOT NULL,
        group_id TEXT,
        PRIMARY KEY (user_id, uid)
    );''')
    cursor.execute('REPLACE INTO bbs_sign VALUES (?, ?, ?);',
                   (user_id, uid, group_id))
    conn.commit()
    conn.close()


async def delete_auto_sign(user_id, uid):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bbs_sign
    (
        user_id TEXT NOT NULL,
        uid TEXT NOT NULL,
        group_id TEXT,
        PRIMARY KEY (user_id, uid)
    );''')
    cursor.execute(
        'DELETE FROM bbs_sign WHERE user_id=? AND uid=?;', (user_id, uid))
    conn.commit()
    conn.close()


async def get_auto_sign():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bbs_sign
    (
        user_id TEXT NOT NULL,
        uid TEXT NOT NULL,
        group_id TEXT,
        PRIMARY KEY (user_id, uid)
    );''')
    cursor.execute('SELECT * FROM bbs_sign;')
    res = cursor.fetchall()
    conn.close()
    return res


async def get_coin_auto_sign():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS coin_bbs_sign
    (
        user_id TEXT NOT NULL,
        uid TEXT NOT NULL,
        group_id TEXT,
        PRIMARY KEY (user_id, uid)
    );''')
    cursor.execute('SELECT user_id,uid,group_id FROM coin_bbs_sign;')
    res = cursor.fetchall()
    conn.close()
    return res

# 通过key(如user_id, uid)获取私人Stoken


async def get_private_stoken(value, key='user_id'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS private_cookies
        (
            user_id TEXT NOT NULL,
            uid TEXT NOT NULL,
            mys_id TEXT,
            cookie TEXT,
            stoken TEXT,
            PRIMARY KEY (user_id, uid)
        );''')
    cursor.execute(
        f'SELECT user_id, cookie, uid, mys_id,stoken FROM private_cookies WHERE {key}="{value}";')
    stoken = cursor.fetchall()
    conn.close()
    return stoken


async def delete_coin_auto_sign(user_id, uid):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS coin_bbs_sign
    (
        user_id TEXT NOT NULL,
        uid TEXT NOT NULL,
        group_id TEXT,
        PRIMARY KEY (user_id, uid)
    );''')
    cursor.execute(
        'DELETE FROM coin_bbs_sign WHERE user_id=? AND uid=?;', (user_id, uid))
    conn.commit()
    conn.close()


async def add_coin_auto_sign(user_id, uid, group_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS coin_bbs_sign
    (
        user_id TEXT NOT NULL,
        uid TEXT NOT NULL,
        group_id TEXT,
        PRIMARY KEY (user_id, uid)
    );''')
    cursor.execute('REPLACE INTO coin_bbs_sign VALUES (?, ?, ?);',
                   (user_id, uid, group_id))
    conn.commit()
    conn.close()

# 更新stoken


async def update_private_stoken(user_id, uid='', mys_id='', cookie='', stoken=''):
    # 保证cookie不被更新
    ck = await get_private_cookie(uid, key='uid')
    cookie = ck[0][1]

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS private_cookies
        (
            user_id TEXT NOT NULL,
            uid TEXT NOT NULL,
            mys_id TEXT,
            cookie TEXT,
            stoken TEXT,
            PRIMARY KEY (user_id, uid)
        );''')
    cursor.execute('REPLACE INTO private_cookies VALUES (?, ?, ?, ?, ?);',
                   (user_id, uid, mys_id, cookie, stoken))
    conn.commit()
    conn.close()
