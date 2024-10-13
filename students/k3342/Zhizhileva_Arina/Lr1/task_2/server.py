from socket import *
import time

def parallelogram_area(a, h):
    return a * h


server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

print("Waiting for client...")

while True:
    connection, addr = server_socket.accept()
    try:
        time.sleep(3)
        print(f"client {addr} is now in session")
        data = connection.recv(1024).decode()
        if data:
            base, height = map(float, data.split())
            print(f"Parameters {base}, {height} are received")
            area = parallelogram_area(base, height)

            connection.sendall(str(area).encode())
            print(f"result {area} sent to client")
    finally:
        connection.close()
