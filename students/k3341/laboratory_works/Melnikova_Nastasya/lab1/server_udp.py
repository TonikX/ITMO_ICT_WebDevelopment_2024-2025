import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # создаём UDP сокет

sock.bind(("127.0.0.1", 12345)) # привязываем его к локальному адресу и порту

print("UDP сервер запущен и ждёт сообщений...")

while True:
    data, addr = sock.recvfrom(1024)  # ждём сообщение от клиента, 1024 — максимальный размер пакета

    print("Получено:", data.decode(), "от", addr)

    sock.sendto("Hello, client".encode(), addr) # отвечаем клиенту
