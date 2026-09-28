import socket

HOST = "127.0.0.1"
PORT = 50000

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto("Hello, server".encode(), (HOST, PORT))

data, address = client.recvfrom(1024)
print(f"Ответ от сервера: {data.decode()}")

client.close()
