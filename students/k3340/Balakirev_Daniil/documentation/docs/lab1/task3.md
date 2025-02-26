# Задание 3

## Текст задания

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

## Требования

*   Обязательно использовать библиотеку `socket`.

## Код


### index.html

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>qweqwewqewqewqewqeqw</title>
    </head>
    <body>

    </body>
    </html>

### client.py
    
    import socket

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 1234))

    response = client.recv(1024)
    print(response.decode())

    client.close()

### server.py

    import socket

    def read_html():
        with open('index.html', 'r') as file:
            return file.read()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 1234))
    server.listen(1)

    conn, addr = server.accept()
    html_content = read_html()

    response = f"""HTTP/1.1 200 OK
    Content-type: text/html
    {html_content}
    """

    conn.send(response.encode())
    conn.close()