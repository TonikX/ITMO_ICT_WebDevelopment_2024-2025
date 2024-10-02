import socket

# Создаем TCP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу (например, localhost и порт 8080)
server_address = ('localhost', 8080)
client_socket.connect(server_address)

# Формируем простой HTTP-запрос
http_request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"

# Отправляем запрос на сервер
client_socket.sendall(http_request.encode('utf-8'))

# Получаем ответ от сервера
response = client_socket.recv(4096).decode('utf-8')

# Выводим ответ
print(response)

# Закрываем соединение
client_socket.close()
