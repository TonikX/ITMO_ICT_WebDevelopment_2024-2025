import socket

conn = socket.socket()

conn.connect(("127.0.0.1", 14901))

request = b"Hello, server"
conn.send(request)

response = b""
tmpShot = conn.recv(1024)
response += tmpShot

print(f"Response: {response.decode("utf-8")}")
conn.close()