import socket
from math import sqrt


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = 'localhost'
PORT = 8080
address = HOST, PORT
s.bind(address)
s.listen(1)
print("Server is running!")
while True:
    client_connection, client_address = s.accept()
    print("We got connection now")
    request = client_connection.recv(1024).decode()
    try:
        a, b = map(float, request.split(','))
        if a > 0 and b > 0:
            result = str(sqrt(a**2 + b**2))
        else:
            result = "Invalid data"
    except:
        result = "Invalid data"

# Отправили ответ
    client_connection.sendall(result.encode())
    client_connection.close()