import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Создаем сокет (AF_INET - IPv4, SOCK_DGRAM - UDP)
sock.bind(('localhost', 2024))  # Определяем ip хоста и номер порта
print("Server listening on port 2024")
message = "Hello, client"

while True:
    data, client_addr = sock.recvfrom(1024)
    print(data.decode())
    sock.sendto(message.encode(), client_addr)
