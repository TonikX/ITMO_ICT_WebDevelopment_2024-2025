import socket
import threading


HOST = 'localhost'
PORT = 9091

# Функция для приема сообщений от сервера
def receive_messages(client_socket):
    while True:
        try:
            # Получаем сообщение от сервера
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                print("Отключено от сервера.")
                break
        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
            break

def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    while True:
        user_input = input()

        if user_input.lower() == "выйти":
            break

        try:
            # Отправляем введенное сообщение на сервер
            client_socket.send(user_input.encode('utf-8'))
        except Exception as e:
            print(f"Ошибка при отправке: {e}")

    client_socket.close()

if __name__ == "__main__":
    run_client()