from datetime import date
from app.db.connection import get_connection


# add new user to bot databse
def addUser(userid):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
        INSERT INTO userTb (user_id)
        VALUES (%s)
        ON CONFLICT (user_id) DO NOTHING;
        """, (userid,))

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
    
        cur.close()
        conn.close()

#check if user exists in database or not
def user_exists(userId):

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT 1 FROM userTb WHERE user_id = %s;",
            (userId,)
        )
        return cur.fetchone() is not None
    finally:
        cur.close()
        conn.close()

#increase count of confession in userTb
def incCount(userId):

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "UPDATE userTb SET count = count + 1 WHERE  user_id = %s;",
            (userId,)
        )

        conn.commit()
    except Exception as e:
         conn.rollback()
         raise e
    finally:
        cur.close()
        conn.close()

#fetch user count(confesssion) from database 
def check(userid):

    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
        SELECT count FROM userTb WHERE user_id = %s;
        """, (userid,))

        row = cur.fetchone()
        return row
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

#reset count of user
def reset_count():

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
         UPDATE userTb
        SET
        count = 0;
        """)

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e
    finally:
    
        cur.close()
        conn.close()