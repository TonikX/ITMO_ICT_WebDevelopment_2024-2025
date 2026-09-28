import socket

HOST = "127.0.0.1"
PORT = 50002

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
server.settimeout(0.5)  # чтобы accept() не блокировал Ctrl+C навсегда
print(f"HTTP-сервер запущен на http://{HOST}:{PORT}")

try:
    while True:
        try:
            conn, address = server.accept()
        except socket.timeout:
            continue

        print(f"Подключился клиент {address}")

        request = conn.recv(1024) # запрос браузера не нужен, просто вычитываем его

        with open("index.html", "rb") as file:
            body = file.read()

        headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n"
        ).encode()

        conn.sendall(headers + body)
        conn.close()
except KeyboardInterrupt:
    print("\nСервер остановлен")
finally:
    server.close()
