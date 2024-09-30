import socket
#
# con_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# con_client.connect(('localhost', 7090))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect(('localhost', 7090))
    s.sendall(b"GET / HTTP/1.1\r\nHost: localhost\r\nAccept: text/html\r\nConnection: close\r\n\r\n")

    while True:

        data = s.recv(1024)

        if not data:
            break

        print(data.decode())