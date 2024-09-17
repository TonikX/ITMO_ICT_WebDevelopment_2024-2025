### Задание:
Необходимо написать простой web-сервер для обработки GET и POST http
запросов
### Стек:
- ЯП: Java
- Пакет: net, util, io
- Протокол: HTTP
### Инструкция по запуску
Выполните команды в папке `Lr1\task_1\src\main\java\ru\barkhatnat`

1. Запуск сервера
	- `cd server`
	- `javac HttpServer.java`
	- `java HttpServer.java <ip> <port> <name>` (вы можете указать желаемый ip и порт, по умолчанию `localhost:1234 SimpleJavaHTTPServer`)
2.  POST метод
	- Укажите значения параметров в URI, например `localhost:1234/grades?discipline=math&grade=6`
3. GET метод
	- Воспользуйтесь URI `localhost:1234/grades`
