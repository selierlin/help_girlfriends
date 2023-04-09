from db import InitDb
from log import logger


def add(openid, notify_type, notify_key, tags):
    try:
        conn = InitDb.get_connect()
        cursor = conn.cursor()
        insert_sql = f"INSERT INTO {InitDb.users_notify_table_name} (openid, notify_type, notify_key, tags) VALUES (?, ?, ?, ?)"
        cursor.execute(insert_sql, (openid, notify_type, notify_key, tags))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        logger.error(e)
        return False


def update(openid, notify_type, notify_key, is_enable):
    try:
        conn = InitDb.get_connect()
        cursor = conn.cursor()
        update_sql = f"UPDATE {InitDb.users_notify_table_name} SET is_enable = ? where openid = ? AND notify_key = ? AND notify_type = ?"
        cursor.execute(update_sql, (is_enable, openid, notify_key, notify_type))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        logger.error(e)
        return False


def delete(openid, notify_type, notify_key):
    try:
        conn = InitDb.get_connect()
        cursor = conn.cursor()
        update_sql = f"DELETE FROM {InitDb.users_notify_table_name} where openid = ? AND notify_key = ? AND notify_type = ?"
        cursor.execute(update_sql, (openid, notify_key, notify_type))
        conn.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount
    except Exception as e:
        logger.error(e)
        return -1


def find(openid):
    try:
        conn = InitDb.get_connect()
        cursor = conn.cursor()
        select_sql = f"SELECT * FROM {InitDb.users_notify_table_name} where openid = ?"
        cursor.execute(select_sql, (openid,))
        result = cursor.fetchall()
        conn.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return result
    except Exception as e:
        logger.error(e)
        return None
