import socket


def calculate_area(base, height):
    return base * height


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12346))
server_socket.listen(1)

print("TCP-сервер ждет подключения клиента...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Подключение от {client_address}")

    data = client_socket.recv(1024).decode('utf-8')
    base, height = map(float, data.split())

    area = calculate_area(base, height)
    client_socket.send(str(area).encode('utf-8'))

    client_socket.close()
