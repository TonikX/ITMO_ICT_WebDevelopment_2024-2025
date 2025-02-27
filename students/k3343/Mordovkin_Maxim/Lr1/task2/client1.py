import socket

def start_client(server_host='127.0.0.1', server_port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("Подключение к серверу...")
        client_socket.connect((server_host, server_port))
        print("Соединение с сервером установлено.")

        print("Доступные операции:")
        print("1: Решение квадратного уравнения (параметры: a, b, c)")

        while True:
            operation = input("Введите номер операции (или 'выход' для завершения): ")
            if operation.lower() == "выход":
                print("Завершение работы...")
                break

            parameters = input("Введите параметры через пробел: ")
            message = f"{operation};{parameters.replace(' ', ';')}"
            print(f"Отправка сообщения серверу: {message}")

            client_socket.send(message.encode())

            result = client_socket.recv(1024).decode()
            print(f"Результат: {result}")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
