# Задание 5: 

## Описание задачи

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

## Код сервера
```python
import socket
import threading
import urllib.parse

# Хранилище для дисциплин и оценок
grades = []

#Функция для обработки GET и POST запросов
def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    headers = request.split('\n')

    #Проверяем, что запрос содержит хотя бы одну строку
    if len(headers) > 0 and len(headers[0].split()) >= 2:
        method, path = headers[0].split()[:2]
        
        if method == 'GET':
            #Возвращаем HTML-форму для ввода данных
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
            response += """
            <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Оценки</title>
                </head>
                <body>
                    <h2>Введите дисциплину и оценку</h2>
                    <form action="/" method="POST">
                        <label for="subject">Дисциплина:</label><br>
                        <input type="text" id="subject" name="subject"><br>
                        <label for="grade">Оценка:</label><br>
                        <input type="text" id="grade" name="grade"><br><br>
                        <input type="submit" value="Отправить">
                    </form>
                    <h2>Все оценки:</h2>
                    <ul>
            """
            #Выводим все сохраненные оценки с учетом кодировки
            for subject, grade in grades:
                response += f"<li>{subject}: {grade}</li>"
            response += "</ul></body></html>"

            client_socket.send(response.encode('utf-8'))

        elif method == 'POST':
            #Получаем данные из POST-запроса
            body = request.split('\r\n\r\n')[1]
            #Декодируем параметры URL (заменяем '%XX' на соответствующие символы)
            params = {param.split('=')[0]: urllib.parse.unquote(param.split('=')[1]) for param in body.split('&')}
            
            #Добавляем дисциплину и оценку в список
            subject = params['subject']
            grade = params['grade']
            grades.append((subject, grade))

            #Перенаправляем обратно на GET, чтобы обновить страницу
            response = "HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n"
            client_socket.send(response.encode())

    client_socket.close()

#Запуск веб-сервера
def start_server():
    server_address = ('localhost', 8080)
    
    #Создаем TCP-сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen()

    print(f"Сервер запущен и ожидает подключения на порту {server_address[1]}...")

    while True:
        client_socket, client_address = server_socket.accept()
        # Запускаем поток для обработки каждого клиента
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

#Запуск сервера
if __name__ == "__main__":
    start_server()
```