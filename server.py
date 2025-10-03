from app.auth import validate_email, validate_name, validate_password

email = data.get("email")
password = data.get("password")
fName = data.get("first_name")
lName = data.get("last_name")

if not validate_email(email):
    return error("Invalid email.")

if not validate_name(fName):
    return error("Invalid First Name")

if not validate_name(lName):
    return error("Invalid Last Name")

if not validate_password(password):
    return error("Invalid Password")