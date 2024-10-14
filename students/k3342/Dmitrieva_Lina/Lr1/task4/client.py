import socket
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
            print("Ошибка при получении сообщения.")
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        message = input('')
        if message:
            try:
                client_socket.send(message.encode())
            except:
                print("Ошибка при отправке сообщения.")
                client_socket.close()
                break

def start_client():
    server_address = ('localhost', 8080)
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    name = input("Введите ваше имя: ")
    client_socket.send(name.encode())

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

if __name__ == "__main__":
    start_client()
