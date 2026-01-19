from socket import socket, AF_INET, SOCK_STREAM
from math import sin, radians

# Создаем TCP-сокет
# используем AF_INET, чтобы работать с IP-адресами (IPv4), и SOCK_DGRAM для использования протокола TCP
server_socket = socket(AF_INET, SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind(('localhost', 8080))

# Начинаем слушать входящие подключения
server_socket.listen(1)
print("Сервер запущен на порту 8080...")
print("Ожидаем запрос на вычисление площади параллелограмма")

while True:
    # Принимаем соединение от клиента
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    # Получаем данные от клиента
    data = client_connection.recv(1024).decode()
    print(f'Получены данные: {data}')

    # Вычисляем площадь
    try:
        # Разделяем данные на основание и высоту
        base1, base2, alpha = map(float, data.split())

        # Формируем ответ
        response = f"Площадь параллелограмма: {round(base1 * base2 * sin(radians(alpha)), 2)}"
    except Exception:
        response = "Ошибка: неверный формат данных. Отправьте в формате: сторона1 сторона2 угол_между_ними_в_градусах"

    # Отправляем ответ клиенту
    client_connection.sendall(response.encode())
    print(f'Отправлен ответ: {response}')

    # Закрываем соединение
    client_connection.close()
