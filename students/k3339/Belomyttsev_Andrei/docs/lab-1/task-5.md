# Task 5

## Задание
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки `socket` в Python.

**Задание:**

  - Сервер должен:
    1. Принять и записать информацию о дисциплине и оценке по дисциплине.
    2. Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

**Полезные ссылки:**

  - [Базовый класс для веб-сервера](https://docs.google.com/document/d/1lv_3D9VtMxz8tNkA6rA1xu9zaWEIBGXiLWBo1cse-0k/edit?usp=sharing)
  - [Мануал по созданию сервера](https://iximiuz.com/ru/posts/writing-python-web-server-part-3/)

---

## HTTP server with GET and POST methods

You can choose specific IP address, port and marks path by changing `ip`, `port` and `marks_path` variables.

In order to connect to the server enter `127.0.0.1:PORT` into your browser's URL field.

You'll see web page with table of subjects and marks, and form for adding new subject and mark or changing existing. To edit the table enter *Subject* and *Mark*, then click *Submit*.

Subjects and marks are stored in `marks.json`.

Used classless CSS to make website prettier.

You can choose CSS by uncommenting specific line.

```python
# content += '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@exampledev/new.css@1/new.min.css">'
# content += '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.min.css">'
# content += '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/dark.min.css">'
content += '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/light.min.css">'
```

I recommend [new.css](https://github.com/xz/new.css) or [water.css](https://github.com/kognise/water.css)

[More classless CSS](https://github.com/dbohdan/classless-css)

---

## Code

5-oop.py:
```python
import socket
import json

from urllib.parse import parse_qs

class Server:
  server_socket = None

  def __init__(self, ip: str, port: int, marks_path: str):
    self.ip = ip
    self.port = port
    self.marks_path = marks_path

  def __del__(self):
    self.stop()

  def run(self):
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.bind((self.ip, self.port))
    self.server_socket.listen()
    while True:
      self.handle_request()
  
  def stop(self):
    if self.server_socket is not None:
      self.server_socket.close()

  def handle_request(self):
    client, address = self.server_socket.accept()
    method, path, http, query = self.parse_request(client.recv(1024).decode('utf-8'))
    if method == 'POST':
      self.set_mark(query['subject'][0], int(query['mark'][0]))
    self.send_response(client)
    client.shutdown(socket.SHUT_WR)
  
  def parse_request(self, data):
    data = data.split('\n')
    method, path, http = data[0].split()
    query = None
    if method == 'POST':
      query = parse_qs(data[-1])
    return method, path, http, query
  
  def set_mark(self, subject: str, mark: int):
    with open(self.marks_path) as f:
      m = json.load(f)
    with open(self.marks_path, 'w') as f:
      m[subject] = mark
      json.dump(m, f)

  def send_response(self, client):
    headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    client.send(headers.encode('utf-8') + self.generate_html().encode('utf-8'))

  def generate_html(self):
    with open(self.marks_path) as f:
      m = json.load(f)
      content = '''<!DOCTYPE html><html lang="en"><head>
      <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Subjects & Marks</title>'''
      # content += '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@exampledev/new.css@1/new.min.css">'
      # content += '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.min.css">'
      # content += '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/dark.min.css">'
      content += '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/light.min.css">'
      content += '</head><body><h1>Subjects & Marks</h1><table><tr><th>Subject</th><th>Mark</th></tr>'
      content += '\n'.join([f'<tr><td>{i[0]}</td><td>{i[1]}</td></tr>' for i in m.items()])
      content += '''</table><br><form action="/" method="POST">
      <label for="subject">Subject:</label><br>
      <input type="text" name="subject" id="subject"><br>
      <label for="mark">Mark:</label><br>
      <input type="number" name="mark" id="mark" min="0"><br>
      <input type="submit">
    </form></body></html>'''
      return content

if __name__ == '__main__':
  ip = '127.0.0.1'
  port = 2020
  marks_path = 'marks.json'
  server = Server(ip, port, marks_path)
  try:
    server.run()
  except KeyboardInterrupt:
    ...
```