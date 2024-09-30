import socket
import pickle

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((socket.gethostname(), 1234))

print("Введите коэффициенты квадратного уравнения: a, b, c\n")
a = int(input())
b = int(input())
c = int(input())
coefs = [a, b, c]

data = pickle.dumps(coefs)

conn.send(data)

result = conn.recv(1024)
result = pickle.loads(result)
print("Результат: ", result)

conn.close()