import socket

server_address = ('localhost', 8080)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(server_address)
    
    a = input("Введите коэффициент a: ")
    b = input("Введите коэффициент b: ")
    c = input("Введите коэффициент c: ")
    
    message = f'{a},{b},{c}'
    sock.sendall(message.encode())
    print(f'Отправлены данные: a={a}, b={b}, c={c}')
    
    data = sock.recv(1024)
    print(f'Получен результат от сервера: {data.decode()}')
    
finally:
    sock.close()
