import socket

host = 'localhost'
port = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((host, port))

# Ждем входящие соединение
server_socket.listen(5)
print(f"HTTP-сервер запущен на {host}:{port}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Новое подключение от {client_address}")

    with open("index.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    response = (
        "HTTP/1.1 200 OK\n"
        "Content-Type: text/html; charset=utf-8\n"
        "Content-Length: {}\n\n{}".format(len(html_content.encode("utf-8")), html_content)
    )

    client_socket.sendall(response.encode())

    client_socket.close()