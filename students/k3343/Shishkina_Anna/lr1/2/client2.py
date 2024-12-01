import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 12345))

a = input("Длина катета a: ")
b = input("Длина катета b: ")

client_socket.send(f"{a} {b}".encode('utf-8'))

response = client_socket.recv(1024).decode('utf-8')
print(f"Ответ от сервера: {response}")

client_socket.close()
