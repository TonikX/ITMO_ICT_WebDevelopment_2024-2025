import socket
import pickle
import math

def solve_quadratic(a, b, c):
    discriminant = b ** 2 - 4 * a * c
    if discriminant >= 0:
        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return root1, root2
    else:
        return "Корней нет"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(10)

while True:
    try:
        conn, addr = s.accept()
        data = conn.recv(1024)
        coefs = pickle.loads(data)

        a, b, c = coefs
        result = solve_quadratic(a, b, c)

        result_data = pickle.dumps(result)
        conn.send(result_data)

        conn.close()

    except KeyboardInterrupt:
        s.close()
        break