### Условие
Необходимо написать простой web-сервер для обработки GET и POST http
запросов средствами Python и библиотеки socket.

Задание: сделать сервер, который может:

● Принять и записать информацию о дисциплине и оценке по дисциплине.

● Отдать информацию обо всех оценах по дсициплине в виде html-страницы.

### Запуск 

Для запуска сервера ``` python server.py 127.0.0.1 8080 MyServer ```

POST-запрос на добавление дисциплины и оценки по ней ``` curl -X POST "http://localhost:8080/disciplines?discipline=Math&grade=4" -H "Host: MyServer" ```

GET-запрос на получение оценки по конкретной дисциплине ``` curl -X GET "http://localhost:8080/disciplines?discipline=Math" -H "Accept: text/html" -H "Host: MyServer" ```

GET-запрос на получение всех оценок по каждой дисциплине ``` curl -X GET "http://localhost:8080/disciplines?discipline=Math" -H "Accept: text/html" -H "Host: MyServer" ```

После GET-запросов в папке с файлом появляются html файлы, в которых содержится информация об оценках