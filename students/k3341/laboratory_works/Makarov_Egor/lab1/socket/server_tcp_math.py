import socket
import math

HOST = "127.0.0.1"
PORT = 5050

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"TCP math-сервер на {PORT}...")

conn, addr = server_socket.accept()
print("Клиент:", addr)

while True:
    data = conn.recv(1024).decode()
    if not data:
        break

    print("Запрос:", data)
    parts = data.split()
    cmd = parts[0].upper()

    result = None

    # --- Теорема Пифагора ---
    if cmd == "PYTH":
        a, b = map(float, parts[1:])
        result = math.sqrt(a*a + b*b)

    # --- Квадратное уравнение ---
    elif cmd == "QUAD":
        a, b, c = map(float, parts[1:])
        D = b*b - 4*a*c

        if D < 0:
            result = []
        elif D == 0:
            x = -b / (2*a)
            result = [x]
        else:
            x1 = (-b + D**0.5) / (2*a)
            x2 = (-b - D**0.5) / (2*a)
            result = [x1, x2]

    # --- Площадь трапеции ---
    elif cmd == "TRAP":
        a, b, h = map(float, parts[1:])
        result = (a + b) / 2 * h

    # --- Площадь параллелограмма ---
    elif cmd == "PARA":
        a, h = map(float, parts[1:])
        result = a * h

    else:
        result = "Неизвестная команда"

    conn.send(str(result).encode())

conn.close()
server_socket.close()

