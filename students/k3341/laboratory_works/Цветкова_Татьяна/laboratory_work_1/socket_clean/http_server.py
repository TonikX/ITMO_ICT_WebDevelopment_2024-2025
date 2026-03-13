import socket

HOST = "127.0.0.1"
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"HTTP сервер на http://{HOST}:{PORT}")

while True:
    conn, _ = server.accept()
    conn.recv(1024)

    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n\r\n"
        + html
    )

    conn.send(response.encode("utf-8"))
    conn.close()