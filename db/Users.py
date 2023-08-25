from db import InitDb
from utils.log_utils import log


def add(openid):
    try:
        conn = InitDb.get_connect()
        cursor = conn.cursor()
        insert_sql = f"INSERT INTO {InitDb.users_table_name} (openid) VALUES (?)"
        cursor.execute(insert_sql, (openid,))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        log.error(e)
        return False
