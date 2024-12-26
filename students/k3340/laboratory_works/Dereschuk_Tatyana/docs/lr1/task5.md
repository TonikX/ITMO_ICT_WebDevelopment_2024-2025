# Задание 5

## Описание

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

## Стек

- Язык: Python
- Библиотека: socket
- Протокол: HTTP

## Как запускать

1. Сервер:
    ```bash
    python3 server.py
    ```
2. Обновление данных

   Через curl:

       curl -X POST -d "subject=Web&grade=5" http://localhost:8080/
       curl --data "subject=Comp&grade=3" http://localhost:8080/

3. Просмотр данных

    a. curl http://localhost:8080/

    b. Просмотреть в браузере страницу
   ```
   http://127.0.0.1:5555
   ```