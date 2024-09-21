## Задание 4: Многопользовательский чат с помощью сокетов и протокола TCP (+ многопоточность)

Описание: <br> Реализовать двухпользовательский или многопользовательский чат. Реализация
многопользовательского часа позволяет получить максимальное количество
баллов.

Код сервера:
```python
import sys
import socket
import threading
from copy import copy


max_conn_count = 10
locker = threading.Lock()
listening = True
threads = []
connections = []


def threaded_handle(conn, address):
    while True:
        data = conn.recv(1024)
        if not data:
            conn.close()
            print(f"{address} connection interrupted")
            break
        msg = address[0] + ":" + str(address[1]) + " said " + data.decode()
        print(msg)
        with locker:
            conn_copy = copy(connections)
        for c in conn_copy:
            c.sendall(msg.encode('utf-8'))


def main():
    try:
        serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_socket.bind(('', 9090))
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    serv_socket.listen(max_conn_count)

    while listening:
        conn_socket, addr = serv_socket.accept()
        conn_thread = threading.Thread(target=threaded_handle, args=(conn_socket, addr,))
        threads.append(conn_thread)
        connections.append(conn_socket)
        conn_thread.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()

```
Код клиента:
```python
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

```