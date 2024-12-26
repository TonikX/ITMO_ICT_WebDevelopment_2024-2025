import socket

HOST = '127.0.0.1'
PORT = 4000
BUFFER_SIZE = 1024

with open('index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

response_headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Сервер запущен!")

while True:
    client_connection, client_address = server_socket.accept()
    client_connection.recv(BUFFER_SIZE)
    client_connection.sendall(response_headers.encode('utf-8') + html_content.encode('utf-8'))
    client_connection.close()
