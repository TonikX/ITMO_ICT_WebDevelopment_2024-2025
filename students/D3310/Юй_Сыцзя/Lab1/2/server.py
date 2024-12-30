import math
import socket


def calc(a, b, c):
    try:
        if c != 0:
            return str(a * c)
        else:
            return str(a * b * math.sin(math.radians(c)))
    except:
        return 'Wrong format'


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("localhost", 7070))
serverSocket.listen(1)

print("Server is listening on port 7070...")

while True:
    client_socket, client_address = serverSocket.accept()

    data = client_socket.recv(1024).decode()
    a, b, c = map(float, data.split())

    ans = calc(a, b, c)

    client_socket.send(ans.encode())

    client_socket.close()
