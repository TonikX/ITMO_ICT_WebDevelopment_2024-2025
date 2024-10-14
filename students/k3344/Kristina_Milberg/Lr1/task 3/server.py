import socket
import os

HOST = 'localhost'
PORT = 9091

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"HTTP сервер запущен на http://{HOST}:{PORT}...")

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    request = client_connection.recv(1024).decode()
    print(f'Запрос клиента:\n{request}')

    requested_file = request.split()[1][1:]
    if requested_file == '':
        requested_file = 'index.html'

    try:
        if os.path.isfile(requested_file):
            with open(requested_file, 'rb') as file:
                content = file.read()
            http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=UTF-8\r\n"
                f"Content-Length: {len(content)}\r\n"
                "Connection: close\r\n"
                "\r\n"
            ).encode() + content
        else:
            html_content = "<h1>404 Not Found</h1><p>Страница не найдена.</p>"
            http_response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html; charset=UTF-8\r\n"
                f"Content-Length: {len(html_content)}\r\n"
                "Connection: close\r\n"
                "\r\n" + html_content
            ).encode()
    except Exception as e:
        print(e)
        http_response = (
            "HTTP/1.1 500 Internal Server Error\r\n"
            "Content-Type: text/html; charset=UTF-8\r\n"
            "Connection: close\r\n"
            "\r\n"
            "<h1>500 Internal Server Error</h1>"
        ).encode()

    client_connection.sendall(http_response)
    client_connection.close()