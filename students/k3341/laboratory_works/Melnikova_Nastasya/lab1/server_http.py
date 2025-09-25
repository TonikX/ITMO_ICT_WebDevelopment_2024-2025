import socket
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 8081))
sock.listen(1)

print("HTTP сервер ждёт подключение на http://127.0.0.1:8081/ ...")

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()
    print("Запрос:\n", request)

    try:
        path = request.split(" ")[1]
    except:
        path = "/"

    if path == "/":
        path = "/index.html"

    file_path = path.lstrip("/")

    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            content = f.read()
        if file_path.endswith(".html"):
            content_type = "text/html"
        elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
            content_type = "image/jpeg"
        else:
            content_type = "application/octet-stream"

        response = f"HTTP/1.1 200 OK\nContent-Type: {content_type}\n\n".encode() + content
    else:
        response = "HTTP/1.1 404 Not Found\nContent-Type: text/plain\n\nФайл не найден".encode()

    conn.send(response)
    conn.close()