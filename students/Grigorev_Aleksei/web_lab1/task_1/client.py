import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

def udp_client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        message = "Hello, server_bro"
        client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))
        print(f"Сообщение отправлено серверу: {message}")

        response, _ = client_socket.recvfrom(BUFFER_SIZE)
        print(f"Ответ от сервера: {response.decode()}")

if __name__ == "__main__":
    udp_client()
