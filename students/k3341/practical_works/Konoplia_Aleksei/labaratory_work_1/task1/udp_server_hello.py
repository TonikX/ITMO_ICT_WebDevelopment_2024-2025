import socket

def udp_server_hello():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("localhost", 12345))
    print("UDP сервер запущен на порту 12345")

    while True:
        message, client_address = server_socket.recvfrom(1024)
        print(f"Получено сообщение: {message.decode()} от {client_address}")
        server_socket.sendto(b"Hello, client", client_address)

if __name__ == '__main__':
    udp_server_hello()