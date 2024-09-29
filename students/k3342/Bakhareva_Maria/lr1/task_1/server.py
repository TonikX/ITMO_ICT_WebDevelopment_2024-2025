import socket

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу и порту
server_address = ('localhost', 12345)
server_socket.bind(server_address)

print("Сервер запущен и ожидает сообщения...")

try:
    while True:
        # Получаем данные от клиента
        data, client_address = server_socket.recvfrom(1024)
        print(f"Получено сообщение от клиента: {data.decode()}")

        # Отправляем ответ клиенту
        response = "Hello, client"
        server_socket.sendto(response.encode(), client_address)
except KeyboardInterrupt:
    print("\nСервер остановлен.")
finally:
    server_socket.close()
