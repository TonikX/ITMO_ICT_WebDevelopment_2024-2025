import socket

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("127.0.0.1", 7777)

try:
    message = "Hello, server"
    clientSock.sendto(message.encode(), server_address)
    print(f"Сообщение отправлено серверу: {message}")

    data, server = clientSock.recvfrom(1024)
    print(f"Ответ от сервера: {data.decode()}")
except Exception as clientExc:
    print(f"Ошибка: {clientExc}")
finally:
    clientSock.close()
    print("Клиент завершил работу.")
