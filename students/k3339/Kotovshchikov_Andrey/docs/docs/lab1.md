# Лабораторная работа 1. Работа с сокетами.

---

## **Задание 1**

**Клиент:**

```python
import socket

SERVER_HOST = socket.gethostname()
SERVER_PORT = 8000
BUFFER_SIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto("Hello server".encode(), (SERVER_HOST, SERVER_PORT))

response_data, server_address = client.recvfrom(BUFFER_SIZE)
decoded_data = response_data.decode()
print(decoded_data)

client.close()
```

SERVER_HOST - имя хостовой машины (ip адрес сервера)

SERVER_PORT - порт, который слушает серверный сокет

BUFFER_SIZE - максимальное количество байт, которое мы читаем за раз

Так как протокол **UDP** не предоставляет гарантии доставки, предварительное соединение с сервером устанавливать не нужно. Мы просто создаем объект сокета (client), передавая ему в качестве аргументов **AF_INET** (означает, что мы используем в качестве сетевого протокола IPv4) и **SOCK_DGRAM** (означает, что мы используем в качестве транспортного протокола UDP). После этого мы отправляем серверу датаграмму с закодированным в **UTF-8** сообщением. Сервер отправляет ответное сообщение, которое мы читаем из нашего клиентского сокета с помощью метода **.recvfrom**, декодируем его и выводим на экран. В конце мы удаляем клиентский сокет с помощью метода **.close**.

**Сервер:**

```python
import socket

PORT = 8000
HOST = socket.gethostname()
MAX_CONNECTIONS = 10
BUFFER_SIZE = 1024


def serve():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))

    while True:
        request_data, client_address = server.recvfrom(BUFFER_SIZE)
        decoded_data = request_data.decode()
        print(decoded_data)
        server.sendto("Hello client".encode(), client_address)

    server.close()


if __name__ == "__main__":
    serve()
```

SERVER_HOST - имя хостовой машины (ip адрес, который слушает сервер)

SERVER_PORT - порт, который слушает серверный сокет

MAX_CONNECTIONS - максимальный размер очереди из еще не принятых подлючений (если количество соединений превысит данное значение, последующие будут отброшены)

BUFFER_SIZE - максимальное количество байт, которое мы читаем за раз

Код сервера очень похож на код клиента, за исключением пары моментов. Мы вызываем метод **.bind**, который и делает наш сокет серверным. Далее идет бесконечный цикл, в котором мы читаем данные и адреса (IP + порт) клиентов. После этого мы декодируем сообщение, печатаем его на экран и отправляем по полученному клиентскому адресу ответное сообщение.

## **Задание 2**

**Клиент:**

```python
import socket
import json

SERVER_HOST = socket.gethostname()
SERVER_PORT = 8000
BUFFER_SIZE = 1024

a, b = map(
    lambda cathet: float(cathet.strip()),
    input("Катеты прямоугольного треугольника ").strip().split(","),
)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOST, SERVER_PORT))
client.send(json.dumps(dict(a=a, b=b)).encode())

response_data = client.recv(BUFFER_SIZE)
hypotenuse = float(response_data.decode())

print(f"Гипотенуза = {hypotenuse}")
client.close()
```

В данном задании мы используем в качестве транспортного протокола TCP, а не UDP. TCP, в отличие от UDP, предоставляет гарантии доставки сообщений. Перед тем как начать отправлять сообщения, мы должны установить соединение с сервером (метод **.connect**). Далее, согласно заданию, мы сериализуем введенные данные в формат **JSON** и отправляем их серверу. Сервер, в свою очередь, отправляет нам ответное сообщение с вычисленным результатом, который мы печатаем на экран. В конце закрываем соединение, используя метод **.close**.

**Сервер:**

```python
import math
import socket
import json

HOST = socket.gethostname()
PORT = 8000
MAX_CONNECTIONS = 10
BUFFER_SIZE = 1024


def calculate_hypotenuse(a: float, b: float) -> float:
    return math.sqrt(a**2 + b**2)


def serve():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNECTIONS)

    while True:
        client, _ = server.accept()
        request_data = client.recv(BUFFER_SIZE)
        cathets = dict(json.loads(request_data))
        hypotenuse = calculate_hypotenuse(**cathets)
        client.send(f"{hypotenuse}".encode())

    server.close()


if __name__ == "__main__":
    serve()
```

Серверный код начинается с создания экземпляра сокета с указанием сетевого и транспортного протокола соответственно (**AF_INET / IPv4** и **SOCK_STREAM / TCP**). Далее используется метод **.bind**, чтобы сделать сокет серверным, и вызывается метод **.listen** с указанием максимального количества еще не принятых соединений. После этого запускается бесконечный цикл, в котором мы принимаем подключения клиентов (**.accept**), читаем данные из запроса, десериализуя их из **JSON** формата в словарь (dict), выполняем операцию и возвращаем результат клиенту.

