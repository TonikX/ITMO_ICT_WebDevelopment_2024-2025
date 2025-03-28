import socket

clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("127.0.0.1", 7777)
clientSock.connect(server_address)

try:
    print("Ввод параметров трапеции.")
    a = input("Введите a: ")
    b = input("Введите b: ")
    h = input("Введите h: ")

    message = f"{a} {b} {h}"
    clientSock.sendall(message.encode())
    print(f"Отправлено сообщение серверу: {message}")

    data = clientSock.recv(1024).decode()
    print(f"Ответ от сервера: {data}")
finally:
    clientSock.close()
    print("Клиент завершил работу.")
