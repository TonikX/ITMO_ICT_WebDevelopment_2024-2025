import socket 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 12346))
server.listen(1)

print("TCP-сервер запущен. Ожидание клиента...")

conn, address = server.accept()

with conn:
    print("Клиент подключился:", address)
    data = conn.recv(1024).decode()
    
    a, h = map(float, data.split())
    s = a * h

    print("Площадь параллелограмма:", s)
    conn.sendall(str(s).encode())

server.close()