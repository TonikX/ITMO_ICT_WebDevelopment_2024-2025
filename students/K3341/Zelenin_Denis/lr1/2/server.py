import socket


def s_trapezoid(param):
    return str(0.5 * (param[0] + param[1]) * param[2]) if len(param) == 3 else 'Некорректные данные'


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = (socket.gethostname(), 8000)
server_socket.bind(HOST)


server_socket.listen(1)
print("Сервер ожидает подключения...")

while True:
    conn, addr = server_socket.accept()
    print(f"Подключение установлено с {addr}")
    data = list(map(int, conn.recv(1024).decode().split()))
    square = s_trapezoid(data)
    print(f"Рассчитанная площадь: {square}")
    conn.send(square.encode())

