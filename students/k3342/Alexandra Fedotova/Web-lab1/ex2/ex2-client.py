import socket

# Настройки клиента
SERVER_IP = 'localhost'  # Соединение с сервером по localhost
SERVER_PORT = 8080
BUFFER_SIZE = 1024

# Создаем TCP сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect((SERVER_IP, SERVER_PORT))

# Ввод параметров с клавиатуры
base = input("Введите основание параллелограмма: ")
height = input("Введите высоту параллелограмма: ")

# Отправляем параметры на сервер
client_socket.send(f"{base},{height}".encode())

# Получаем и выводим результат от сервера
result = client_socket.recv(BUFFER_SIZE).decode()
print(f"Результат от сервера: Площадь параллелограмма = {result}")

# Закрываем сокет
client_socket.close()
