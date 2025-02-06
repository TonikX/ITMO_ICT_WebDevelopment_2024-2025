import socket
import math


def calc_hypotenuse(a: float, b: float) -> float:
    if a <= 0 or b <= 0:
        raise ValueError("The lengths of the sides must be positive numbers.")
    return math.sqrt(a**2 + b**2)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SERVER_ADDRESS = ("localhost", 1234)
BUFFER_SIZE = 1024

server_socket.bind(SERVER_ADDRESS)
server_socket.listen(0)
print(f"Listening on {SERVER_ADDRESS}")

client_socket, client_address = server_socket.accept()
print(f"Accepted connection from {client_address}")

while True:
    try:
        request = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Received: {request}")
        try:
            a, b = map(float, request.split(" "))
            response = calc_hypotenuse(a, b)
        except Exception as err:
            response = f"Something went wrong: {err}"
        client_socket.send(str(response).encode())
    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()
        print("Connection to client closed")
        server_socket.close()
        break
