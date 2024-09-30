import socket

# Создаем UDP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(('localhost', 8080))

print("Сервер запущен на порту 8080 и ожидает сообщений...")

while True:
    message, client_address = server_socket.recvfrom(1024)
    print(f"Получено сообщение от клиента: {message.decode('utf-8')}")

    reply_message = "Hello, client"
    server_socket.sendto(reply_message.encode('utf-8'), client_address)
    print(f"Ответ отправлен клиенту: {reply_message}")