import socket
import math

HOST = "127.0.0.1"
PORT = 50001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
server.settimeout(0.5)  # чтобы accept() не блокировал Ctrl+C навсегда
print(f"TCP-сервер запущен на {HOST}:{PORT}")

try:
    while True:
        try:
            conn, address = server.accept()
        except socket.timeout:
            continue

        print(f"Подключился клиент {address}")

        data = conn.recv(1024).decode()
        a, b = map(float, data.split())
        c = math.sqrt(a ** 2 + b ** 2)
        print(f"Катеты: {a}, {b} -> гипотенуза: {c}")

        conn.send(str(c).encode())
        conn.close()
except KeyboardInterrupt:
    print("\nСервер остановлен")
finally:
    server.close()
