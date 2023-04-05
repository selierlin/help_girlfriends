import logging
import sqlite3

from log import logger

userTableName = 'users'


def initTable():
    logger.info("开始初始化表")
    # 连接到 jobs.db 数据库
    conn = sqlite3.connect('/Users/selier/Project/help_girlfriends/jobs.db')
    cursor = conn.cursor()
    initUsers(conn, cursor)
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()


def initUsers(conn, cursor):
    # 如果 user 表不存在，则创建该表
    if not checkTableExists(cursor, userTableName):
        createUsers(conn, cursor, userTableName)
    else:
        logger.info(f'表 {userTableName} 已存在')


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

