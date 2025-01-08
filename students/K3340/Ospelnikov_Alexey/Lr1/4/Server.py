import socket
import threading
from copy import copy


max_conn_count = 10
locker = threading.Lock()
threads = []
connections = []

def threaded_handle(conn, address):
    while True:
        data = conn.recv(1024)
        if not data:
            conn.close()
            print(f"{address} connection interrupted")
            break
        msg = address[0] + ":" + str(address[1]) + " send a message: " + data.decode()
        print(msg)
        with locker:
            conn_copy = copy(connections)
        for c in conn_copy:
            c.sendall(msg.encode('utf-8'))


def main():
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a_socket.bind(('', 8080))
    a_socket.listen(max_conn_count)

    while True:
        conn_socket, addr = a_socket.accept()
        conn_thread = threading.Thread(target=threaded_handle, args=(conn_socket, addr,))
        threads.append(conn_thread)
        connections.append(conn_socket)
        conn_thread.start()

if __name__ == "__main__":
    main()