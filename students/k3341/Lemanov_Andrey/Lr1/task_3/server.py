import socket

HOST, PORT = '127.0.0.1', 8000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f'Serving on http://{HOST}:{PORT}')

while True:
    connection, address = server_socket.accept()
    print(f'Connection from {address}')

    request = connection.recv(1024).decode()
    print(f'Request: {request}')

    try:
        filename = 'index.html'

        with open(filename, 'rb') as f:
            response_data = f.read()

        response_headers = 'HTTP/1.1 200 OK\n'
        response_headers += 'Content-Type: text/html\n'
        response_headers += 'Content-Length: {}\n\n'.format(len(response_data))

    except FileNotFoundError:
        response_headers = 'HTTP/1.1 404 Not Found\n\n'
        response_data = b'<html><body><h1>404 Not Found</h1></body></html>'
    connection.sendall(response_headers.encode() + response_data)
    connection.close()
