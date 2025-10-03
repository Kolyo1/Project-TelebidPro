import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import hashlib

def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        dbname="my_app",
        user="my_ussername",
        password="my_password",
    )
    return conn

def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            password_hash VARCHAR(255) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def hash_password(password:str) -> str:
    return hasattr.sha256(password.encode()).hexdigest()

def create_user(email,fName,lName,password):
    try:
        conn = connect_db()
        cur = conn.cursor()
        password_hash = hash_password(password)
        
        cur.execute("""
            INSERT INTO users (email, first_name, last_name, password_hash)
            VALUES (%s, %s, %s, %s)
        """, (email, fName, lName, password_hash))

        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        return("Failed", e)
        return True

def get_user_by_email(email):
    conn = connect_db
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users WHERE email = %s", email)
    user = cur.fetchone()                    
    cur.close()
    conn.close()
    return user

def update_user(email, new_Fname=None, new_Lname=None, new_password = None):
    try:
        conn = connect_db()
        cur = conn.cursor()

        if new_password:
            new_password = hash_password(new_password)

        fields = []
        values = []

        if new_Fname:
            fields.append("Fname = %s")
            values.append(new_Fname)
        if new_Lname:
            fields.append("Lname = %s")
            values.append(new_Fname)
        if new_password:
            fields.append("hash_password = %s")
            values.append(new_password)

        if fields:
            return False

        values.append(email)
        query = f"UPDATE users SET{', '.join(fields)} WHERE email = %s"

        cur.execute(query, tuple(values))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Invalid", e)
        return False