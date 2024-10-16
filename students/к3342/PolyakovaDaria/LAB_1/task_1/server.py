import socket

HOST = 'localhost'
PORT = 8080

# Создаем сокет для UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу и порту
server_socket.bind((HOST, PORT))

print(f"UDP сервер запущен на {HOST}:{PORT}...")

while True:
    # Получаем сообщение от клиента
    message, client_address = server_socket.recvfrom(1024)
    print(f"Сообщение от клиента: {message.decode()}")

    # Отправляем ответ клиенту
    response = "Hello, client"
    server_socket.sendto(response.encode(), client_address)