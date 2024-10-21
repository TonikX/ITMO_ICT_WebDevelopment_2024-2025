import socket
import math


def calculate_pythagorean(a, b):
    return math.sqrt(a ** 2 + b ** 2)


def solve_quadratic(a, b, c):
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return "No real roots"
    elif discriminant == 0:
        x = -b / (2 * a)
        return x
    else:
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return x1, x2


def calculate_trapezoid_area(a, b, h):
    return ((a + b) / 2) * h


def calculate_parallelogram_area(base, height):
    return base * height


def handle_client_request(data):
    operation, *args = data.split()
    args = list(map(float, args))
    if operation == 'pythagorean':
        return calculate_pythagorean(*args)
    elif operation == 'quadratic':
        return solve_quadratic(*args)
    elif operation == 'trapezoid_area':
        return calculate_trapezoid_area(*args)
    elif operation == 'parallelogram_area':
        return calculate_parallelogram_area(*args)
    else:
        return "Invalid operation"


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)
    print("Server listening on port 8080...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break

        result = handle_client_request(data)
        conn.sendall(str(result).encode('utf-8'))
        conn.close()


if __name__ == "__main__":
    start_server()
