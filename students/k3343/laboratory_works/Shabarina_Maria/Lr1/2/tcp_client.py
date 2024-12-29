import socket

a = input("Enter the first side (a): ")
b = input("Enter the second side (b): ")
h = input("Enter height (h): ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect(("localhost", 1234))
    client_socket.sendall(f"{a}, {b}, {h}".encode())
    server_message = client_socket.recv(1024)

print(f"The area of the trapezoid: {server_message.decode()}")