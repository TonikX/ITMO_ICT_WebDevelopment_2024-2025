import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind(('localhost', 8080))

    print("Сервер запущен на порту 8080...")

    while True:
        client_message, client_address = server_socket.recvfrom(1024)
        print("Recieved message:", client_message.decode())
        server_socket.sendto("Hello, client".encode(), client_address)
        socket.socket.close()
