#for db operations means table create etc

from app.db.connection import get_connection

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS userTb (
            user_id BIGINT PRIMARY KEY,
            count INT DEFAULT 0,
            last_confess_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()

    cur.close()
    conn.close()
