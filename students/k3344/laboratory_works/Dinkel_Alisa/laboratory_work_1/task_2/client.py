import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect(('localhost', 8080))

# Запрашиваем у пользователя параметры для вычисления площади
a = input("Введите основание параллелограмма: ")
h = input("Введите высоту параллелограмма: ")

# Отправляем сообщение серверу
message = f"{a} {h}"
client_socket.sendall(message.encode())

# Получаем ответ от сервера
response = client_socket.recv(1024)
print(f'Ответ от сервера: {response.decode()}')

# Закрываем соединение
client_socket.close()
