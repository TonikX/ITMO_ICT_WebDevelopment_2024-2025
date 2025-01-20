import socket


def communicate_with_server():
    serv_address = ('localhost', 8080)
    message = 'Hello, server!'

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message.encode(), serv_address)
        print(f'Message sent to server: {message}')

        data, _ = sock.recvfrom(1024)
        print(f'Received message from server: {data.decode()}')


if __name__ == "__main__":
    communicate_with_server()
