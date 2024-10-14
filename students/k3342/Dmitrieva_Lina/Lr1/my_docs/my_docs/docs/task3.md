# Задание 3: 

## Описание задачи

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

## Код сервера
```python
import socket

HOST = 'localhost'
PORT = 8081  

#Имя HTML файла, который будет обслуживать сервер
html_file = 'index.html'

def create_http_response(html_content):
    """
    Функция для создания HTTP-ответа с указанным HTML-контентом.
    """
    # Начинаем формирование ответа
    response = 'HTTP/1.1 200 OK\r\n'  # Устанавливаем статус ответа (200 OK)
    response += 'Content-Type: text/html\r\n'  # Указываем тип содержимого (HTML)
    response += 'Content-Length: {}\r\n'.format(len(html_content))  # Указываем длину содержимого
    response += 'Connection: close\r\n'  # Указываем, что соединение будет закрыто после передачи
    response += '\r\n'  # Пустая строка для разделения заголовков и тела ответа
    response += html_content  # Добавляем HTML-контент к ответу
    return response  # Возвращаем сформированный HTTP-ответ

#Создаем TCP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
#Привязываем сокет к указанному хосту и порту
server_socket.bind((HOST, PORT))
#Начинаем слушать входящие соединения (5 - максимальное количество очередей)
server_socket.listen(5) 
print(f"Сервер запущен на {HOST}:{PORT}...")

#Запускаем бесконечный цикл для обработки входящих соединений
while True: 
    # Ожидаем подключения клиента и принимаем его
    client_connection, client_address = server_socket.accept()  
    #Выводим адрес подключившегося клиента
    print(f'Подключение от {client_address}')

    # Получаем запрос от клиента
    request = client_connection.recv(1024).decode()  
    print(f'Запрос от клиента: {request}')

    try:
        # Пытаемся открыть HTML-файл и прочитать его содержимое
        with open(html_file, 'r') as file:  
            html_content = file.read()

        # Если файл успешно прочитан, создаем HTTP-ответ
        http_response = create_http_response(html_content)  
    except FileNotFoundError:
        # Обработка случая, если файл не найден
        http_response = 'HTTP/1.1 404 NOT FOUND\r\n' 
        http_response += 'Content-Type: text/html\r\n' 
        http_response += '\r\n' 
        http_response += '<html><body><h1>404 Not Found</h1></body></html>'

    # Отправляем HTTP-ответ клиенту
    client_connection.sendall(http_response.encode())  
    client_connection.close()  # Закрываем соединение с клиентом
```