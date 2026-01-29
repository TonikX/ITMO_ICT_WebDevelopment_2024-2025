import socket
import math
import json

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 8080)
server_socket.bind(server_address)

server_socket.listen(1)

print(f"TCP сервер запущен на {server_address[0]}:{server_address[1]}")
print("Ожидание подключения клиента...\n")

client_socket, client_address = server_socket.accept()
print(f"Подключен клиент: {client_address}")

try:
    data = client_socket.recv(1024).decode('utf-8')
    print(f"Получены данные от клиента: {data}")
    
    request = json.loads(data)
    operation = request.get('operation')
    
    if operation == 'pythagorean':
        a = float(request.get('a'))
        b = float(request.get('b'))
        
        print(f"Вычисление теоремы Пифагора: a={a}, b={b}")
        
        c = math.sqrt(a**2 + b**2)
        
        response = {
            'status': 'success',
            'result': c,
        }
        
        print(f"Результат вычисления: c = {c:.4f}")
    else:
        response = {
            'status': 'error',
            'message': 'Неизвестная операция'
        }
    
    client_socket.sendall(json.dumps(response).encode('utf-8'))
    print("Результат отправлен клиенту")

except Exception as e:
    error_response = {
        'status': 'error',
        'message': str(e)
    }
    client_socket.sendall(json.dumps(error_response).encode('utf-8'))
    print(f"Ошибка при обработке запроса: {e}")

finally:
    client_socket.close()
    print("Соединение с клиентом закрыто")
    
    server_socket.close()
    print("Сервер завершил работу")