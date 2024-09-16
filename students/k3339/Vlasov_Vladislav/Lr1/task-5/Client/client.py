import socket

GET = b"GET http://localhost:14905?discipline=TEST HTTP/1.1\r\nHost: lb1\r\n\r\n"
POST = b"POST http://localhost:14905 HTTP/1.1\r\nHost: lb1\r\nContent-Length: 24\r\n\r\ndiscipline=TEST&mark=103"


conn = socket.socket()

conn.connect(("127.0.0.1", 14905))

request = GET
conn.send(request)

response = conn.recv(4096)

print(f"Response: {response.decode('utf-8')}")
conn.close()