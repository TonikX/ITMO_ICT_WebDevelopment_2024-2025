import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            client_message = client_socket.recv(1024)
            if not client_message:
                break
            print(client_message.decode())
        except:
            break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect(('127.0.0.1', 1234))
    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    while True:
        client_message = input()
        if client_message.lower() == 'exit':
            client_socket.close()
            break
        client_socket.send(client_message.encode())
