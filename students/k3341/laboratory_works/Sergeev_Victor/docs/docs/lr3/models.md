# Модели сущностей

## Genre

Модель жанра

* title: varchar(50) - название жанра

## Author

Модель автора

* full_name: varchar(120) - ФИО автора

## Book

Модель оригинала книги

* title: varchar(150) - название книги
* publisher: varchar(50) - издательство
* genre: many_to_many(Genre, throught=BookGenre) - жанры книги
* author: many_to_many(Author, throught=BookAuthor) - авторы книги

## BookGenre

Модель жанра конкретной книги

* book: foreign_key(Book) - книга
* genre: foreign_key(Genre) - жанр

## BookAuthor

Модель автора книги

* book: foreign_key(Book) - книга
* author: foreign_key(Author) - автор

## BookCopy

Модель копии книги

* book: foreign_key(Book) - оригинал книги
* cipher: varchar(10) - шифр копии книги
* publish_year: positiveInteger(min=1000, max=2097, default=today.year) - год публикации копии

## ReadingRoom

Модель читального зала

* name: varchar(30) - название зала
* capacity: integer - вместимость

## Reader

Модель читателя

* full_name: varchar(120) - ФИО читателя
* passport_number: varchar(16) - номер пасспорта
* birthdate: date - дата рождения
* address: varchar(100) - адрес читателя
* phone_number: varchar(20) - номер телефон
* education: varchar(1), choice=[начальное, среднее, высшее] - образование читателя
* degree: boolean(default=False) - наличие учёной степени
* registration_date: date(default=today) - дата регистрации читателя
* reading_ticket_number: varchar(10) - номер читательского билета
* reading_room: foreign_key(ReadingRoom) - читальный зал читателя

## BookTake

Модель взятия книги

* book_copy: foreign_key(BookCopy) - взятая копия книги
* reader: foreign_key(Reader) - читатель
* take_date: date(default=today) - дата взятия
* restore_date: date(default=None) - дата возврата
