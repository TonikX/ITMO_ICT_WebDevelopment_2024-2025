import socket
import threading


getting_msg, host, port = True, 'localhost', 8080
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
    client_socket = socket.socket()
    client_socket.connect((host, port))
    chat_thread = threading.Thread(target=show_chat, args=(client_socket,))
    chat_thread.start()

    while getting_msg:
        new_msg = input().encode('utf-8')
        client_socket.send(new_msg)

    chat_thread.join()


if __name__ == "__main__":
    main_client()