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
            break

def send_messages(client_socket):
    while True:
        message = input()
        if message.lower() == 'выход':
            client_socket.send('Покинул чат.'.encode())
            break
        client_socket.send(message.encode())
        print(f"Я: {message}")

def start_client(server_host='127.0.0.1', server_port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    name = input("Введите ваше имя: ")
    client_socket.send(name.encode())

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

if __name__ == "__main__":
    start_client()