import socket
import threading

HOST = 'localhost'
PORT = 8080

def receive_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
    except OSError:
        pass
    finally:
        client_socket.close()

def send_messages(client_socket):
    try:
        while True:
            message = input('')
            if message.lower() == 'exit':
                client_socket.shutdown(socket.SHUT_RDWR)
                client_socket.close()
                break
            client_socket.send(message.encode('utf-8'))
    except OSError:
        pass

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    receive_thread.start()
    send_thread.start()
    receive_thread.join()
    send_thread.join()

if __name__ == "__main__":
    start_client()
