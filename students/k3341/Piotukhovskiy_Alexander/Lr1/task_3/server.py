import os
import socket

HOST = "localhost"
PORT = 8080
MAX_CONNECTIONS = 10
BUFFER_SIZE = 1024


def load_html_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.read()
    else:
        return None


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(MAX_CONNECTIONS)
print("Server is running")

while True:
    client, _ = server.accept()
    client.recv(BUFFER_SIZE)

    html = load_html_file("index.html")
    if html is not None:
        response = (
            (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(html)}\r\n"
                    "\r\n"
                    + html
            )
        )
    else:
        response = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "\r\n"
            "<h1>404 Not Found</h1>"
        )
    client.sendall(response.encode())
