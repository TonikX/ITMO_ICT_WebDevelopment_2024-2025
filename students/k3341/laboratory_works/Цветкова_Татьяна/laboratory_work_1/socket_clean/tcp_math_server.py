import socket
import math

HOST = "127.0.0.1"
PORT = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"TCP math-сервер на {PORT}...")

conn, addr = server.accept()
print("Клиент подключился:", addr)

while True:
    data = conn.recv(1024).decode()
    if not data:
        break

    parts = data.split()
    cmd = parts[0].upper()

    if cmd == "PYTH":
        a, b = map(float, parts[1:])
        result = math.sqrt(a*a + b*b)

    elif cmd == "QUAD":
        a, b, c = map(float, parts[1:])
        D = b*b - 4*a*c
        if D < 0:
            result = []
        elif D == 0:
            result = [-b / (2*a)]
        else:
            result = [(-b + D**0.5)/(2*a), (-b - D**0.5)/(2*a)]

    elif cmd == "TRAP":
        a, b, h = map(float, parts[1:])
        result = (a + b) / 2 * h

    elif cmd == "PARA":
        a, h = map(float, parts[1:])
        result = a * h

    else:
        result = "Ошибка команды"

    conn.send(str(result).encode())

conn.close()
server.close()