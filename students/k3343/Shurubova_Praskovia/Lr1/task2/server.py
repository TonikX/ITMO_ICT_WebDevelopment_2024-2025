import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8080))

server_socket.listen(1)
print("Сервер запущен на порту 8080...")

while True:
    client_connection, client_address = server_socket.accept()
    client_connection.send(
        "Введите сначала сторону, к которой проведена высота,"
        "а затем - высоту".encode()
    )
    request = client_connection.recv(1024).decode()
    try:
        a, h = map(float, request.split())
        square = a * h
        response = f'Площадь паралелограмма равна: {square:.2f}'
    except ValueError:
        response = "Ошибка: введите в каждой строке только одно число."

    client_connection.sendall(response.encode())

    client_connection.close()