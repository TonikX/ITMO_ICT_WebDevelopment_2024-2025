import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))

server_socket.listen(1)

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()
    print(f'The parametrs of the parallelogram: {request}')

    response = float(request.split(' ')[0]) * float(request.split(' ')[1]) * 0.5
    print(f'The area of the parallelogram: {response}')
    client_connection.sendall(str(response).encode())

    client_connection.close()