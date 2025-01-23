Задание:
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

Вариант операции:
Поиск площади трапеции.

Требования:

Обязательно использовать библиотеку socket.
Реализовать с помощью протокола TCP.

Листинг кода серверной части:
```
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 9090))
server_socket.listen(10)
server_socket.settimeout(1)

try:
    while True:
        try:
            client_socket, address = server_socket.accept()
            client_socket.send(
                "Введите через запятую без пробелов значения a, b и h".encode()
            )

            data = client_socket.recv(1024).decode()
            try:
                a, b, h = (float(num) for num in data.split(","))
                calculation = (a + b) / 2 * h
                client_socket.send(f"Площадь трапеции: {calculation}".encode())
            except ValueError:
                client_socket.send("Ошибка ввода: убедитесь, что введены числа через запятую.".encode())

            client_socket.close()  # закрываем соединение с клиентом

        except socket.timeout:
            pass

except KeyboardInterrupt:
    server_socket.close()

```
Листинг кода клиентской части:
```
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 9090))

question = client_socket.recv(1024).decode() #вопрос от сервера 
print(question)

abh = input()

client_socket.send(abh.encode()) #отправляем данные серверу

result = client_socket.recv(1024).decode()
print(result)

client_socket.close()

```

Объяснение:

1. С помощью socket.socket(socket.AF_INET, socket.SOCK_DGRAM) создается объект сокета, где socket.SOCK_STREAM отвечает за протокол TCP.
2. Подключение к серверу происходит через .connect.
3. .recv обеспечивает получение информационного сообщения.
4. На сервер с помощью .send отправляем и с помощью .recv получаем результат.
5. .close. закрывает соединение. 
6. Использованы дополнительные проверки для обработки неправильных значений при разбиении строки на числа (ValueError).
Если клиент ввёл некорректные данные, сервер отправит сообщение об ошибке.