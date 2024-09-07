# Задание 2

## Текст задачи

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает у
сервера выполнение математической операции, параметры, которые вводятся с
клавиатуры. Сервер обрабатывает полученные данные и возвращает результат
клиенту.
Необходимо найти решение квадратного уравнения

Обязательно использовать библиотеку **socket**
Реализовать с помощью протокола TCP

## Листинг кода


### Сервер 

```python
import math
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime

def solver_server(socket_address: tuple[str, int] = ('localhost', 12345)):
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(socket_address)

    server.listen(5)
    # socket setup
    
    print(f'Started listening on {socket_address}')

    while True:
        # main loop
        try:
            client_socket, client_address = server.accept()
            print(f'Connected from {client_address}')
            message = client_socket.recv(1024).decode('utf-8')
            print(f'Received message from client: {message}\nValidating data...')
            params = validate_data(message)  # irrelevant helper function
            if params:
                solution = solve_quadratic(*params)  # irrelevant helper function
                print(f'The data is valid\nsending back to client at {datetime.now().time}: \n{solution}')
                client_socket.send(solution.encode('utf-8'))
            else:
                # if params are wrong
                print('The data is invalid')
                client_socket.send('Invalid parameters, try again.'.encode('utf-8'))
        except KeyboardInterrupt:
            print('shutting down')
            server.close()
            return


if __name__ == '__main__':
    solver_server()


```

### Клиент

```python
from socket import socket, AF_INET, SOCK_STREAM


def tcp_client(server_address: tuple[str, int] = ('localhost', 12345)):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(server_address)

    data = input("give me the 'a b c' of a quadratic equation for me to solve: ")
    client_socket.send(data.encode('UTF-8'))
    print(client_socket.recv(1024).decode('UTF-8'))
    client_socket.close()


if __name__ == "__main__":
    tcp_client()

```

## Детализация

TCP соединение требует процедуры рукопожатия между клиентом и сервером. 