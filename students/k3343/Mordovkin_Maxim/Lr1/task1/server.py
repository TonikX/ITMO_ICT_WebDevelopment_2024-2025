import socket

def start_server(host='127.0.0.1', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_socket.bind((host, port))
    print(f"Сервер запущен на {host}:{port}...")

    while True:
        try:
            message, client_address = server_socket.recvfrom(1024)
            print(f"Получено от {client_address}: {message.decode()}")

            response = "Привет, клиент"
            server_socket.sendto(response.encode(), client_address)
            print(f"Отправлено {client_address}: {response}")
        except Exception as e:
            print(f"Ошибка: {e}")
            break

if __name__ == "__main__":
    start_server()
