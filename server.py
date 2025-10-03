from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from app.auth import validate_email, validate_name, validate_password
from app.db import create_user

Host = "localhost"
Port = 8800

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=="/":
            try:
                with open("templates/register.html", "r", encoding="UTF-8") as f:
                    html = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=UTF-8")
                self.end_headers()
                self.wfile.write(html.encode("UTF-8"))
            except:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"<h1>404 - Not Found</h1>")
        else:
            self.send_error(404, "Not existing")

    def do_POST(self):
        if self.path == "/register":
            content_length = int(self.headers("Content-Length"))
            post_data = self.rfile.read(content_length).decode("UTF-8")
            data = urllib.parse.parse_qs(post_data)

            email = data.get("email", [""])[0]
            password = data.get("password", [""])[0]
            fName = data.get("fName", [""])[0]
            lName = data.get("lName", [""])[0]

            errors = []

            if not validate_name(fName):
                errors.append("Invalid First Name")
                
            if not validate_name(lName):
                errors.append("Invalid Last Name")

            if not validate_email(email):
                errors.append("Invalid email.")

            if not validate_password(password):
                errors.append("Invalid Password")
            
            if errors: 
                message = "<br>".join(errors)
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=UTF-8")
                self.end_headers()
                self.wfile.write(f"<h2>Error registration : </h2> <p>{message}</p>".encode("utf-8"))
                return
            
            if create_user(email,fName,lName,password):
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=UTF-8")
                self.end_headers()
                self.wfile.write(b"<h2>Succeed</h2>")
            else:
                self.send_response(500)
                self.send_header("Content-type", "text/html; charset=UTF-8")
                self.end_headers()
                self.wfile.write(b"<h2>Error in database</h2>")


server = HTTPServer((Host,Port), MyHandler)
print(f"Works : /{Host} {Port}")
server.serve_forever()