import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect(('localhost', 8080))

# Вводим данные для теоремы Пифагора
a = input("Введите длину первого катета (a): ")
b = input("Введите длину второго катета (b): ")

# Формируем запрос серверу
request = f"{a} {b}"
client_socket.sendall(request.encode())

# Получаем ответ от сервера
response = client_socket.recv(1024)
print(f'Ответ от сервера: {response.decode()}')

# Закрываем соединение
client_socket.close()
