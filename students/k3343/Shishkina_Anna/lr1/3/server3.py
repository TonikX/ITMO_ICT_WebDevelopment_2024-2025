import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8080))

server_socket.listen(5)
print("Сервер запущен")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Подключен клиент: {client_address}")

    request = client_socket.recv(1024).decode('utf-8')
    print(f"Запрос: {request}")

    try:
        with open('index.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        http_response = (
            "HTTP/1.1 200 OK\n"
            "Content-Type: text/html; charset=utf-8\n"
            "Content-Length: {}\n"
            "Connection: close\n"
            "\n"
            "{}"
        ).format(len(html_content), html_content)
    except FileNotFoundError:
        http_response = (
            "HTTP/1.1 404 Not Found\n"
            "Content-Type: text/html; charset=utf-8\n"
            "Connection: close\n"
            "\n"
            "<h1>404 Not Found</h1>"
        )

    client_socket.sendall(http_response.encode('utf-8'))

    client_socket.close()