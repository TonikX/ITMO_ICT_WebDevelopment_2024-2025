import socket
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = 'localhost'
PORT = 8080
BUFF_SIZE = 2048
file_path = 'index.html'

server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("HTTP server is running on", HOST, ':', PORT)
print(f'http://{HOST}:{PORT}')

while True:
    try:
        client_connection, client_address = server_socket.accept()
        print('Connection from: ', client_address)

        request = client_connection.recv(BUFF_SIZE).decode()
        print("Request:", request)

        file = open(file_path, 'r', encoding='utf-8')
        content = file.read()

        # Формируем HTTP-ответ
        http_response = (
            "HTTP/1.1 200 OK\r\n"
            f"Host: {HOST}\r\n"
            f"Content-Type: text/html; charset=UTF-8\r\n"
            f"Content-Length: {len(content)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode() + content.encode()

        client_connection.sendall(http_response)

    except KeyboardInterrupt:
        server_socket.close()
        break

