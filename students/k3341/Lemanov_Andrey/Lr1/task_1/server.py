import socket


def start_udp_server(host='', port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        print(f'Server listening on {host}:{port}')

        while True:
            received_data = server_socket.recvfrom(1024)
            data = received_data[0]
            addr = received_data[1]
            if not data:
                break
            print(f'Received: {data.decode()}')
            server_socket.sendto("Hello, client".encode(), addr)


if __name__ == "__main__":
    start_udp_server()
