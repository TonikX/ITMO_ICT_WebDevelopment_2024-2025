# Лабораторные по сокетам (Python стандартная библиотека)

## Быстрый старт

Лучше создать отдельную виртуальную среду:
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

### Задание 1 — UDP и Hello sever
Окно 1:
```bash
python task1_udp_hello/server_udp.py
```
Окно 2:
```bash
python task1_udp_hello/client_udp.py
```

### Задание 2 — TCP и Математика
Окно 1:
```bash
python task2_tcp_math/server_tcp_math.py
```
Окно 2 (интерактивный клиент):
```bash
python task2_tcp_math/client_tcp_math.py
```

### Задание 3 — HTTP сервер, отдающий index.html
```bash
python task3_http_static/http_file_server.py
```
Откройте браузер: http://127.0.0.1:8080

### Задание 4 — Многопользовательский чат (TCP + threads)
Окно 1 (сервер):
```bash
python task4_chat/chat_server.py
```
Окна 2..N (клиенты):
```bash
python task4_chat/chat_client.py
```

### Задание 5 — HTTP сервер с GET/POST (оценки)
```bash
python task5_http_grades/grades_server.py
```
Откройте http://127.0.0.1:9090 и добавляйте записи через форму.

## Протоколы

- **UDP**: датаграммный протокол без установления соединения и гарантий доставки. Подходит для простых сообщений/пинга.
- **TCP**: потоковый, с установлением соединения и гарантированной доставкой и порядком байт. Удобен для RPC/запрос-ответ.
- **HTTP**: текстовый прикладной протокол (обычно поверх TCP). В заданиях 3 и 5 мы вручную формируем статусную строку, заголовки и тело.

