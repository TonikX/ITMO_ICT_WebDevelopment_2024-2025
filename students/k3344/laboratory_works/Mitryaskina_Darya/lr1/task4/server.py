import socket
import threading

CLIENTS = []


def remove_client(client_socket):
    if client_socket in CLIENTS:
        CLIENTS.remove(client_socket)


def broadcast_message(message, sender_socket, sender_address):
    for client_socket in CLIENTS:
        if client_socket != sender_socket:
            try:
                msg = str(sender_address[1]) + ': ' +  message
                client_socket.send(msg.encode('utf-8'))
            except:
                client_socket.close()
                remove_client(client_socket)


def handle_client(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(2056).decode('utf-8')
            if message:
                broadcast_message(message, client_socket, client_address)
            else:
                break
        except:
            break
    client_socket.close()
    remove_client(client_socket)


def start_server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), 1234))
        s.listen(10)
        print("Сервер запущен и слушает порт 1234...")
        while True:
            client_socket, client_address = s.accept()
            client_socket.send(b'You connected successfully.')
            print(f"Подключен клиент: {client_address}")
            CLIENTS.append(client_socket)
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        s.close()

if __name__ == '__main__':
    start_server()

