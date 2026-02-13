import socket
import math

HOST = "127.0.0.1"
PORT = 5001

def solve_quadratic(a, b, c):
    D = b * b - 4 * a * c
    if D > 0:
        x1 = (-b + math.sqrt(D)) / (2 * a)
        x2 = (-b - math.sqrt(D)) / (2 * a)
        return f"Два корня: x1 = {x1}, x2 = {x2}"
    elif D == 0:
        x = -b / (2 * a)
        return f"Один корень: x = {x}"
    else:
        return "Действительных корней нет (D < 0)"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Quadratic TCP server on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            data = conn.recv(1024).decode("utf-8")
            if not data:
                continue
            try:
                a_str, b_str, c_str = data.split()
                a = float(a_str)
                b = float(b_str)
                c = float(c_str)
                if a == 0:
                    result = "Ошибка: a не должно быть 0"
                else:
                    result = solve_quadratic(a, b, c)
            except Exception as e:
                result = f"Ошибка разбора данных: {e}"
            conn.sendall(result.encode("utf-8"))
