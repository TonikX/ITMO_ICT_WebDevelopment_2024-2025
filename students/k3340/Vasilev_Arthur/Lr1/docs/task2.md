# Задание 2: TCP калькулятор площади параллелограмма

## Описание

Реализован TCP клиент-сервер для вычисления площади параллелограмма по формуле S = основание × высота.

## Файлы реализации

- `client.py` - TCP клиент с интерфейсом
- `server.py` - TCP сервер

## Код клиента

```python
import socket

def display_menu():
    """Отображает меню для пользователя"""
    print("\n" + "="*50)
    print("КЛИЕНТ ДЛЯ РАСЧЕТА ПЛОЩАДИ ПАРАЛЛЕЛОГРАММА")
    print("="*50)
    print("Формула: Площадь = основание × высота")
    print("Пример ввода: 5,3 (основание 5, высота 3)")
    print("Команды:")
    print("  - Введите числа через запятую для расчета")
    print("  - 'exit' для выхода")
    print("="*50)

def start_client():
    """Запускает TCP клиент"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 8082)

    print("Клиент запущен")

    try:
        client_socket.connect(server_address)
        print(f"Успешно подключен к серверу {server_address}")

        display_menu()

        while True:
            user_input = input("\nВведите основание и высоту (через запятую): ").strip()

            if user_input.lower() == 'exit':
                client_socket.send('exit'.encode('utf-8'))
                print("Завершение работы клиента...")
                break

            if not user_input:
                print("Ошибка: Введите данные")
                continue

            if ',' not in user_input:
                print("Ошибка: Используйте формат 'основание,высота'")
                continue

            client_socket.send(user_input.encode('utf-8'))

            response = client_socket.recv(1024).decode('utf-8')

            print(f"\nРезультат: {response}")

            continue_calc = input("\nПродолжить вычисления? (y/n): ").strip().lower()
            if continue_calc != 'y':
                client_socket.send('exit'.encode('utf-8'))
                print("Завершение работы...")
                break

    except ConnectionRefusedError:
        print("Ошибка: Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
    except KeyboardInterrupt:
        print("\nКлиент остановлен пользователем")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
    finally:
        client_socket.close()
        print("Соединение закрыто")

if __name__ == "__main__":
    start_client()
```

## Код сервера

```python
import socket
import math

def calculate_parallelogram_area(base, height):
    """Вычисляет площадь параллелограмма: S = base * height"""
    return base * height

def handle_client_connection(client_socket, client_address):
    """Обрабатывает соединение с клиентом"""
    print(f"Подключен клиент: {client_address}")

    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')

            if not data:
                print(f"Клиент {client_address} отключился")
                break

            if data.lower() == 'exit':
                print(f"Клиент {client_address} запросил отключение")
                client_socket.send("Сервер завершил соединение".encode('utf-8'))
                break

            print(f"Получены данные от клиента: {data}")

            try:
                base, height = map(float, data.split(','))

                area = calculate_parallelogram_area(base, height)

                response = f"Площадь параллелограмма с основанием {base} и высотой {height} = {area:.2f}"

            except ValueError as e:
                response = f"Ошибка: Неверный формат данных. Ожидается: основание,высота. Пример: 5,3"
            except Exception as e:
                response = f"Ошибка при вычислении: {str(e)}"

            client_socket.send(response.encode('utf-8'))
            print(f"Отправлен ответ: {response}")

    except ConnectionResetError:
        print(f"Клиент {client_address} неожиданно отключился")
    except Exception as e:
        print(f"Ошибка при работе с клиентом {client_address}: {str(e)}")
    finally:
        client_socket.close()
        print(f"Соединение с клиентом {client_address} закрыто")

def start_server():
    """Запускает TCP сервер"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 8082)
    server_socket.bind(server_address)
    server_socket.listen(5)

    print("TCP Сервер запущен и слушает на localhost:8082")
    print("Ожидание подключений...")
    print("Для остановки сервера нажмите Ctrl+C")

    try:
        while True:
            client_socket, client_address = server_socket.accept()

            handle_client_connection(client_socket, client_address)

    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем")
    finally:
        server_socket.close()
        print("Серверный сокет закрыт")

if __name__ == "__main__":
    start_server()
```

## Запуск

1. Запустите сервер: `python server.py`
2. В другом терминале запустите клиент: `python client.py`
3. Введите основание и высоту через запятую