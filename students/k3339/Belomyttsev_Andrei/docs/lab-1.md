# Lab-1

You can choose specific IP address and port by changing `IP` and `PORT` variables.

## Task 1

**UDP client and server**

Firstly run `python 1-server.py`

Then run `python 1-client.py`

You'll see messages in both consoles: "*Hello, server*" and "*Hello, client*".

## Task 2

**Parallelogram area calculator**

Firstly run `python 2-server.py`

Then run `python 2-client.py`

Enter numbers into client's console: a, h or a, b, alpha (without commas, space as separator, alpha in degrees).

You'll see the result.

```
Parallelogram Area Calculator
Enter a, h or a, b, alpha: 10 20
Result: 200.0

Parallelogram Area Calculator
Enter a, h or a, b, alpha: 10 20 30
Result: 99.99999999999999
```

## Task 3

**HTTP server**

In order to connect to the server enter `127.0.0.1:PORT` into your browser's URL field.

You'll see `index.html` web page.

## Task 4

**TCP multiplayer chat**

Firstly run `python 4-server.py`

Then run multiple `python 4-client.py`

Enter name on client. Then you will be able to send and receive messages.

Server:
```
Chat started...
('127.0.0.1', 52188) connected
Name is Andrei
('127.0.0.1', 52195) connected
Name is Alice
('127.0.0.1', 52499) connected
Name is Dima
```

Client 1:
```
Enter name: Andrei
Andrei joined the chat.
Alice joined the chat.
Dima joined the chat.
Hello!
Andrei: Hello!
Alice: Hi!
Dima: Hello World!
```

Client 2:
```
Enter name: Alice 
Alice joined the chat.
Dima joined the chat.
Andrei: Hello!
Hi!   
Alice: Hi!
Dima: Hello World!
```

Client 3:
```
Enter name: Dima 
Dima joined the chat.
Andrei: Hello!
Alice: Hi!
Hello World!
Dima: Hello World!
```

## Task 5

**HTTP server with GET and POST methods**

In order to connect to the server enter `127.0.0.1:PORT` into your browser's URL field.

You'll see web page with table of subjects and marks, and form for adding new subject and mark or changing existing. To edit the table enter *Subject* and *Mark*, then click *Submit*.

Subjects and marks are stored in `marks.json`.

Used classless CSS to make website prettier.

You can choose CSS by uncommenting specific line.

```python
# content += '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@exampledev/new.css@1/new.min.css">'
# content += '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.min.css">'
# content += '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/dark.min.css">'
content += '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/light.min.css">'
```

I recommend [new.css](https://github.com/xz/new.css) or [water.css](https://github.com/kognise/water.css)

[More classless CSS](https://github.com/dbohdan/classless-css)