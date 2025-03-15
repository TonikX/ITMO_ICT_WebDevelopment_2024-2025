import socket
import threading

def receive_server_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Получено сообщение: {message}")
            else:
                break
        except Exception as error:
            print(f"Ошибка при получении сообщения: {error}")
            client_socket.close()
            break

def send_client_messages(client_socket):
    while True:
        try:
            message = input("Введите сообщение: ")
            client_socket.send(message.encode('utf-8'))
        except Exception as error:
            print(f"Ошибка при отправке сообщения: {error}")
            client_socket.close()
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('127.0.0.1', 8075))
        print("Соединение с сервером установлено.")
    except Exception as error:
        print(f"Не удалось подключиться к серверу: {error}")
        return

    threading.Thread(target=receive_server_messages, args=(client_socket,)).start()
    threading.Thread(target=send_client_messages, args=(client_socket,)).start()

if __name__ == "__main__":
    start_client()
