import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect(('localhost', 8080))

# Отправляем сообщение серверу
sides = input("Enter lengths of a and b: ")
client_socket.sendall(sides.encode())

# Получаем ответ от сервера
response = client_socket.recv(1024)
print(f'Server response: {response.decode()}')

# Закрываем соединение
client_socket.close()