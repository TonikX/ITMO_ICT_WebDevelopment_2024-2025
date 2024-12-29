import socket

# Создаем TCP-клиент
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

a = input("Введите длину катета a: ")
b = input("Введите длину катета b: ")

# Отправляем данные на сервер
client_socket.send(f"{a},{b}".encode())

# Получаем результат от сервера
result = client_socket.recv(1024).decode()
print(f"Ответ от сервера: {result}")

# Закрываем соединение
client_socket.close()
