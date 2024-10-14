import socket


# HEADERSIZE = 4
# AF_INET - IPv4
# SOCK_STREAM - TCP
# SOCK_DGRAM - UDP
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 2003))

    while True:
        data, client_address = server_socket.recvfrom(1234)
        if data:
            message = data.decode('utf-8')
            print(f"Received message from {client_address}: {message}")
            server_msg = "Hello client!"
            server_socket.sendto(server_msg.encode("utf-8"), client_address)


if __name__ == "__main__":
    main()
