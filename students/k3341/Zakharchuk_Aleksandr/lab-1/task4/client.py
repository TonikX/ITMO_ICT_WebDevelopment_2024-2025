import socket
import threading


def receive_messages(client_socket: socket.socket) -> None:
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except (Exception, KeyboardInterrupt):
            client_socket.close()
            break


def send_messages(client_socket: socket.socket) -> None:
    while True:
        try:
            message = input().strip()
            client_socket.send(message.encode())
        except (Exception, KeyboardInterrupt):
            client_socket.close()
            break

def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("localhost", 12345))

    send_thread = threading.Thread(target=send_messages, args=(conn,))
    receive_thread = threading.Thread(target=receive_messages, args=(conn,))

    send_thread.start()
    receive_thread.start()

    try:
        receive_thread.join()
        send_thread.join()
    except KeyboardInterrupt:
        print("Соединение разорвано")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
