import socket

server_address = ('localhost', 8080)

# Создание TCP-сокета
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Подключение к серверу
    sock.connect(server_address)

    a = input("Введите длину первого основания трапеции: ")
    b = input("Введите длину второго основания трапеции: ")
    h = input("Введите высоту трапеции: ")

    # Отправка данных на сервер
    message = f'{a},{b},{h}'
    sock.sendall(message.encode())
    print(f'Отправлены данные: основание 1 = {a}, основание 2 = {b}, высота = {h}')

    # Ожидание и получение результата от сервера
    data = sock.recv(1024)
    print(f'Получен результат от сервера: Площадь трапеции = {data.decode()}')

finally:
    sock.close()