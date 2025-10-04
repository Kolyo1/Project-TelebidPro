import psycopg2
from psycopg2 import sql

DB_NAME = "telebidpro"
DB_USER = "prom4"   
DB_PASS = "your_password" 
DB_HOST = "localhost"
DB_PORT = "5432"

def db_connect():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )


def create_user(email, first_name, last_name, password):
    try:
        conn = db_connect()
        cur = conn.cursor()
        query = """
            INSERT INTO users (email, first_name, last_name, password)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(query, (email, first_name, last_name, password))
        conn.commit()
        cur.close()
        conn.close()
        print("✅ User created successfully!")
        return True
    except Exception as e:
        print("Database error:", e)
        return False


def update_user(email, new_Fname =None, new_Lname = None,new_password = None):
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
            fields.append("password = %s")
            values.append(new_password)
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
    
def check_credentials(email, password):
    try:
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE email = %s", (email, ))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is None:
            return False
        
        db_password = result[0]
        return db_password == password
    except Exception as e :
        print("Login error: ", e)
        return False
