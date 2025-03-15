import socket

HOST = 'localhost'
PORT = 8081

html_file = 'index.html'


def create_http_response(html_content):
    response = 'HTTP/1.1 200 OK\r\n'
    response += 'Content-Type: text/html\r\n'
    response += 'Content-Length: {}\r\n'.format(len(html_content))
    response += 'Connection: close\r\n'
    response += '\r\n'
    response += html_content
    return response


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Сервер запущен на {HOST}:{PORT}...")

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    request = client_connection.recv(1024).decode()
    print(f'Запрос от клиента: {request}')

    try:
        with open(html_file, 'r') as file:
            html_content = file.read()

        http_response = create_http_response(html_content)
    except FileNotFoundError:
        http_response = 'HTTP/1.1 404 NOT FOUND\r\n'
        http_response += 'Content-Type: text/html\r\n'
        http_response += '\r\n'
        http_response += '<html><body><h1>404 Not Found</h1></body></html>'

    client_connection.sendall(http_response.encode())
    client_connection.close()

