import socket

SERVER_ADDR = ("localhost", 9090)

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = "Hello, server!"
    client_socket.sendto(message.encode('utf-8'), SERVER_ADDR)

    client_socket.settimeout(5.0)
    try:
        data, server_address = client_socket.recvfrom(1024)
        response = data.decode('utf-8')
        print(f"[Message from {server_address[0]}:{server_address[1]}] {response}")
    except socket.timeout:
        print("[Error] Server timeout")

    client_socket.close()
