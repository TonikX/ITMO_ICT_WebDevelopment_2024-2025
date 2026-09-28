import socket

HOST = "127.0.0.1"
PORT = 50000

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))
server.settimeout(0.5)  # чтобы recvfrom() не блокировал Ctrl+C навсегда
print(f"UDP-сервер запущен на {HOST}:{PORT}")

try:
    while True:
        try:
            data, address = server.recvfrom(1024)
        except socket.timeout:
            continue

        print(f"Сообщение от {address}: {data.decode()}")
        server.sendto("Hello, client".encode(), address)
except KeyboardInterrupt:
    print("\nСервер остановлен")
finally:
    server.close()
