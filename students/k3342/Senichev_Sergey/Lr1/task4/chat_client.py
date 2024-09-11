import socket
import threading

buffer_size = 1024
host = 'localhost'
port = 8000
server_address = (host, port)

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(buffer_size).decode()
            if message:
                print(f"\n{message}")
        except:
            print("Error while connecting to server.")
            client_socket.close()
            break

def server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        client_socket.send(message.encode())

if __name__ == "__main__":
    server()
