import socket

a = input('Введите a: ')
b = input('Введите b: ')
c = input('Введите c: ')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect(('localhost', 8080))

    message = f"{a} {b} {c}"
    client_socket.sendall(message.encode())
    print(f"Отправлено сообщение серверу: {message}")

    data = client_socket.recv(1024)
    print(f"Получено сообщение от сервера: {data.decode()}")
