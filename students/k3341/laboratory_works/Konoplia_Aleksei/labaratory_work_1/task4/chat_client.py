import socket
import threading

def chat_client():
    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode()
                print(message)
            except:
                print("Отключено от сервера")
                client_socket.close()
                break

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 34567))

    threading.Thread(target=receive_messages).start()

    while True:
        message = input()
        client_socket.sendall(message.encode())

if __name__ == '__main__':
    chat_client()