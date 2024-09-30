import socket
def calc(a, b, h):
    return ((a + b) / 2) * h
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("localhost", 14901)
server_sock.bind(server_address)
server_sock.listen(1)
print("Сервер запущен и ожидает сообщения...")
while True:
    conn, addr = server_sock.accept()
    print(f"Подключение от {addr}")
    data = conn.recv(1024).decode()
    if not data:
        break
    a, b, h = map(float, data.split())
    s = calc(a, b, h)
    conn.send(f"Площадь трапеции: {s}".encode())
    conn.close()
