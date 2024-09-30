import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"\n{message}")
            else:
                break
        except:
            print("Connection closed by server")
            client_socket.close()
            break


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5555)
client_socket.connect(server_address)

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

try:
    while True:
        message = input("You: ")
        client_socket.send(message.encode())
except KeyboardInterrupt:
    print("Exiting chat...")
    client_socket.close()
