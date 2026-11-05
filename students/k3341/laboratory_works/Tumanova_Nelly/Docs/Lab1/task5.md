# Задание №5: Простой веб-сервер (GET/POST)

## Постановка задачи

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python. Сервер должен:

- принимать и записывать информацию о дисциплине и оценке по дисциплине;
- отдавать информацию обо всех оценках по дисциплинам в виде HTML-страницы;
- группировать журнал по предмету.

Требования:

- [x] Обязательно использовать библиотеку socket
- [x] Поддержка GET и POST
- [x] Хранение с группировкой по дисциплине
- [x] Отдача HTML-страницы

## Выполнение

### `grades.json`

```json
{
  "Прога": ["2", "5", "1", "3"],
  "Матан": ["1"],
  "WEB": ["5", "5", "5", "5", "5", "5", "5", "5", "5", "5"]
}
```

Файл-хранилище. Ключ — название дисциплины, значение — список оценок. Такая структура обеспечивает группировку по
предмету: все оценки одной дисциплины хранятся в одном списке, а не отдельными записями.

### `server.py`

```python
import json
import os
import socket
import threading
import urllib.parse
from collections import defaultdict


class GradesServer:
    HOST = ""
    PORT = 9090
    DATA_FILE = "grades.json"

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.grades = defaultdict(list)
        self.grades_lock = threading.Lock()

        self.load()

    def load(self):
        self.grades = defaultdict(list)
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
                    raw = json.load(f)
                for discipline, marks in raw.items():
                    self.grades[discipline] = marks
            except (OSError, json.JSONDecodeError):
                return

    def save(self):
        with open(self.DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(dict(self.grades), file, ensure_ascii=False, indent=2)

    def add_grade(self, discipline, grade):
        with self.grades_lock:
            self.grades[discipline].append(grade)
            self.save()

    def get_all(self):
        with self.grades_lock:
            return {d: list(marks) for d, marks in self.grades.items()}

    def start(self):
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(socket.SOMAXCONN)
        print(f"[*] HTTP-server started on {self.HOST}:{self.PORT}")

        while True:
            client_sock, client_addr = self.sock.accept()
            client_thread = threading.Thread(
                target=self.handle_client, args=(client_sock, client_addr), daemon=True
            )
            client_thread.start()

    def handle_client(self, client_sock, client_addr):
        try:
            request = self.read_request(client_sock)
            if request is None: return

            method, path, headers, body = request
            print(f"[{client_addr[0]}:{client_addr[1]}] {method} {path}")

            if method == 'GET' and path == '/':
                self.respond(client_sock, 200, self.render_page())
            elif method == 'POST' and path == '/':
                self.handle_post(client_sock, body)
            else:
                self.respond(client_sock, 404, "<h1>404 Not Found</h1>")
        except OSError:
            pass
        finally:
            client_sock.close()

    @staticmethod
    def read_request(client_sock):
        client_sock.settimeout(5.0)
        buffer = b''

        while b'\r\n\r\n' not in buffer:
            chunk = client_sock.recv(4096)
            if not chunk:
                return None
            buffer += chunk

        head, body = buffer.split(b'\r\n\r\n', 1)

        lines = head.decode('utf-8', errors='replace').split('\r\n')
        request_line = lines[0]
        parts = request_line.split()
        if len(parts) != 3:
            return None
        method, path, _ = parts

        headers = {}
        for line in lines[1:]:
            if ':' in line:
                k, v = line.split(':', 1)
                headers[k.strip().lower()] = v.strip()

        content_length = int(headers.get('content-length', 0))
        while len(body) < content_length:
            chunk = client_sock.recv(4096)
            if not chunk:
                break
            body += chunk

        return method, path, headers, body.decode('utf-8', errors='replace')

    def handle_post(self, client_sock, body):
        params = urllib.parse.parse_qs(body)
        discipline_raw = params.get("discipline", [""])[0]
        grade_raw = params.get("grade", [""])[0]

        status_disc, message_disc, discipline_clean = self.validate_discipline(discipline_raw)
        status_gr, message_gr, grade_clean = self.validate_grade(grade_raw)

        if status_disc and status_gr:
            self.add_grade(discipline_clean, grade_clean)
            self.respond(client_sock, 200, self.render_page(
                message="Оценка добавлена.",
                message_type="success",
            ))
        else:
            error = message_disc or message_gr
            self.respond(client_sock, 200, self.render_page(
                message=error,
                message_type="error",
                form_discipline=discipline_raw,
                form_grade=grade_raw,
            ))

    def validate_grade(self, grade: str):
        grade = grade.strip()
        if not grade:
            return False, "Оценка не может быть пустой.", None

        try:
            value = int(grade)
        except ValueError:
            return False, "Оценка должна быть целым числом от 1 до 5.", None

        if not (1 <= value <= 5):
            return False, "Оценка должна быть от 1 до 5.", None

        return True, None, str(value)

    def validate_discipline(self, discipline: str):
        discipline = discipline.strip()
        if not discipline:
            return False, "Название дисциплины не может быть пустым.", None
        if len(discipline) > 100:
            return False, "Название дисциплины слишком длинное (макс. 100 символов).", None
        return True, None, discipline

    def respond(self, client_sock, status, html):
        status_text = {200: 'OK', 404: 'Not Found'}.get(status, 'OK')
        body = html.encode('utf-8')
        headers = (
            f"HTTP/1.1 {status} {status_text}\r\n"
            f"Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body)}\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        )
        client_sock.sendall(headers.encode('utf-8') + body)

    def render_page(self, message=None, message_type=None, form_discipline='', form_grade=''):
        grades = self.get_all()

        if grades:
            rows = []
            for discipline, marks in grades.items():
                marks_str = ', '.join(self.escape(m) for m in marks)
                rows.append(
                    f"<tr>"
                    f"<td>{self.escape(discipline)}</td>"
                    f"<td>{marks_str}</td>"
                    f"<td>{len(marks)}</td>"
                    f"</tr>"
                )
            table = f"""
            <table>
                <thead>
                    <tr>
                        <th>Дисциплина</th>
                        <th>Оценки</th>
                        <th>Количество</th>
                    </tr>
                </thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
            """
        else:
            table = "<p>Пока нет оценок.</p>"

        if message:
            css_class = "error" if message_type == "error" else "success"
            alert = f'<div class="alert {css_class}">{self.escape(message)}</div>'
        else:
            alert = ''

        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>Журнал оценок</title>
    <style>
        body {{ font-family: sans-serif; max-width: 700px; margin: 40px auto; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
        th {{ background: #f0f0f0; }}
        form {{ margin-top: 20px; display: flex; gap: 8px; }}
        input, button {{ padding: 6px 10px; font-size: 14px; }}
        .alert {{
            padding: 10px 14px;
            margin: 16px 0;
            border-radius: 4px;
            border: 1px solid transparent;
        }}
        .alert.error {{
            background: #fdecea;
            border-color: #f5c6cb;
            color: #a94442;
        }}
        .alert.success {{
            background: #e8f5e9;
            border-color: #c8e6c9;
            color: #2e7d32;
        }}
    </style>
</head>
<body>
    <h1>Журнал оценок</h1>
    {alert}
    {table}

    <h2>Добавить оценку</h2>
    <form method="POST" action="/">
        <input type="text" name="discipline" placeholder="Дисциплина"
               value="{self.escape(form_discipline)}" required>
        <input type="text" name="grade" placeholder="Оценка"
               value="{self.escape(form_grade)}" required>
        <button type="submit">Добавить</button>
    </form>
</body>
</html>"""

    @staticmethod
    def escape(text):
        return (
            text.replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
        )

    def stop(self):
        self.sock.close()


if __name__ == '__main__':
    server = GradesServer()
    try:
        server.start()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
```

