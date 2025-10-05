import sys
import os
import pytest
from app.db import db_connect, create_user

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(autouse=True)
def clear_users_table(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM users;")
    db_connection.commit()
    cursor.close()

@pytest.fixture(scope="session")
def db_connection():
    conn = db_connect()
    yield conn
    conn.close()


@pytest.fixture
def test_user(db_connection):
    email = "testuser@example.com"
    f_name = "Test"
    l_name = "User"
    password = "Password123!"
    
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM users WHERE email = %s;", (email,))
    db_connection.commit()

    create_user(email, f_name, l_name, password)

    yield {"email": email, "password": password}

    cursor.execute("DELETE FROM users WHERE email = %s;", (email,))
    db_connection.commit()
