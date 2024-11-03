import socket


def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('localhost', 12123)
    print("Press Enter to start!")

    try:
        while True:
            s = input()
            if s == "exit":
                break

            message = b"Hello, server"

            print(f"Sending message: {message.decode('utf-8')}")

            client_socket.sendto(message, server_address)

            response, _ = client_socket.recvfrom(1024)
            print(f"Server's response: {response.decode('utf-8')}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    udp_client()
