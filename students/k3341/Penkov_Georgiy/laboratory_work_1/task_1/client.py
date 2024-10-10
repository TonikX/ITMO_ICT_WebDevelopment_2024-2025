import socket

SERVER_ADDRESS = ("127.0.0.1", 1024)
MESSAGE = b"Hello, server!"
BUFFER_SIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    print(f"Sending {MESSAGE}")
    client_socket.sendto(MESSAGE, SERVER_ADDRESS)
    print("Waiting to receive..")
    response, server = client_socket.recvfrom(BUFFER_SIZE)
    print(f"Received {response} from {server}")
finally:
    client_socket.close()
    print("Socket closed")
