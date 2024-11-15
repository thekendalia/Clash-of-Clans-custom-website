from repositories.db import get_pool
from psycopg.rows import dict_row
import bcrypt


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
            
            
def new_account(uname: str, cname: str, password: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            insert_query = """INSERT INTO users (username, email, password, code, clan_tag)
                              VALUES (%s, %s, %s, 7685, 000);"""
            cursor.execute(insert_query, (uname, cname, password))
            conn.commit()
            
def update_clan_tag(clan_tag: str, email: str):  
    pool = get_pool() 
    with pool.connection() as conn:  
        with conn.cursor() as cursor:   
            update_query = """UPDATE users SET clan_tag = %s WHERE email = %s;"""  
            cursor.execute(update_query, (clan_tag, email))
            conn.commit()
            
def delete_account(email: str):  
    pool = get_pool() 
    with pool.connection() as conn:  
        with conn.cursor() as cursor:   
            update_query = """DELETE FROM users where email = %s"""  
            cursor.execute(update_query, (email,))
            conn.commit()
            

def login_user(username: str, userpass: str):   
    pool = get_pool()  
    with pool.connection() as conn:  
        with conn.cursor() as cur: 
            cur.execute('SELECT id, username, email, password FROM users WHERE username = %s OR email = %s', (username, username))  
            user_record = cur.fetchone()  
            
            if user_record:  
                user_id, db_username, clash_name, hashed_password = user_record  
                
                user_bytes = userpass.encode('utf-8')  
                if bcrypt.checkpw(user_bytes, hashed_password.encode('utf-8')):  
                    return True, user_id, db_username, clash_name
            return False, None, None, 'Invalid username or password'
        
def user_data(email: str):   
    pool = get_pool()  
    with pool.connection() as conn:  
        with conn.cursor() as cur:   
            cur.execute('SELECT id, username, email, clan_tag FROM users WHERE email = %s', (email,))  
            user_record = cur.fetchone()  
            
            if user_record:  
                user_id, db_username, clash_name, clan_tag = user_record  
                
                return True, user_id, db_username, clash_name, clan_tag
            return False, None, None, 'Invalid username or password', None
            
def existingaccount(name: str) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT EXISTS(
                    SELECT 1
                    FROM users
                    WHERE LOWER(username) = %s
                )""",
                (name,)
            )
            exists = cursor.fetchone()[0]
            return exists
        
def existingemail(name: str) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT EXISTS(
                    SELECT 1
                    FROM users
                    WHERE LOWER(email) = %s
                )""",
                (name,)
            )
            exists = cursor.fetchone()[0]
            return exists
        
            
def existingemail(name: str) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT EXISTS(
                    SELECT 1
                    FROM users
                    WHERE LOWER(email) = %s
                )""",
                (name,)
            )
            exists = cursor.fetchone()[0]
            return exists


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
            
            
def update_user_code(code: int, email: str):  
    pool = get_pool() 
    with pool.connection() as conn:  
        with conn.cursor() as cursor:   
            update_query = """UPDATE users SET code = %s WHERE email = %s;"""  
            cursor.execute(update_query, (code, email))
            conn.commit()
            
            
def check_code(email: str):  
    pool = get_pool()  
    with pool.connection() as conn:  
        with conn.cursor() as cursor:  
            cursor.execute(  
                """SELECT code FROM users WHERE email = %s""",
                (email,)  
            )  
            result = cursor.fetchone()
            return result[0]
            
def update_password(password: str, email: str):  
    pool = get_pool() 
    with pool.connection() as conn:  
        with conn.cursor() as cursor:   
            update_query = """UPDATE users SET password = %s WHERE email = %s;"""  
            cursor.execute(update_query, (password, email))
            conn.commit()