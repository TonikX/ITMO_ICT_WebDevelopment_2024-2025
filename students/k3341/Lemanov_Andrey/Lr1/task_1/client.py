import socket


def start_udp_client(host='127.0.0.1', port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.connect((host, port))
        message = 'Hello, server'
        print(f'Sending: {message}')
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        print(f'Received from server: {data.decode()}')


if __name__ == "__main__":
    start_udp_client()
