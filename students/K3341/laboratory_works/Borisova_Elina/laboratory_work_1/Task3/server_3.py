import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(4)

with open('index.html', 'r', encoding='utf-8') as file:
    content = file.read()

http_response = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html; charset=utf-8\r\n"
    "Content-Length: {}\r\n"
    "Connection: close\r\n"
    "\r\n"
    "{}"
).format(len(content.encode('utf-8')), content)

while True:
    connection, address = server_socket.accept()
    request = connection.recv(1024).decode('utf-8')
    print(f"Запрос:\n{request}")
    connection.sendall(http_response.encode('utf-8'))
    connection.close()