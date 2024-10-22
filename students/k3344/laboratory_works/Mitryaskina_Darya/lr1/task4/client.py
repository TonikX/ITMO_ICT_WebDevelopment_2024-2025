import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(2056).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            break
    client_socket.close()


def send_messages(client_socket):
    while True:
        new_msg = input()
        client_socket.send(new_msg.encode('utf-8'))


def start_client():
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((socket.gethostname(), 1234))

        welcome_msg = conn.recv(1024).decode()
        print(welcome_msg)

        receive = threading.Thread(target=receive_messages, args=(conn,))
        receive.start()
        send = threading.Thread(target=send_messages, args=(conn,))
        send.start()

    except KeyboardInterrupt:
        conn.close()


if __name__ == '__main__':
    start_client()