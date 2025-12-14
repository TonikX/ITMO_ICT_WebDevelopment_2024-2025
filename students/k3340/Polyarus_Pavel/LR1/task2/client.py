import socket
import json

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 8080)

print("Вычисление теоремы Пифагора")
print("Формула: c = √(a² + b²)")
print("-" * 40)

try:
    a = float(input("Введите длину катета a: "))
    b = float(input("Введите длину катета b: "))
    
    if a <= 0 or b <= 0:
        print("Ошибка: длины катетов должны быть положительными числами!")
        exit(1)
    
    print(f"\nПодключение к серверу {server_address[0]}:{server_address[1]}...")
    client_socket.connect(server_address)
    print("Подключение установлено")
    
    request = {
        'operation': 'pythagorean',
        'a': a,
        'b': b
    }
    
    print(f"Отправка данных на сервер: a={a}, b={b}")
    client_socket.sendall(json.dumps(request).encode('utf-8'))
    
    data = client_socket.recv(1024).decode('utf-8')
    response = json.loads(data)
    
    print("\nОтвет от сервера:")
    print("-" * 40)
    
    if response['status'] == 'success':
        print(f"Результат: c = {response['result']:.4f}")
    else:
        print(f"Ошибка: {response['message']}")

except ValueError:
    print("Ошибка: введите корректные числовые значения!")
except ConnectionRefusedError:
    print("Ошибка: не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    client_socket.close()
    print("\nКлиент завершил работу")