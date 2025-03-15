import socket

SERVER_ADDRESS = ("localhost", 1234)
BUFFER_SIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(SERVER_ADDRESS)

while True:
    data = input("Enter space-separated two numbers: ")
    if not data:
        break
    client_socket.send(data.encode())

    response = client_socket.recv(BUFFER_SIZE).decode()
    print(f"Received: {response}")

client_socket.close()
print("Connection to server closed")
