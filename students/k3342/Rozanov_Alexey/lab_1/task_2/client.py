import socket


if __name__ == "__main__":
    socket_user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 8088)
    message = '2 4 30'

    socket_user.connect(server_address)
    socket_user.send(message.encode('utf-8'))

    resp = socket_user.recv(1024)

    print(resp.decode())

    socket_user.close()

