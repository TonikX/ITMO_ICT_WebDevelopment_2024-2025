import socket

if __name__ == '__main__':
    socket_user = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('localhost', 8088)
    message = 'Hello, server'
    socket_user.sendto(message.encode(), server_address)

    data, server = socket_user.recvfrom(1024)
    socket_user.close()

    print(data.decode())

