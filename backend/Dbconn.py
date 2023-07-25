import sqlite3

import os

DATABASE = './db.sqlite'
conn = sqlite3.connect(DATABASE, check_same_thread=False)


def init():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)


def dbGet(sql, params):
    cur = conn.cursor()
    cur.execute(sql, params)
    ret = cur.fetchall()

    return ret


def dbSet(sql, params):
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    cur = conn.cursor()

    cur.execute(sql, params)

    if sql.split(' ')[0] == 'INSERT':
        # 插入操作返回主键
        ret = cur.lastrowid
    else:
        # 删除和更新操作返回影响行数
        ret = cur.rowcount

    conn.commit()
    return ret
