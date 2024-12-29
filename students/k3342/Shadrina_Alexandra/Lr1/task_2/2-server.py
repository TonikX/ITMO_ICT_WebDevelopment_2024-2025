import socket


def calculate_square(a, b, h):
    return (a + b) * h / 2


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)
print("Сервер запущен на порту 8080...")

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    request = client_connection.recv(1024).decode()
    print(f'Запрос от клиента: {request}')

    if not request:
        print('Данные не получены')
        client_connection.close()
        continue

    try:
        a, b, h = map(float, request.split(','))
        square = calculate_square(a, b, h)
        response = f'площадь трапеции {square}'
    except ValueError:
        response = 'Ошибка: некорректные данные.'

    print(f'Ответ: {response}')

    client_connection.sendall(response.encode())

    client_connection.close()
