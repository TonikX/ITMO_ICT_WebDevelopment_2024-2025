from socket import socket, AF_INET, SOCK_DGRAM

# Создаем UDP-сокет
# используем AF_INET, чтобы работать с IP-адресами (IPv4), и SOCK_DGRAM для использования протокола UDP
server_socket = socket(AF_INET, SOCK_DGRAM)

# Привязываем сокет к адресу и порту
server_address = ('localhost', 8080)
server_socket.bind(server_address)

print("Сервер запущен и ожидает сообщения...")

while True:
    # Получаем данные и адрес клиента
    data, client_address = server_socket.recvfrom(1024)
    message = data.decode('utf-8')

    print(f"Получено сообщение от {client_address}: {message}")

    if message == "Hello, server":
        # Отправляем ответ клиенту
        response = "Hello, client"
        server_socket.sendto(response.encode('utf-8'), client_address)
        print(f"Отправлен ответ: {response}")