## Новые функции и приёмы

`json.load()` / `json.dump()` — сериализация журнала в файл `grades.json` и обратно. Позволяет сохранять оценки
между запусками сервера. `ensure_ascii=False` сохраняет кириллицу читаемой, `indent=2` — делает файл удобным для
просмотра.

`defaultdict(list)` — словарь, автоматически создающий пустой список при обращении к новому ключу. Удобно для
хранения оценок по дисциплинам: `self.grades["Матан"].append("5")` работает без предварительной инициализации ключа.

`load()` / `save()` — чтение и запись журнала в файл. `load()` вызывается в `__init__` при старте сервера,
`save()` — при каждом добавлении оценки. Обработка `OSError` и `json.JSONDecodeError` защищает от повреждённого файла.

`add_grade(discipline, grade)` — атомарно под блокировкой добавляет оценку в список нужной дисциплины и сохраняет
журнал на диск. Именно здесь реализована группировка по предмету: оценки не создают новых записей, а дописываются в
существующий список.

`get_all()` — возвращает копию журнала под блокировкой. Копия нужна, чтобы потоки-обработчики не видели изменений
словаря во время формирования HTML.

`read_request(client_sock)` — разбирает HTTP-запрос вручную:

- читает данные до разделителя `\r\n\r\n`, отделяющего заголовки от тела;
- из первой строки извлекает метод, путь и версию протокола;
- парсит заголовки в словарь;
- из заголовка `Content-Length` узнаёт длину тела и дочитывает его остаток.

