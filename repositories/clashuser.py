from repositories.db import get_pool
from psycopg.rows import dict_row


def get_clash_users():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """SELECT
                                clashname,
                                optin,
                                id 
                            FROM 
                                clash"""
            )
            return cursor.fetchall()
        
def get_id():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """SELECT
                                id 
                            FROM 
                                clash"""
            )
            return cursor.fetchall()


def insert_clash_users(cname: str, opt: bool):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            insert_query = """INSERT INTO clash (clashname, optin)
                              VALUES (%s, %s);"""
            cursor.execute(insert_query, (cname, opt))
            conn.commit()
            

def delete_clash_users(clashid: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            delete_query = """DELETE FROM clash WHERE id = %s;"""
            cursor.execute(delete_query, (clashid,))
            conn.commit()


def check_user_exists(name: str) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT EXISTS(
                    SELECT 1
                    FROM clash
                    WHERE clashname = %s
                )""",
                (name,)
            )
            exists = cursor.fetchone()[0]
            return exists
            