import logging
import socket
import json


def start_tcp_client(host='127.0.0.1', port=8000):
    print("Please enter length and height of parallelogram")
    length = int(input())
    height = int(input())
    data = json.dumps({'length': length, 'height': height})
    encoded_data = bytes(data, encoding="utf-8")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f'Sending: {encoded_data}')
        client_socket.sendall(encoded_data)

        data = client_socket.recv(1024)
        print(f'Received from server: {json.loads(data.decode())["square"]}')


if __name__ == "__main__":
    start_tcp_client()
