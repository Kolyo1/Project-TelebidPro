import pytest
from app.db import create_user, check_credentials, get_user_by_email, update_user

@pytest.fixture
def unit_user():
    email = "unit@example.com"
    create_user(email, "Unit", "Test", "Abc123!")
    yield email
    # Optionally clean up after test
    # from app.db import db_connect
    # conn = db_connect()
    # cur = conn.cursor()
    # cur.execute("DELETE FROM users WHERE email = %s;", (email,))
    # conn.commit()
    # cur.close()
    # conn.close()

def test_create_user():
    result = create_user("unit@example.com", "Unit", "Test", "Abc123!")
    assert result is True

def test_get_user_by_email(unit_user):
    user = get_user_by_email(unit_user)
    assert user is not None
    assert user[1] == "unit@example.com"
    assert user[2] == "Unit"

def test_check_credentials_valid(unit_user):
    assert check_credentials(unit_user, "Abc123!")

def test_check_credentials_invalid(unit_user):
    assert not check_credentials(unit_user, "wrongpass")

def test_update_user(unit_user):
    result = update_user(unit_user, "Updated", None, None)
    assert result is True