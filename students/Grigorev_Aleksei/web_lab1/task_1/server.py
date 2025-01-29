import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

def udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        print(f"Сервер запущен на {SERVER_HOST}:{SERVER_PORT}")

        while True:
            message, client_address = server_socket.recvfrom(BUFFER_SIZE)
            print(f"Сообщение от клиента: {message.decode()}")

            response = "Hello, client_bro"
            server_socket.sendto(response.encode(), client_address)
            print(f"Ответ отправлен клиенту {client_address}")

if __name__ == "__main__":
    udp_server()
