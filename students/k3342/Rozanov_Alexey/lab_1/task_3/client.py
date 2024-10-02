import socket


if __name__ == "__main__":
    socket_user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 8088)
    message = b"GET / HTTP/1.1\r\nHost: webcode.me\r\nAccept: text/html\r\nConnection: close\r\n\r\n"

    socket_user.connect(server_address)
    socket_user.send(message)

    resp = socket_user.recv(1024)

    print(resp.decode())

    socket_user.close()