import socket
import threading

def receive_messages(client_socket):
    #  Обработка сообщений от сервера
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(message.decode('utf-8'))
            else:
                break
        except:
            print("Потеря соединения.")
            break

def start_client():
    #  Запуск клиента
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 8080))

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    while True:
        message = input()
        client.send(message.encode('utf-8'))

if __name__ == "__main__":
    start_client()
