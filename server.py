from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from app.auth import validate_email, validate_name, validate_password
from app.db import create_user, check_credentials, update_user
from app.captcha import generate_captcha

Host = "localhost"
Port = 8800

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        user = self.get_logged_user()

        if self.path == "/":
            self.render_html("index.html")

        elif self.path == "/register":
            if user:
                self.send_response(302)
                self.send_header("Location", "/")
                self.end_headers()
            else:
                question, answer = generate_captcha()
                self.send_response(200) 
                self.send_header("Content-type", "text/html; charset=UTF-8")
                self.send_header("Set-Cookie", f"captcha_answer={answer}; Path=/")
                self.end_headers()
                with open("templates/register.html", "r", encoding="UTF-8") as f:
                    html = f.read()
                html = html.replace("{CAPTCHA_QUESTION}", question)
                self.wfile.write(html.encode("UTF-8"))


        elif self.path == "/login":
            if user:
                self.send_response(302)
                self.send_header("Location", "/")
                self.end_headers()
            else:
                question, answer = generate_captcha()
                self.send_response(200) 
                self.send_header("Content-type", "text/html; charset=UTF-8")
                self.send_header("Set-Cookie", f"captcha_answer={answer}; Path=/")
                self.end_headers()
                with open("templates/login.html", "r", encoding="UTF-8") as f:
                    html = f.read()
                html = html.replace("{CAPTCHA_QUESTION}", question) 
                self.wfile.write(html.encode("UTF-8"))


        elif self.path == "/logout":
            self.send_response(302)
            self.send_header("Location", "/")
            self.send_header("Set-Cookie", "user_email=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT")
            self.end_headers()

        elif self.path == "/profile":
            user = self.get_logged_user()
            if not user:
                self.send_response(302)
                self.send_header("Location", "/login")
                self.end_headers()
            else:
                self.render_html("templates/profile.html")
        else:
            self.send_error(404, "Not existing")

    def render_html(self, path, captcha_question = None):
        try:
            with open(path, "r", encoding="UTF-8") as f:
                html = f.read()
            if captcha_question:
                html = html.replace("CAPTCHA_QUESTION", captcha_question)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()
            self.wfile.write(html.encode("UTF-8"))
        except:
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()
            self.wfile.write(b"<h1>404 - Not Found</h1>")

    def get_logged_user(self):
            cookie = self.headers.get("Cookie")
            if not cookie:
                return None
            for part in cookie.split(";"):
                key, _, value = part.strip().partition("=")
                if key == "user_email":
                    return value
            return None

    def do_POST(self):
        if self.path == "/register":
            self.handle_register()
        elif self.path == "/login":
            self.handle_login()
        elif self.path == "/profile":
            user = self.get_logged_user()
            if not user:
                self.send_response(302)
                self.send_header("Location", "/login")
                self.end_headers()
                return

            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")
            data = urllib.parse.parse_qs(post_data)

            new_Fname = data.get("first_name", [""])[0]
            new_Lname = data.get("last_name", [""])[0]
            new_password = data.get("password", [""])[0]

            if not new_Fname and not new_Lname and not new_password:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=UTF-8")
                self.end_headers()
                self.wfile.write(b"<h3>No changes made.</h3>")
                return

            success = update_user(user, new_Fname if new_Fname else None,  new_Lname if new_Lname else None,new_password if new_password else None)

            if success:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=UTF-8")
                self.end_headers()
                self.wfile.write(b"<h2>Profile updated successfully!</h2><a href='/'>Go back</a>")
            else:
                self.send_response(500)
                self.send_header("Content-type", "text/html; charset=UTF-8")
                self.end_headers()
                self.wfile.write(b"<h2>Error updating profile!</h2>")
        else:
            self.send_error(404, "Invalid POST endpoint")


    def handle_register(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("UTF-8")
        data = urllib.parse.parse_qs(post_data)

        email = data.get("email", [""])[0]
        password = data.get("password", [""])[0]
        fName = data.get("fName", [""])[0]
        lName = data.get("lName", [""])[0]
        captcha_input = data.get("captcha_input", [""])[0]

        cookies = self.headers.get("Cookie", "")
        captcha_answer = None
        for c in cookies.split(";"):
            k, _, v = c.strip().partition("=")
            if k == "captcha_answer":
                captcha_answer = v

        if not captcha_answer or int(captcha_input) != int(captcha_answer):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()
            self.wfile.write(b"<h2>Incorrect CAPTCHA!</h2>")
            return

        errors = []

        if not validate_name(fName):
            errors.append("Invalid First Name")
        if not validate_name(lName):
            errors.append("Invalid Last Name")
        if not validate_email(email):
            errors.append("Invalid Email")
        if not validate_password(password):
            errors.append("Invalid Password")

        if errors:
            message = "<br>".join(errors)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()
            self.wfile.write(f"<h2>Error:</h2><p>{message}</p>".encode("utf-8"))
            return

        if create_user(email, fName, lName, password):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()
            self.wfile.write(b"<h2>Registration Successful!</h2><a href='/login'>Go to Login</a>")
        else:
            self.send_response(500)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()
            self.wfile.write(b"<h2>Database Error!</h2>")

    def handle_login(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("UTF-8")
        data = urllib.parse.parse_qs(post_data)

        email = data.get("email", [""])[0]
        password = data.get("password", [""])[0]
        captcha_input = data.get("captcha_input", [""])[0]

        cookies = self.headers.get("Cookie", "")
        captcha_answer = None
        for c in cookies.split(";"):
            k, _, v = c.strip().partition("=")
            if k == "captcha_answer":
                captcha_answer = v

        if not captcha_answer or int(captcha_input) != int(captcha_answer):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()
            self.wfile.write(b"<h2>Incorrect CAPTCHA!</h2>")
            return

        if check_credentials(email, password):
            self.send_response(302)
            self.send_header("Location", "/")
            self.send_header("Set-Cookie", f"user_email={email}; Path=/; HttpOnly")
            self.end_headers()
        else:
            self.send_response(401)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()
            self.wfile.write(b"<h2>Invalid email or password!</h2>")



server = HTTPServer((Host,Port), MyHandler)
print(f"Works : /{Host} {Port}")
server.serve_forever()