import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8080)
server.bind(server_address)
server.listen(1)

while True:
    connection, client_address = server.accept()
    try:
        print(f"Подключен клиент: {client_address}")

        request = connection.recv(1024).decode()
        print("Получен запрос:\n", request)

        with open('index.html', 'r') as f:
            html_content = f.read()

        http_response = f"HTTP/1.1 200 OK\r\n" \
                        f"Content-Type: text/html; charset=UTF-8\r\n" \
                        f"Content-Length: {len(html_content)}\r\n" \
                        f"\r\n" \
                        f"{html_content}"

        connection.sendall(http_response.encode())
    finally:
        connection.close()