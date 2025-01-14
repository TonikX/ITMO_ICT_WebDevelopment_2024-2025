import socket
import threading
#Обработчик получения сообщений
def receive_messages(user_socket):
    while True:
        try:
            message = user_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except:
            print("Message receive error")
            break
#Обработчик отправки сообщений
def send_messages(user_socket):
    while True:
        message = input("")
        user_socket.send(message.encode())
#Запуск клиента
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    client_socket.connect(server_address)
    #Поток получения сообщений
    thread_receive = threading.Thread(target=receive_messages, args=(client_socket,))
    thread_receive.start()
    #Поток отправки сообщений
    thread_send = threading.Thread(target=send_messages, args=(client_socket,))
    thread_send.start()

if __name__ == "__main__":
    start_client()