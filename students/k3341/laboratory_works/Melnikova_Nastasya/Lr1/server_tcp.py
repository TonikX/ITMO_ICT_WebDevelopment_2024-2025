import socket
import math

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создаём TCP сокет

sock.bind(("127.0.0.1", 12345)) # привязываем к адресу и порту

sock.listen(1) # 1 = сколько подключений в очереди

print("TCP сервер ждёт подключение...")

conn, addr = sock.accept()
print("Подключился:", addr)

while True:
    data = conn.recv(1024).decode()
    if not data:
        break  # если клиент закрыл соединение — выходим

    try:
        a, b = map(float, data.split())
        c = math.sqrt(a**2 + b**2)  # считаем гипотенузу
        conn.send(str(c).encode())  # отправляем обратно
    except:
        conn.send("Ошибка ввода!".encode())

conn.close()