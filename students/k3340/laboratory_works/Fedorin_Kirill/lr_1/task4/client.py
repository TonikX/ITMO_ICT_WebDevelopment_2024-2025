import socket
import threading


def receive_messages(client_socket):
    """
    Получает сообщения от сервера и выводит их в консоль.
    """
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except:
            print("Соединение с сервером потеряно.")
            break


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 12345))

    # Поток для получения сообщений
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Ввод никнейма
    nickname = input("Введите ваш никнейм: ")
    client_socket.send(nickname.encode())

    # Отправка сообщений
    while True:
        try:
            message = input()
            if message.lower() == "/exit":
                print("Отключение от чата.")
                client_socket.close()
                break
            client_socket.send(message.encode())
        except:
            print("Ошибка при отправке сообщения. Отключение.")
            client_socket.close()
            break


if __name__ == "__main__":
    start_client()
