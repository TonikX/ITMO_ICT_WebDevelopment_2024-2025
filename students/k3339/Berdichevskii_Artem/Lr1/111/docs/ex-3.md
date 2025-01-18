# Задание 3

### Описание задачи

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее 
HTML-страницу, которая сервер подгружает из файла index.html.

### Реализация

##### Стэк
* Python: 3.10
* Библиотека: socket

**Серверная часть:**
```
import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        with open('index.html', 'rb') as f:
            html_content = f.read()

        http_header = f'''HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: {len(html_content)}

'''.encode('utf-8')

        conn.sendall(http_header + html_content)
```

**Клиентская часть:**
```
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		<title>Ex-3</title>
	</head>
	<body>
		Html ex-3
	</body>
</html>
```