Это ключевой приём задания — стандартная библиотека не разбирает HTTP автоматически, всё делается вручную.

`handle_post(client_sock, body)` — обработка POST-запроса. Тело имеет формат `application/x-www-form-urlencoded` (
`discipline=Матан&grade=5`), поэтому используется `urllib.parse.parse_qs()` для разбора параметров.

`validate_discipline()` / `validate_grade()` — валидация входных данных. Возвращают кортеж
`(успех, сообщение_об_ошибке, очищенное_значение)`. Проверяют, что дисциплина не пустая и не длиннее 100 символов, а
оценка — целое число от 1 до 5.

`respond(client_sock, status, html)` — формирует и отправляет HTTP-ответ. Заголовки отделяются от тела пустой
строкой `\r\n\r\n`, `Content-Length` равен длине тела в байтах, `Connection: close` закрывает соединение после ответа.

`render_page(...)` — генерирует HTML-страницу журнала. Таблица строится по данным `get_all()`: строки — дисциплины,
столбцы — список оценок и их количество. Форма для добавления оценки отправляет POST на `/`. Сообщение об успехе или
ошибке выводится через блок `.alert` с соответствующим CSS-классом.

`escape(text)` — экранирует спецсимволы HTML (`&`, `<`, `>`, `"`). Защищает от XSS: если пользователь введёт
`<script>`, он отобразится как текст, а не выполнится в браузере.

## Проверка

Запуск сервера:

```bash
$ python server.py
[*] HTTP-server started on :9090
```

Открыть в браузере `http://localhost:9090/` — отобразится таблица с оценками из `grades.json` и форма добавления. После
отправки формы новая оценка попадёт в соответствующую дисциплину (если дисциплина новая — создастся отдельная строка),
страница обновится с сообщением об успехе.

Пример запроса через `curl`:

```bash
$ curl -X POST -d "discipline=Матан&grade=4" http://localhost:9090/
```

После этого в `grades.json` у дисциплины «Матан» появится вторая оценка.

## Вывод

В ходе работы изучены приёмы ручной обработки HTTP поверх TCP:

- `read_request()` — разбор метода, пути, заголовков и тела запроса из сырого потока байт;
- `handle_post()` + `urllib.parse.parse_qs()` — извлечение параметров из `application/x-www-form-urlencoded`;
- `json.load()` / `json.dump()` — персистентное хранение журнала в файле;
- `defaultdict(list)` — структура данных с группировкой оценок по дисциплине;
- `respond()` — формирование корректного HTTP-ответа с заголовками `Content-Type`, `Content-Length`, `Connection`;
- `render_page()` — динамическая генерация HTML на основе текущего состояния журнала;
- `escape()` — защита от XSS при выводе пользовательских данных.

Ключевое отличие от предыдущего задания — сервер не просто отдаёт статический файл, а разбирает запрос, различает GET и
POST, для POST читает тело и сохраняет данные, а страницу собирает динамически из структурированного хранилища. Журнал
ведётся с группировкой по предмету: `defaultdict(list)` хранит все оценки одной дисциплины в одном списке, а не
отдельными строками.
