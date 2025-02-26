import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 1234))

data = client.recv(1024)
print(data.decode())

user = input("Введите стороны a и b через пробел: ")
client.send(user.encode())

response = client.recv(1024)
print(response.decode())

client.close()

