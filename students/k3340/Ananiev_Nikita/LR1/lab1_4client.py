import sys
import socket
import threading

getting_msg, host, port = True, 'localhost', 9090
client_locker = threading.Lock()


def show_chat(sock):
    while True:
        with client_locker:
            serv_data = sock.recv(1024)
        if not serv_data:
            with client_locker:
                sock.close()
            print("Connection closed")
            break
        print(serv_data.decode())


def main_client():
    try:
        client_sock = socket.socket()
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    client_sock.connect((host, port))
    chat_thread = threading.Thread(target=show_chat, args=(client_sock,))
    chat_thread.start()

    while getting_msg:
        new_msg = input().encode('utf-8')
        client_sock.send(new_msg)

    chat_thread.join()


if __name__ == "__main__":
    main_client()