## **Задание 3**

**Сервер:**

```python
import pathlib
import socket

HOST = "127.0.0.1"
PORT = 8000
MAX_CONNECTIONS = 10
BUFFER_SIZE = 1024
BASE_DIR = pathlib.Path("third")


def serve():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNECTIONS)

    while True:
        client, _ = server.accept()
        client.recv(BUFFER_SIZE)
        client.send(b"HTTP/1.1 200 OK\n")
        client.send(b"Content-Type: text/html\n")
        client.send(b"\n")
        client.send((BASE_DIR / "index.html").read_bytes())

    server.close()


if __name__ == "__main__":
    serve()
```

Для того чтобы отрисовать **HTML-страницу** в браузере, нам необходимо реализовать протокол прикладного уровня **HTTP**, который, в свою очередь, работает поверх протокола транспортного уровня **TCP**. Это делается путем указания специальных данных (заголовков). Для того чтобы браузер смог отобразить HTML-страницу, нам достаточно указать:

    HTTP/1.1 200 OK - начальная строка, в которой через пробел указаны версия протола HTTP (в нашем слечае 1.1) и статус код (200 OK означает успешное получение данных).

    Content-Type: text/html - Заголовок ответа, который говорит браузеру, что данные, полученные в ответе, стоит интерпретировать как html страницу.

## **Задание 4**

**Читатель:**

```python
import socket

SERVER_HOST = socket.gethostname()
SERVER_PORT = 8000
BUFFER_SIZE = 1024


chat_id = input("Идентификатор чата ").strip()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOST, SERVER_PORT))
client.send(chat_id.encode())


while True:
    message = client.recv(BUFFER_SIZE)
    print(f"Получено новое сообщение: {message.decode()}")

client.close()
```

В данном задании было задействовано два клиентских сокета, чтобы чтение не блокировало запись и наоборот. Читающий сокет подключается к групповому чату, используя однобайтовый идентификатор **chat_id**. Затем, в бесконечном цикле мы ждем новых сообщений от участников чата и, как только в нашем чате появится новое сообщение, мы читаем его из буфера сокета и выводим на экран.

**Отправитель:**

```python
import socket

SERVER_HOST = socket.gethostname()
SERVER_PORT = 8000
BUFFER_SIZE = 1024


chat_id = input("Идентификатор чата ").strip()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOST, SERVER_PORT))
client.send(chat_id.encode())


while True:
    message = input("Сообщение ").strip()
    client.send(message.encode())
    if message == "exit":
        break

client.close()
```

Сокет-отправитель, также как и сокет-читатель, подключается к одноименному чату, используя **chat_id**. Идентификатор чата отправляется непосредственно перед отправкой самого сообщения. Далее, в бесконечном цикле мы вводим текст сообщения через консоль, после чего оно отправляется на сервер. Для реализации выхода из чата было предусмотрено специальное сообщение **exit**, сообщающее серверу, что клиент желает отключиться и его следует удалить из чата.

**Сервер:**

```python
import socket
import threading

HOST = socket.gethostname()
PORT = 8000
MAX_CONNECTIONS = 10
CHAT_ID_SIZE = 1
MESSAGE_SIZE = 1024

type ChatId = str
type Socket = socket.socket
lock = threading.Lock()


class ChatConnectionManager:
    _chat_connections: dict[ChatId, list[Socket]]

    def __init__(self) -> None:
        self._chat_connections = dict()

    def connect_client_to_chat(self, chat_id: str, client: Socket) -> None:
        is_chat_exists = self._chat_connections.get(chat_id, None) is not None
        if not is_chat_exists:
            self._chat_connections[chat_id] = []

        self._chat_connections[chat_id].append(client)

    def disconnect_client_from_chat(self, chat_id: str, client: Socket) -> None:
        chat_connections = self._chat_connections.get(chat_id, None)
        if chat_connections is None:
            return

        chat_connections.remove(client)
        client.close()

    def send_message(self, chat_id: str, message: str) -> None:
        chat_connections = self._chat_connections.get(chat_id, None)
        if chat_connections is None:
            return

        for client_socket in chat_connections:
            client_socket.send(message.encode())


chat_connection_manager = ChatConnectionManager()


def consume_client(client: Socket) -> None:
    chat_id = client.recv(CHAT_ID_SIZE).decode()
    with lock:
        chat_connection_manager.connect_client_to_chat(chat_id, client)

    while True:
        message = client.recv(MESSAGE_SIZE).decode()
        if message == "exit":
            chat_connection_manager.disconnect_client_from_chat(chat_id, client)
            break

        chat_connection_manager.send_message(chat_id=chat_id, message=message)


def serve():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNECTIONS)

    while True:
        client, _ = server.accept()
        thread = threading.Thread(
            target=consume_client,
            args=(client,),
        )

        thread.start()

    server.close()


if __name__ == "__main__":
    serve()
```

