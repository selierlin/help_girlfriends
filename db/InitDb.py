import sqlite3

from utils import config
from utils.log_utils import log

users_table_name = 'users'
users_notify_table_name = 'users_notify'


def get_connect():
    return sqlite3.connect(config.get("db_path"))


def init_table():
    log.info("开始初始化表")
    conn = get_connect()
    # 连接到 jobs.db 数据库
    cursor = conn.cursor()
    # 初始化表
    init_users(conn, cursor)
    init_users_notify(conn, cursor)
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()


def init_users(conn, cursor):
    # 如果 user 表不存在，则创建该表
    if not check_table_exists(cursor, users_table_name):
        create_users(conn, cursor, users_table_name)
    else:
        log.info(f'表 {users_table_name} 已加载')


def init_users_notify(conn, cursor):
    # 如果 user 表不存在，则创建该表
    if not check_table_exists(cursor, users_notify_table_name):
        create_users_notify(conn, cursor, users_notify_table_name)
    else:
        log.info(f'表 {users_notify_table_name} 已加载')


def create_users(conn, cursor, table_name):
    cursor.execute(f'''
                CREATE TABLE {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    openid TEXT NOT NULL,
                    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    update_time DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    # 创建触发器，自动更新更新时间字段
    cursor.execute(f'''
                CREATE TRIGGER update_{table_name}
                AFTER UPDATE ON {table_name}
                FOR EACH ROW
                BEGIN
                    UPDATE {table_name} SET update_time = DATETIME('NOW') WHERE id = NEW.id;
                END;
            ''')

    # 设置 openid 唯一索引
    cursor.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{table_name}_notify ON {table_name} (openid)")

    conn.commit()
    log.info(f'表 {table_name} 创建成功')


def check_table_exists(cursor, table_name):
    # 判断 user 表是否存在
    cursor.execute(
        f'''
        SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'
        ''')
    return cursor.fetchone() is not None


def create_users_notify(conn, cursor, table_name):
    cursor.execute(f'''
                CREATE TABLE {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    openid TEXT NOT NULL,
                    notify_type INTEGER NOT NULL,
                    notify_key TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    is_enable INTEGER NOT NULL DEFAULT 1,
                    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    update_time DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    # 创建触发器，自动更新更新时间字段
    cursor.execute(f'''
                CREATE TRIGGER update_{table_name}
                AFTER UPDATE ON {table_name}
                FOR EACH ROW
                BEGIN
                    UPDATE {table_name} SET update_time = DATETIME('NOW') WHERE id = NEW.id;
                END;
            ''')

    # 设置 openid notify_type notify_key 联合唯一索引
    cursor.execute(
        f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{table_name}_notify ON {table_name} (openid, notify_type, notify_key)")

    conn.commit()
    log.info(f'表 {table_name} 创建成功')
