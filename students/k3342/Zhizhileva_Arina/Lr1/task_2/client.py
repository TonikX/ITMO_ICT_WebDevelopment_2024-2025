from socket import *

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('localhost', 12345))

try:
    base = float(input("Enter the length of the base of the parallelogram: "))
    height = float(input("Enter the height of the parallelogram: "))
    print(f"Parameters for the parallelogram are base={base}, height={height}.")
    message = f"{base} {height}"
    client_socket.sendall(message.encode())

    data = client_socket.recv(1024).decode()
    print(f"Area of the parallelogram is {data}")

finally:
    client_socket.close()

