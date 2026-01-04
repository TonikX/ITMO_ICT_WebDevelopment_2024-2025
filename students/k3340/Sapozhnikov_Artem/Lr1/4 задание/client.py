import socket
import threading

HOST = 'localhost'
PORT = 8080

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode("utf-8")
            if not message:
                break
            print("\n" + message)
        except:
            print("Соединение с сервером потеряно.")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Запрашиваем имя
    name = input("Введите ваше имя: ")
    client_socket.send(name.encode("utf-8"))

    # Поток для приёма сообщений
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    # Отправка сообщений
    print("Введите сообщения (Ctrl+C для выхода):")
    while True:
        try:
            msg = input()
            if msg.strip():
                client_socket.send(msg.encode("utf-8"))
        except KeyboardInterrupt:
            print("\nВыход из чата.")
            client_socket.close()
            break

if __name__ == "__main__":
    main()
