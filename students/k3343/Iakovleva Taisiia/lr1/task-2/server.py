import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8080))

server_socket.listen(1)
print("Сервер запущен на порту 8080...")

while True:

    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    request = client_connection.recv(1024).decode()
    print(f'Запрос от клиента: {request}')

    a, b = map(float, request.split())

    c = (a ** 2 + b ** 2) ** 0.5
    response = f"Гипотенуза: {c:.2f}"
    client_connection.sendall(response.encode())

    client_connection.close()
