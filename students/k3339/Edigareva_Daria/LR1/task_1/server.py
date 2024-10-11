import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 12345)
server_socket.bind(server_address)

print("Сервер готов к приему сообщений...")

with server_socket:
    while True:
        message, client_address = server_socket.recvfrom(1024)
        print(f"Получено сообщение от клиента: {message.decode()}")

        response_message = "Hello, client"
        server_socket.sendto(response_message.encode(), client_address)
        print(f"Ответ отправлен клиенту: {response_message}")
