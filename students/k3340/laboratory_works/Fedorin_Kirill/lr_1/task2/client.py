import socket


def start_client() -> None:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    client_socket.connect(server_address)

    print('Введите коэффициенты квадратного уравнения ax^2 + bx + c = 0')
    a = input('Введите a: ')
    b = input('Введите b: ')
    c = input('Введите c: ')

    # Отправляем коэффициенты на сервер в формате "a,b,c"
    message = f'{a},{b},{c}'
    client_socket.send(message.encode())

    # Получаем ответ от сервера
    result = client_socket.recv(1024).decode()
    print(f'Результат: {result}')

    client_socket.close()


if __name__ == '__main__':
    start_client()
