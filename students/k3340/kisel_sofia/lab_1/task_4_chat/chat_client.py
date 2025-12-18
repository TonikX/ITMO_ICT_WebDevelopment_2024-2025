import socket
import threading


def receive_messages(client: socket.socket):
    while True:
        try:
            data = client.recv(1024)
            if data:
                print(data.decode())
        except Exception:
            break


def run_client(server_host: str = '127.0.0.1', server_port: int = 8082):
    nickname = input()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((server_host, server_port))
        client.sendall(nickname.encode())

        thread = threading.Thread(
            target=receive_messages,
            args=(client,),
            daemon=True
        )
        thread.start()

        while True:
            message = input()
            client.sendall(message.encode())


if __name__ == '__main__':
    run_client()