Сам сервер стартует с функции **serve**, в которой мы инициализируем серверный TCP-сокет, и затем в бесконечном цикле ждем подключения клиентов. Как только к нам приходит запрос на подключение, мы создаем новый **поток (thread)** и запускаем в нем функцию **consume_client**, в которую в качестве аргумента передается сокет клиента, которого мы только что подключили. На каждого нового клиента выделяется отдельный поток. Сделано это для того, чтобы методы **recv** и **send** не блокировали основной поток сервера, и он мог продолжать принимать соединения. Системные вызовы для чтения данных из сокета и записи данных в сокет по умолчанию являются блокирующими. Поэтому, в случае если мы не используем потоки, до тех пор пока один клиент не "отвиснет", остальные будут вынуждены его ждать.

Класс **ChatConnectionManager**, реализующий поведенческий паттерн проектирования **Observer**, отвечает за отправку сообщений всем клиентам, находящимся в одном чате. Стоит отметить, что во время вызова метода **.connect_client_to_chat** функцией **consume_client** может возникнуть состояние гонки:

**Фрагмент кода, где может возникнуть состояние гонки:**

```python
 def connect_client_to_chat(self, chat_id: str, client: Socket) -> None:
        is_chat_exists = self._chat_connections.get(chat_id, None) is not None
        if not is_chat_exists:
            self._chat_connections[chat_id] = []

        self._chat_connections[chat_id].append(client)
```

Поэтому, чтобы избежать потенциальных проблем с **race condition** была использована **блокировка (threading.Lock())**, которая гарантирует, что в каждый момент времени только один поток будет исполнять выделенный код, а все остальные будут ждать снятия блокировки.

## **Задание 5**

**Сервер:**

```python
from io import BufferedReader
import socket
import re
import sys

from event_loop import EventLoop, TaskType
from exception import ServerExeption
from response import Response
from request import Request
from routes import get_all_subjects, save_subject

type Socket = socket.socket


class HTTPServer:
    _max_line: int = 64 * 1024
    _max_headers: int = 100
    _host: str
    _port: int

    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port

    def serve_forever(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.bind((self._host, self._port))
            server.listen()
            while True:
                yield (TaskType.TO_READ, server)
                connection, _ = server.accept()

                try:
                    event_loop.create_task(self.serve_client(connection))
                except Exception as exc:
                    print(exc)
        finally:
            server.close()

    def serve_client(self, connection: Socket):
        try:
            yield (TaskType.TO_READ, connection)
            request = self.parse_request(connection)
            response = self.handle_request(request)

            yield (TaskType.TO_WRITE, connection)
            self.send_response(connection, response)

        except ServerExeption as exc:
            print(exc)
            error_response = Response(status_code=exc.status_code, reason=exc.reason)
            self.send_response(connection, error_response)

        except Exception as exc:
            print(exc)
            error_response = Response(status_code=500, reason="Internal Server Error")
            self.send_response(connection, error_response)

        finally:
            connection.close()

    def parse_request(self, connection: Socket):
        stream = connection.makefile("rb")
        raw = stream.readline(self._max_line + 1)
        if len(raw) > self._max_line:
            raise ServerExeption(431, "Too long request line")

        line = raw.decode("iso-8859-1").rstrip("\r\n")
        line_parts = line.split()
        if len(line_parts) != 3:
            raise ServerExeption(400, "Malformed request line")

        method, url, version = line_parts
        headers = self.parse_headers(stream)

        return Request(
            method=method,
            url=url,
            version=version,
            stream=stream,
            headers=headers,
        )

    def parse_headers(self, stream: BufferedReader):
        headers = dict()
        while True:
            line = stream.readline(self._max_line + 1)
            if len(line) > self._max_line:
                raise ServerExeption(431, "Too long header line")

            if line in (b"\r\n", b"\n", b""):
                break

            header, value = line.decode("iso-8859-1").split(":", 1)
            headers[header] = value.rstrip("\r\n")
            if len(headers) > self._max_headers:
                raise ServerExeption(431, "Too many headers")

        return headers

    def handle_request(self, request: Request):
        if not re.fullmatch(r"\/subjects\/\d+", request.path):
            raise ServerExeption(404, "Not found")

        student_id = request.path[len("/subjects/") :]
        response = None
        if request.method == "GET":
            response = get_all_subjects(request=request, student_id=int(student_id))

        elif request.method == "POST":
            response = save_subject(request=request, student_id=int(student_id))

        if response is None:
            raise ServerExeption(405, "Method not allowed")

        return response

    def send_response(self, connection: Socket, response: Response):
        stream = connection.makefile("wb")
        status_line = f"HTTP/1.1 {response.status_code} {response.reason}\r\n"
        stream.write(status_line.encode("iso-8859-1"))

        if response.headers:
            for key, value in response.headers.items():
                header_line = f"{key}: {value}\r\n"
                stream.write(header_line.encode("iso-8859-1"))

        stream.write(b"\r\n")
        if response.body is not None:
            stream.write(response.body)

        stream.flush()
        stream.close()


if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])

    server = HTTPServer(host, port)
    try:
        event_loop = EventLoop(main=server.serve_forever())
        event_loop.run()
    except KeyboardInterrupt:
        pass
```

