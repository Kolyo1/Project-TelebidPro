import re

def validate_email(email:str) -> bool:
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_name(name:str) -> bool:
    if not name:
        return False
    pattern = r'^[A-Za-zА-Яа-я]{2,50}$'
    return re.search(pattern, name) is not None

def validate_password(password:str) -> bool:
    if len(password) < 6:
        return False
    if not re.search(r'[A-Za-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*]', password):
        return False
    return True
    
