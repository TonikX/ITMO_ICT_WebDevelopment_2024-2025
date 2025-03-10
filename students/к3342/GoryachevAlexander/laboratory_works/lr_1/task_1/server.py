import socket

SERVER_IP = '127.0.0.1'  # Локальный IP-адрес
SERVER_PORT = 12345       # Порт для прослушивания

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

print(f"UDP сервер запущен на {SERVER_IP}:{SERVER_PORT}")

while True:
    data, client_address = server_socket.recvfrom(1024)
    print(f"Сообщение от клиента {client_address}: {data.decode()}")

    response = "Hello, client"
    server_socket.sendto(response.encode(), client_address)