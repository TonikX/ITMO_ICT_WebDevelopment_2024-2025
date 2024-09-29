import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Адрес сервера
server_address = ('localhost', 12345)

try:
    # Отправляем сообщение серверу
    message = "Hello, server"
    client_socket.sendto(message.encode(), server_address)

    # Получаем ответ от сервера
    data, _ = client_socket.recvfrom(1024)
    print(f"Получено сообщение от сервера: {data.decode()}")
except KeyboardInterrupt:
    print("\nКлиент остановлен.")
finally:
    client_socket.close()
