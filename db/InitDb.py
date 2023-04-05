import logging
import sqlite3

import config
from log import logger

usersTableName = 'users'
usersNotifyTableName = 'users_notify'


def initTable():
    logger.info("开始初始化表")
    # 连接到 jobs.db 数据库
    conn = sqlite3.connect(config.conf().get("db_path"))
    cursor = conn.cursor()
    # 初始化表
    initUsers(conn, cursor)
    initUsersNotify(conn, cursor)
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()


def initUsers(conn, cursor):
    # 如果 user 表不存在，则创建该表
    if not checkTableExists(cursor, usersTableName):
        createUsers(conn, cursor, usersTableName)
    else:
        logger.info(f'表 {usersTableName} 已存在')


def initUsersNotify(conn, cursor):
    # 如果 user 表不存在，则创建该表
    if not checkTableExists(cursor, usersNotifyTableName):
        createUsersNotify(conn, cursor, usersNotifyTableName)
    else:
        logger.info(f'表 {usersNotifyTableName} 已存在')


def createUsers(conn, cursor, tableName):
    cursor.execute(f'''
                CREATE TABLE {tableName} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    openid TEXT NOT NULL,
                    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    update_time DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    # 创建触发器，自动更新更新时间字段
    cursor.execute(f'''
                CREATE TRIGGER update_{tableName}
                AFTER UPDATE ON {tableName}
                FOR EACH ROW
                BEGIN
                    UPDATE {tableName} SET update_time = DATETIME('NOW') WHERE id = NEW.id;
                END;
            ''')
    conn.commit()
    logger.info(f'表 {tableName} 创建成功')


def checkTableExists(cursor, tableName):
    # 判断 user 表是否存在
    cursor.execute(
        f'''
        SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}'
        ''')
    return cursor.fetchone() is not None


def createUsersNotify(conn, cursor, tableName):
    cursor.execute(f'''
                CREATE TABLE {tableName} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    openid TEXT NOT NULL,
                    notity_type INTEGER NOT NULL,
                    notity_key TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    is_enable INTEGER NOT NULL DEFAULT 1,
                    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    update_time DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    # 创建触发器，自动更新更新时间字段
    cursor.execute(f'''
                CREATE TRIGGER update_{tableName}
                AFTER UPDATE ON {tableName}
                FOR EACH ROW
                BEGIN
                    UPDATE {tableName} SET update_time = DATETIME('NOW') WHERE id = NEW.id;
                END;
            ''')
    conn.commit()
    logger.info(f'表 {tableName} 创建成功')
