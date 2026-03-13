import socket

# Настройки сервера
HOST = '127.0.0.1'
PORT = 12346
BUFFER_SIZE = 1024

# Создаём TCP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"TCP-сервер запущен на {HOST}:{PORT}, ожидаем подключения...")

try:
    while True:
        # Принимаем подключение
        conn, addr = server_socket.accept()
        print(f"Подключён клиент {addr}")

        # Получаем данные от клиента
        data = conn.recv(BUFFER_SIZE).decode('utf-8')
        print(f"Получены данные: {data}")

        # Разбираем строку вида "a,b,h"
        try:
            a, b, h = map(float, data.split(','))
            if a <= 0 or b <= 0 or h <= 0:
                raise ValueError("Стороны должны быть положительными")
            area = (a + b) / 2 * h
            result = f"Площадь трапеции: {area:.2f}"
        except Exception as e:
            result = f"Ошибка в данных: {e}. Ожидался формат: a,b,h"

        # Отправляем результат клиенту
        conn.send(result.encode('utf-8'))
        print(f"Отправлено: {result}")

        # Закрываем соединение
        conn.close()
        print("Соединение с клиентом закрыто\n")

except KeyboardInterrupt:
    print("\nСервер остановлен.")
finally:
    server_socket.close()