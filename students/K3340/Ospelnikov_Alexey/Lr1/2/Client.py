import socket


client_socket = socket.socket()

client_socket.connect(('localhost', 8080))
print("Please write the lengths of 2 sides and an angle of the parallelogramm:")
client_socket.send(bytes(input(), 'utf-8'))
res = client_socket.recv(1024)
print(f"Area = {res.decode()}")

client_socket.close()