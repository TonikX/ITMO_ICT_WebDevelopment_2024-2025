import socket

def solve_quadratic_equation(a, b, c):
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return None
    elif discriminant == 0:
        x = -b / (2*a)
        return (x, x)
    else:
        x1 = (-b + (discriminant)**0.5) / (2*a)
        x2 = (-b - (discriminant)**0.5) / (2*a)
        return (x1, x2)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8080))

server_socket.listen(1)
print("Сервер запущен на порту 8080...")

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    request = client_connection.recv(1024).decode()
    a, b, c = request.split()
    solution = solve_quadratic_equation(float(a),  float(b), float(c))
    if solution is None:
        response = 'Корней нет'
    elif solution[0] == solution[1]:
        response = f'Корень уравнения: {solution[0]}'
    else:
        response = f'Корни уравнения: {solution[0]} и {solution[1]}'
    client_connection.sendall(response.encode())

    client_connection.close()