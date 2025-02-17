import socket
import json


def start_tcp_server(host='127.0.0.1', port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f'Server listening on {host}:{port}')

        while True:
            connection, client_address = server_socket.accept()
            with connection:
                print(f'Connected by {client_address}')
                while True:
                    data = connection.recv(1024)
                    if not data:
                        break
                    received_data = data.decode()
                    print(f'Received: {received_data}')
                    dict_data = json.loads(received_data)
                    parallelogram_square = dict_data['length'] * dict_data['height']
                    connection.sendall(bytes(json.dumps({'square': parallelogram_square}).encode()))


if __name__ == "__main__":
    start_tcp_server()
