import psycopg2
import bcrypt
import os

def db_connect():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "telebidpro"),
        user=os.getenv("DB_USER", "prom4"),
        password=os.getenv("DB_PASS", ""),
        host="localhost"
    )

def create_user(email, first_name, last_name, password):
    try:
        conn = db_connect()
        cur = conn.cursor()
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        cur.execute(
            "INSERT INTO users (email, first_name, last_name, password) VALUES (%s, %s, %s, %s)",
            (email, first_name, last_name, hashed)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error creating user:", e)
        return False

def check_credentials(email, password):
    try:
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE email = %s", (email,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if not result:
            return False
        stored_hash = result[0]  # string from VARCHAR
        match = bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))
        return match
    except Exception as e:
        print("Error checking credentials:", e)
        return False

def update_user(email, new_Fname=None, new_Lname=None, new_password=None):
    try:
        conn = db_connect()
        cur = conn.cursor()
        fields = []
        values = []
        if new_Fname:
            fields.append("first_name = %s")
            values.append(new_Fname)
        if new_Lname:
            fields.append("last_name = %s")
            values.append(new_Lname)
        if new_password:
            hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            fields.append("password = %s")
            values.append(hashed)
        if not fields:
            return False
        query = f"UPDATE users SET {', '.join(fields)} WHERE email = %s"
        values.append(email)
        cur.execute(query, tuple(values))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Update user error:", e)
        return False

def get_user_by_email(email):
    try:
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user
    except Exception as e:
        print("Select error:", e)
        return None