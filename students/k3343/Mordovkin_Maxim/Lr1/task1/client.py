import socket

def start_client(server_host='127.0.0.1', server_port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        message = "Привет, сервер"
        client_socket.sendto(message.encode(), (server_host, server_port))
        print(f"Отправлено серверу: {message}")

        response, server_address = client_socket.recvfrom(1024)
        print(f"Получено от сервера: {response.decode()}")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
