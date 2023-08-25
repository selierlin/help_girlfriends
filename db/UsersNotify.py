from db import InitDb
from utils.log_utils import log


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
        log.error(e)
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
        log.error(e)
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
        log.error(e)
        return -1


def delete_by_openid(openid, key_id):
    try:
        conn = InitDb.get_connect()
        cursor = conn.cursor()
        update_sql = f"DELETE FROM {InitDb.users_notify_table_name} where openid = ? AND id = ?"
        cursor.execute(update_sql, (openid, key_id))
        conn.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount
    except Exception as e:
        log.error(e)
        return -1


def update_by_openid(openid, key_id, state):
    try:
        conn = InitDb.get_connect()
        cursor = conn.cursor()
        update_sql = f"UPDATE {InitDb.users_notify_table_name} set is_enable = ? where openid = ? AND id = ?"
        cursor.execute(update_sql, (state, openid, key_id))
        conn.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount
    except Exception as e:
        log.error(e)
        return -1


def find(openid):
    try:
        conn = InitDb.get_connect()
        cursor = conn.cursor()
        select_sql = f"SELECT * FROM {InitDb.users_notify_table_name} where openid = ? and is_enable = 1"
        cursor.execute(select_sql, (openid,))
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        return result
    except Exception as e:
        log.error(e)
        return None


def list_key(openid):
    try:
        conn = InitDb.get_connect()
        cursor = conn.cursor()
        select_sql = f"SELECT id,tags,notify_type,is_enable,create_time,notify_key FROM {InitDb.users_notify_table_name} where openid = ?"
        cursor.execute(select_sql, (openid,))
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        return result
    except Exception as e:
        log.error(e)
        return None
