import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

a = input("Enter the base of the parallelogram: ")
h = input("Enter the height of the parallelogram: ")
message = a + ' ' + h
client_socket.sendall(message.encode())

response = client_socket.recv(1024)
print(f'Area of the parallelogram: {response.decode()}')

client_socket.close()