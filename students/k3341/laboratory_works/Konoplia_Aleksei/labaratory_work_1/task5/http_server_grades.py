import socket
import threading
import urllib.parse

grades = []

def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    request_line = request.splitlines()[0]
    method, path, _ = request_line.split()

    if method == 'GET':
        if path == '/':
            response = '''HTTP/1.1 200 OK
                        Content-Type: text/html; charset=utf-8

                        <!DOCTYPE html>
                        <html lang="ru">
                        <head>
                            <meta charset="UTF-8">
                            <title>Оценки по дисциплинам</title>
                        </head>
                        <body>
                            <h1>Оценки по дисциплинам</h1>
                            <table border="1">
                                <tr>
                                    <th>Дисциплина</th>
                                    <th>Оценка</th>
                                </tr>'''
            for subject, grade in grades:
                response += f'''<tr>
                    <td>{subject}</td>
                    <td>{grade}</td>
                </tr>'''
            response += '''</table>
                                <h2>Добавить оценку</h2>
                                <form method="POST" action="/add_grade">
                                    Дисциплина: <input type="text" name="subject"><br>
                                    Оценка: <input type="text" name="grade"><br>
                                    <input type="submit" value="Добавить">
                                </form>
                            </body>
                            </html>'''
        else:
            response = '''HTTP/1.1 404 Not Found
                        Content-Type: text/html; charset=utf-8

                        <!DOCTYPE html>
                        <html lang="ru">
                        <head>
                            <meta charset="UTF-8">
                            <title>404 - Страница не найдена</title>
                        </head>
                        <body>
                            <h1>Страница не найдена</h1>
                        </body>
                        </html>'''
    elif method == 'POST':
        if path == '/add_grade':
            body = request.split('\r\n\r\n')[1]
            params = urllib.parse.parse_qs(body)
            subject = params.get('subject', [''])[0]
            grade = params.get('grade', [''])[0]
            
            if subject and grade:
                grades.append((subject, grade))
            
            response = '''HTTP/1.1 200 OK
                        Content-Type: text/html; charset=utf-8

                        <!DOCTYPE html>
                        <html lang="ru">
                        <head>
                            <meta charset="UTF-8">
                            <title>Оценки по дисциплинам</title>
                        </head>
                        <body>
                            <h1>Оценки по дисциплинам</h1>
                            <table border="1">
                                <tr>
                                    <th>Дисциплина</th>
                                    <th>Оценка</th>
                                </tr>'''
            for subject, grade in grades:
                response += f'''<tr>
                    <td>{subject}</td>
                    <td>{grade}</td>
                </tr>'''
            response += '''</table>
                                <h2>Добавить оценку</h2>
                                <form method="POST" action="/add_grade">
                                    Дисциплина: <input type="text" name="subject"><br>
                                    Оценка: <input type="text" name="grade"><br>
                                    <input type="submit" value="Добавить">
                                </form>
                            </body>
                            </html>'''

    else:
        response = '''HTTP/1.1 405 Method Not Allowed
                    Content-Type: text/html; charset=utf-8

                    <!DOCTYPE html>
                    <html lang="ru">
                    <head>
                        <meta charset="UTF-8">
                        <title>405 - Метод не разрешен</title>
                    </head>
                    <body>
                        <h1>Метод не разрешен</h1>
                    </body>
                    </html>'''

    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

def start_server(host='127.0.0.1', port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Сервер запущен на {host}:{port}")
    
    while True:
        client_socket, _ = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
