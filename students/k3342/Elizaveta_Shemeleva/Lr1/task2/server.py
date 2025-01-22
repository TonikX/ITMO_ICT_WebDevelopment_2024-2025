import socket


def parallelogram_area(base, height):
    return base * height


# Настройка TCP-сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 2020))
server_socket.listen(1)

print("Сервер ожидает подключения...")

while True:
    conn, addr = server_socket.accept()
    print(f"Подключен клиент: {addr}")

    data = conn.recv(1024).decode()
    base, height = map(float, data.split())

    result = parallelogram_area(base, height)
    conn.sendall(f"Площадь параллелограмма: {result}".encode())

    conn.close()
