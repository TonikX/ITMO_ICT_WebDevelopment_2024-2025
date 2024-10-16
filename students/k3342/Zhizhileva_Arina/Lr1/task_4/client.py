from socket import *
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except:
            print("unable to send message")
            client_socket.close()
            break

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('localhost', 8080))

threading.Thread(target=receive_messages, args=(client_socket,)).start()

username = input("Enter your name: ")
client_socket.send(username.encode())

while True:
    message = input()
    if message.lower() == 'exit':
        break
    client_socket.send(message.encode())

client_socket.close()