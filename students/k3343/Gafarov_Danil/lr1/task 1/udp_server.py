import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('Socket created')

# Привязываем сокет к адресу и порту
HOST = 'localhost'
PORT = 8080
s.bind((HOST, PORT))
print('Socket bind complete')

while True:
    message, address = s.recvfrom(1024)
    print(f"New message from client: {message.decode()}")

    response = 'Hello, UDP Client!'
    s.sendto(response.encode(), address)
    print(f"Message sent to client: {response}")
