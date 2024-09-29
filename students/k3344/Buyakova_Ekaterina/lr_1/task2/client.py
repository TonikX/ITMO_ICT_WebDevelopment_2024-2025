import socket

# Функция для запроса данных у пользователя
def cat_info():
    cat1 = input("Determine the length of the first leg: ")
    cat2 = input("Determine the length of the second leg: ")
    return f'{cat1},{cat2}'

# Создаем TCP сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect(('localhost', 8080))

# Получаем параметры от пользователя
data = cat_info()

# Отправляем данные на сервер
client_socket.sendall(data.encode())

# Получаем результат от сервера
response = client_socket.recv(1024).decode()
print(f'Server response: {response}')

# Закрываем соединение
client_socket.close()
