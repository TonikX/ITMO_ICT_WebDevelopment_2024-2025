import socket
import json

from urllib.parse import parse_qs

IP = '127.0.0.1'
PORT = 2020

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()

def page():
  with open('marks.json') as f:
    m = json.load(f)
  headers = b'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
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
  return headers + content.encode('utf-8')

try:
  while True:
    client, address = server.accept()
    data = client.recv(1024).decode('utf-8').split('\n')
    method, path, _ = data[0].split()
    if method == 'POST':
      query = parse_qs(data[-1])
      with open('marks.json') as f:
        m = json.load(f)
      with open('marks.json', 'w') as f:
        m[query['subject'][0]] = int(query['mark'][0])
        json.dump(m, f)
    client.send(page())
    client.shutdown(socket.SHUT_WR)
except KeyboardInterrupt:
  server.close()