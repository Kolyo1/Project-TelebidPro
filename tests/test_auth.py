import pytest
from app.auth import validate_email, validate_name, validate_password

def test_validate_email_valid():
    assert validate_email("testexam@ple.com")

def test_validate_email_invalid():
    assert not validate_email("Invalid Email.")

def test_validate_first_name_valid():
    assert validate_name("Test")

def test_validate_first_name_invalid():
    assert not validate_name("123Test")

def test_validate_last_name_valid():
    assert validate_name("Last")

def test_validate_last_name_invalid():
    assert not validate_name("123Last")

def test_validate_password_valid():
    assert validate_password("Testpassword1*")

def test_validate_password_too_short():
    assert not validate_password("Test")