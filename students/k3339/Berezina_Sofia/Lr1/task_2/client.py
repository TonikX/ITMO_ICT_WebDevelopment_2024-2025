import socket

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(('127.0.0.1', 14900))

a, h = input(), input()
conn.send(a.encode('utf-8') + b' ' + h.encode('utf-8'))
conn.close()