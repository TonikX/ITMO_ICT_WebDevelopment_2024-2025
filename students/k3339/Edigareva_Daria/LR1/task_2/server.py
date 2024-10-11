import socket


def find_square(a, h):
    s = a * h
    return s


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(("127.0.0.1", 14900))
socket.listen(5)

print("Сервер запущен и ожидает соединений...")

with socket:
    while True:
        clientsocket, address = socket.accept()
        print(f"Подключен клиент: {address}")

        data = clientsocket.recv(16384).decode("utf-8")
        a, h = map(float, data.split())
        s = find_square(a, h)

        clientsocket.send(str(s).encode())

        print(f"Площадь параллелограмма для a = {a} и h = {h} равна: {s}")

        clientsocket.close()
