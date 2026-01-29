import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    msg = "Hello, server!"
    s.sendto(msg.encode(), ('localhost', 8080))
    print(f"Отправлено сообщение серверу: {msg}")

    data, server = s.recvfrom(1024)
    print(f"Получено сообщение от сервера: {data.decode()}")