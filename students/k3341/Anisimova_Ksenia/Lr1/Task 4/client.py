import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except Exception as e:
            print(f"Error while receiving a message from the server: {e}")
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8081)
client_socket.connect(server_address)

username = input("Input your name: ")
client_socket.send(username.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

while True:
    message = input()
    if message.lower() == 'exit':
        break
    client_socket.send(message.encode('utf-8'))

client_socket.close()