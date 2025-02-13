import socket
import math

def handle_client(client_socket):
    try:
        print("Обработка нового клиента...")
        while True:
            request = client_socket.recv(1024).decode()
            if not request:
                print("Данные не получены. Закрытие соединения.")
                break
            print(f"Получен запрос: {request}")

            data = request.split(";")
            operation = data[0]
            parameters = list(map(float, data[1:])) if len(data) > 1 else []

            if operation == "1":
                if len(parameters) != 3:
                    result = "Ошибка: Квадратное уравнение требует 3 параметра (a, b, c)."
                else:
                    a, b, c = parameters
                    discriminant = b**2 - 4*a*c
                    if discriminant < 0:
                        result = "Нет действительных корней."
                    elif discriminant == 0:
                        root = -b / (2 * a)
                        result = f"Один корень: {root}"
                    else:
                        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
                        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
                        result = f"Два корня: {root1}, {root2}"
            else:
                result = "Ошибка: Неизвестная операция."

            print(f"Отправка результата клиенту: {result}")
            client_socket.send(str(result).encode())
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        print("Клиент отключился.")
        client_socket.close()

def start_server(host='127.0.0.1', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Сервер запущен на {host}:{port}...")

    while True:
        print("Ожидание нового подключения...")
        client_socket, client_address = server_socket.accept()
        print(f"Новое подключение от {client_address}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()
