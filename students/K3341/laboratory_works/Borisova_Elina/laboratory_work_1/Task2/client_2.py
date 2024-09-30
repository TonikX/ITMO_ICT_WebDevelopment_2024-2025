import socket

a = input("a:")
b = input("b:")
c = input("c:")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8080))

client.send(f"{a},{b},{c}".encode('utf-8'))
result = client.recv(1024).decode('utf-8')
print(f"Solution: {result}")

client.close()