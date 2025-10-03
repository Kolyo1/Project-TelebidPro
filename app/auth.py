import re
def validate_email(email:str) -> bool:
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_name(name:str) -> bool:
    if not name:
        return False
    pattern = r'^[A-Za-zА-Яа-я]{2,50}$'
    return not re.search(pattern, name) is not None

def validate_password(password:str) -> bool:
    if(len(password) < 8):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*]', password):
        return False
    
