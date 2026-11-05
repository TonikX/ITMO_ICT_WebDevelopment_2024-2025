import socket

SERVER_ADDR = ("localhost", 9090)

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(SERVER_ADDR)

    print(f"[*] UDP-server started on {SERVER_ADDR[0]}:{SERVER_ADDR[1]}")

    try:
        while True:
            data, client_address = server_socket.recvfrom(1024)
            message = data.decode('utf-8')
            print(f"[Message from {client_address[0]}:{client_address[1]}] {message}")

            response = "Hello, client!"
            server_socket.sendto(response.encode('utf-8'), client_address)
    except KeyboardInterrupt:
        print("[*] UDP-server stopped")
    finally:
        server_socket.close()

