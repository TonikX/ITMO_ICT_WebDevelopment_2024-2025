# Задание 1: UDP клиент-сервер

## Описание

Реализован простой UDP клиент и сервер для обмена сообщениями. Клиент отправляет "Hello, server", сервер отображает сообщение и отвечает "Hello, client".

## Файлы реализации

- `client.py` - UDP клиент
- `server.py` - UDP сервер

## Код клиента

```python
import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('localhost', 8081)

    print("Клиент запущен")
    print("Для выхода введите 'exit'")

    try:
        while True:
            message = input("Введите сообщение для сервера: ")

            client_socket.sendto(message.encode('utf-8'), server_address)

            if message.lower() == 'exit':
                print("Завершение работы клиента")
                break

            # Ждем ответ от сервера
            data, _ = client_socket.recvfrom(1024)
            response = data.decode('utf-8')

            print(f"Получен ответ от сервера: {response}")

    except KeyboardInterrupt:
        print("\nКлиент остановлен пользователем")
    except ConnectionRefusedError:
        print("Ошибка: Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
    finally:
        # Всегда закрываем сокет
        client_socket.close()
        print("Сокет клиента закрыт")

# Запускаем клиент, только если файл запущен напрямую
if __name__ == "__main__":
    start_client()
```

## Код сервера

```python
import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('localhost', 8081)

    server_socket.bind(server_address)

    print("Сервер запущен и слушает на localhost:8081")
    print("Ожидание сообщения от клиента...")

    try:
        while True:
            data, client_address = server_socket.recvfrom(1024)

            message = data.decode('utf-8')
            print(f"Получено от {client_address}: {message}")

            if message.lower() == 'exit':
                response = "Сервер завершает работу"
                server_socket.sendto(response.encode('utf-8'), client_address)
                print("Завершение работы сервера по запросу клиента")
                break

            response = "Hello, client"

            server_socket.sendto(response.encode('utf-8'), client_address)
            print(f"Отправлен ответ клиенту: {response}")

    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем")
    finally:
        server_socket.close()
        print("Сокет сервера закрыт")

if __name__ == "__main__":
    start_server()
```

## Запуск

1. Запустите сервер: `python server.py`
2. В другом терминале запустите клиент: `python client.py`
3. Введите сообщение в клиенте