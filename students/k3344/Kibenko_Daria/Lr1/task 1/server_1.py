import socket

# Создаем UDP-сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 12345))

print("Сервер запущен и ожидает сообщений...")

while True:
    # Получаем сообщение от клиента
    data, addr = sock.recvfrom(1024)
    print(f"Получено сообщение от {addr}: {data.decode()}")

    # Отправляем ответ клиенту
    response = "Hello, client"
    sock.sendto(response.encode(), addr)