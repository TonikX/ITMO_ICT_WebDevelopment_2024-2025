import socket
import json

server_host = socket.gethostname()
server_port = 8000

input_data = input("Сторона и высота, проведенная к ней: ").strip().split(" ")
side, height = float(input_data[0].strip()), float(input_data[1].strip())


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_host, server_port))
client.send(json.dumps(dict(side=side, height=height)).encode())

response_data = client.recv(1024)

print(f"Площадь параллелограмма = {response_data.decode()}")
client.close()