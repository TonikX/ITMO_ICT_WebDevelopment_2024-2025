import socket


def calculate_trapezoid_area(a, b, h):
    return ((a + b) / 2) * h


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 65432)
server_socket.bind(server_address)
server_socket.listen(1)

print("Server is running and waiting for connection...")

while True:
    connection, client_address = server_socket.accept()
    try:
        print(f"Connected client: {client_address}")

        data = connection.recv(1024).decode()
        print(f"Received data: {data}")

        a, b, h = map(float, data.split(', '))

        area = calculate_trapezoid_area(a, b, h)

        connection.sendall(str(area).encode())
    finally:
        connection.close()