В последнем задании был реализован полноценный **асинхронный** HTTP-веб-сервер. Сервер стартует с создания экземпляра класса **HTTPServer**, в который передаются хост и порт, указанные в аргументах командной строки. Затем, для реализации асинхронности и неблокирующего ввода/вывода создается объект класса **EventLoop**, код которого рассматривается ниже. В качестве параметра **main** передается генератор (вызов метода **.serve_forever**). В методе **.serve_forever** мы инициализируем серверный TCP-сокет, который ждет подключения клиентов. Вызов метода **.accept** у сокета является блокирующей операцией. Поэтому, перед тем как вызывать данный метод, мы делаем **yield** из генератора, передавая наружу кортеж, состоящий из указания операции, которую мы планируем выполнить с сокетом (в нашем случае **.accept** подразумевает чтение данных) и сам сокет. После того, как сокет станет доступным для чтения, метод **.serve_forever** выполнит **.accept**, который вернет сокет клиента, и отдаст его в **.serve_client**. В методе **.serve_client** мы также делаем **yield** перед вызовом блокирующей операции. Как только сокет станет доступным для чтения, мы распарсим запрос клиента (вместе с query-параметрами и заголовками) в методе **.parse_request**, сформируем объект ответа при помощи метода **.handle_request** и, как только клиентский сокет будет готов к записи, запишем в него ответ и отправим его при помощи метода **.send_response**.

**EventLoop:**

```python
import enum
from select import select
from typing import Generator


class TaskType(enum.StrEnum):
    TO_READ = "to_read"
    TO_WRITE = "to_write"


class EventLoop:
    _tasks: list[Generator]
    _to_read: dict
    _to_write: dict

    def __init__(self, main: Generator) -> None:
        self._tasks = [main]
        self._to_read = dict()
        self._to_write = dict()

    def run(self):
        while any([self._to_read, self._to_write, self._tasks]):
            while not self._tasks:
                ready_to_read, ready_to_write, _ = select(
                    self._to_read,
                    self._to_write,
                    [],
                )

                for socket in ready_to_read:
                    self._tasks.append(self._to_read.pop(socket))

                for socket in ready_to_write:
                    self._tasks.append(self._to_write.pop(socket))

            current_task = self._tasks.pop(0)
            try:
                task_type, socket = next(current_task)
            except StopIteration:
                continue

            if task_type == TaskType.TO_READ:
                self._to_read[socket] = current_task

            elif task_type == TaskType.TO_WRITE:
                self._to_write[socket] = current_task

    def create_task(self, task: Generator):
        self._tasks.append(task)
```

Для реализации неблокирующего ввода/вывода был написан кастомный **EventLoop**, который при помощи системного вызова **select** отслеживает готовность сокетов к чтению (**to_read**) или записи (**to_write**). Сам по себе **EventLoop** представляет из себя бесконечный цикл, в котором при отсутствии готовых к выполнению задач (список **tasks**) срабатывает вложенный цикл (цикл ожидания задач). Цикл ожидания задач использует системный вызов **select**, передавая ему сокеты, состояние которых мы хотим отслеживать. Вызов select блокирует поток выполнения до тех пор, пока хотя бы один сокет не будет готов для чтения или записи.

После того как **select** вернет списки из сокетов, готовых для чтения (**ready_to_read**) и сокетов, готовых для записи (**ready_to_write**), происходит итерирование по обоим спискам и добавление в список **tasks** функций (генераторов), которые ранее прервали свое выполнение при помощи **yield**. Затем, для каждого генератора, находящегося в **tasks**, производится вызов **next**, и генератор начинает выполнение с момента предыдущего вызова **yield**. Генератор может либо закончить свое выполнение (произойдет исключение **StopIteration**), либо еще раз вызвать **yield** и вернуть сокет, который нужно отслеживать на состояние готовности к чтению или записи. Если происходит второй вариант, мы в соответствующий словарь добавляем в качестве ключа сокет, а в качестве значения — сам генератор. После этого все повторяется заново.
