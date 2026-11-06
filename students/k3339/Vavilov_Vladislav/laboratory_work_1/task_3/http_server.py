import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 8080))
server.listen(5)

print("HTTP-сервер запущен: http://127.0.0.1:8080")

while True:
    conn, address = server.accept()

    with conn:
        request = conn.recv(4096).decode("utf-8", errors="replace")
        print("Запрос:", request.splitlines()[0] if request else "")

        with open("index.html", "rb") as file:
            content = file.read()

        headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(content)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        conn.sendall(headers.encode("utf-8") + content)