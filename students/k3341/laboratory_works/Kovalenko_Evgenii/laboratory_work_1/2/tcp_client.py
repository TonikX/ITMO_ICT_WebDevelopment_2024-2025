from socket import socket, AF_INET, SOCK_STREAM

# Создаем TCP-сокет
# используем AF_INET, чтобы работать с IP-адресами (IPv4), и SOCK_DGRAM для использования протокола TCP
client_socket = socket(AF_INET, SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect(('localhost', 8080))

# Запрашиваем данные у пользователя
print("Вычисление площади параллелограмма")
base1 = input("Введите длину стороны: ")
base2 = input("Введите длину смежной с ней стороны: ")
alpha = input("Введите угол между сторонами в градусах: ")

# Формируем и отправляем сообщение серверу
message = f"{base1} {base2} {alpha}"
client_socket.sendall(message.encode())
print(f"Отправлено серверу: {message}")

# Получаем ответ от сервера
response = client_socket.recv(1024).decode()
print(f"Ответ от сервера: {response}")

# Закрываем соединение
client_socket.close()
