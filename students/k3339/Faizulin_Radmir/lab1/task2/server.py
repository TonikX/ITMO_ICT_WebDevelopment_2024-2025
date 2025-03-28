# TCP сервер для вычисления площади трапеции
import socket

def calculate_trapezoid_area(a, b, h):
    """Вычисляет площадь трапеции."""
    return 0.5 * (a + b) * h

# Создаем TCP-сокет
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к IP-адресу и порту
server_address = ("127.0.0.1", 7777)
serverSock.bind(server_address)
serverSock.listen(1)
print("Сервер запущен и ожидает подключения...")

while True:
    # Принимаем соединение от клиента
    connection, client_address = serverSock.accept()
    try:
        print(f"Подключение от клиента: {client_address}")

        # Получаем данные от клиента
        data = connection.recv(1024).decode()
        print(f"Получено сообщение от клиента: {data}")

        # Разбираем данные и вычисляем площадь
        try:
            a, b, h = map(float, data.split())
            area = calculate_trapezoid_area(a, b, h)
            response = f"Площадь трапеции: {area:.2f}"
        except ValueError:
            response = "Ошибка: Проверьте введенные данные. Ожидаются три числа: a, b, h."

        # Отправляем ответ клиенту
        connection.sendall(response.encode())
    finally:
        connection.close()
        print(f"Соединение с {client_address} закрыто.")
