Задание:
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

для GET-запроса:
```
curl curl http://localhost:8080/grades
```
для POST-запроса:
```
curl -d "discipline=Physics&grade=5A" -X POST http://127.0.0.1:8080/
```