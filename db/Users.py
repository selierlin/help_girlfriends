from db import InitDb
from log import logger


def add(openid):
    try:
        conn = InitDb.getConnect()
        cursor = conn.cursor()
        insert_sql = f"INSERT INTO {InitDb.usersTableName} (openid) VALUES (?)"
        cursor.execute(insert_sql, (openid,))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        logger.error(e)
        return False
