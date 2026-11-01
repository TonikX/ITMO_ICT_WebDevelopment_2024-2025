import socket

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.connect(('localhost', 8080))

data = socket_server.recv(1024)
print(data.decode("utf-8"))

message = input()

socket_server.send(message.encode("utf-8"))
data = socket_server.recv(1024)
print(data.decode("utf-8"))
message = input()
socket_server.send(message.encode("utf-8"))
data = socket_server.recv(1024)
print(data.decode("utf-8"))

socket_server.close()


