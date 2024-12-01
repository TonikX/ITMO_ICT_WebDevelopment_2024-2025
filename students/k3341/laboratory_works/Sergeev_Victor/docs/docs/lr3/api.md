# API

## CRUD Views

Для следующих моделей реализованы API CRUD запросы по соотвествующему пути:

* Genre - genre
* Author - author
* Book - book
* BookCopy - book_copy
* Reader - reader
* ReadingRoom - room
* BookTake - book_take

### ListView

```API
GET api/<model>/
```

### RetrieveView

```API
GET api/<model>/<int:pk>/
```

### UpdateView

```API
PATCH api/<model>/<int:pk>/

Request-body
{
    "model_field1": "value1",
    ...
}
```

### DeleteView

```API
DELETE api/<model>/<int:pk>/
```

### CreateView

```API
POST api/<model>/create/

Request-body
{
    "model_field1": "value1",
    ...
}
```

## Special Views

Какие книги закреплены за заданным читателем?

```API
GET reader/<int:pk>/book/
```

Кто из читателей взял книгу более месяца тому назад?

```API
GET reader/delay/month/
```

За кем из читателей закреплены книги, количество экземпляров которых в библиотеке не превышает 5?

```API
GET reader/less/5/
```

Сколько в библиотеке читателей младше 20 лет?

```API
GET reader/age/young/
```

Сколько читателей в процентном отношении имеют начальное образование, среднее, высшее, ученую степень?

```API
GET reader/education/stat/
```
