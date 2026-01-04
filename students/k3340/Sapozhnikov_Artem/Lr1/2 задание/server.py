import socket
import math

HOST = "localhost"
PORT = 8080

def solve_quadratic(a, b, c):
    d = b**2 - 4*a*c
    if d < 0:
        return "Нет действительных корней"
    elif d == 0:
        x = -b / (2*a)
        return f"Один корень: x = {x:.2f}"
    else:
        x1 = (-b + math.sqrt(d)) / (2*a)
        x2 = (-b - math.sqrt(d)) / (2*a)
        return f"Два корня: x1 = {x1:.2f}, x2 = {x2:.2f}"

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Подключился клиент {addr}")
        data = conn.recv(1024).decode("utf-8")
        if not data:
            conn.close()
            continue

        try:
            a, b, c = map(float, data.split())
            result = solve_quadratic(a, b, c)
        except Exception as e:
            result = f"Ошибка: {e}"

        conn.sendall(result.encode("utf-8"))
        conn.close()

if __name__ == "__main__":
    start_server()
  
