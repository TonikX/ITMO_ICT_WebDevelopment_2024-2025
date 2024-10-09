### Задание 5:

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

Сервер должен:
- Принять и записать информацию о дисциплине и оценке по дисциплине.
- Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

### Ход работы:

#### server.py

```
import socket
import threading

grades = []


def client_handler(client_socket):
    request = client_socket.recv(1024).decode()

    lines = request.splitlines()
    if len(lines) > 0:
        method, path = lines[0].split()[0], lines[0].split()[0]

        if method == 'GET':
            html_content = """<html><head>
        <title>Grades Tracker</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }</style>
            </head><body>"""

            html_content += "<h1>Grades Tracker</h1>"
            html_content += "<table border='1'><tr><th>Subject</th><th>Grade</th></tr>"

            for subject, grade in grades:
                html_content += f"<tr><td>{subject}</td><td>{grade}</td></tr>"

            html_content += "</table>"
            html_content += """
                <h2>Add Grade</h2>
                <form method="POST" action="/">
                    Subject: <input type="text" name="subject"><br>
                    Grade: <input type="text" name="grade"><br>
                    <input type="submit" value="Submit">
                </form>
                </body></html>
                """

            response = html_content.encode()

            client_socket.sendall(b'HTTP/1.1 200 OK\r\n'
                                  b'Content-Type: text/html\r\n'
                                  b'Content-Length: ' + str(len(response)).encode() + b'\r\n'
                                                                                      b'\r\n'
                                  + response)

        elif method == 'POST':
            content_length = int(
                [line for line in lines if line.startswith('Content-Length:')][0].split(': ')[1])
            body = request.split('\r\n\r\n')[1][:content_length]
            subject, grade = body.split('&')
            subject = subject.split('=')[1]
            grade = grade.split('=')[1]

            grades.append([subject, grade])
            response = b'HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n'
            client_socket.sendall(response)

        client_socket.close()


serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_address = ('localhost', 8080)
serv_sock.bind(serv_address)
serv_sock.listen()
print('server is connected and listening:', serv_address)

while True:
    cl_socket, cl_address = serv_sock.accept()
    print(f'{cl_address} is doing something')
    thread = threading.Thread(target=client_handler, args=(cl_socket,))
    thread.start()
```

В данном задании объединяем знания работы с html-структурой из 3 задания и внедрения библиотека 
threading из 4 задания.

После успешной настройки сокета и соединения хоста настраиваем прослушивание запросов. Пока 
программа работает, сервер принимает запросы клиентов, сообщая об их активной работе, и 
запускает потоки для работы многих клиентов одновременно. Потоки работают на основе функции 
`client_handler`, обрабатывая запросы. При методе GET сервер формирует таблицу с записанными 
оценками, при методе POST записывает новые пары предмет-оценка в список отметок.

Чтобы убедиться в работе сайта, переходим по заданному адресу `http://localhost:8080`