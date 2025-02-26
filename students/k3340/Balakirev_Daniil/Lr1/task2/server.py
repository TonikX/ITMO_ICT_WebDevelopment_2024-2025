import socket

def pifagor(a: int, b: int) -> float:
    return round((a**2 + b**2) ** (1/2))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 1234))
server.listen(1)
print("Сервер запущен, ожидает подключения...")

conn, addr = server.accept()
print(f"Подключение от {addr}")
conn.send("Теорема Пифагора".encode())

data = conn.recv(1024)
if data:
    a, b = map(int, data.decode().split())
    result = pifagor(a, b)
    conn.send(f'Гипотенуза: {result}'.encode())

conn.close()