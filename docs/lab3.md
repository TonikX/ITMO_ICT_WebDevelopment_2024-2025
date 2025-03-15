# Лабораторная работа 3
 Была реализована база данных для книжного магазина. Далее представлены модели, методы, описания и метаданные.

## Модели данных
# Модель Employee (Сотрудник)
# Описание:

Хранит информацию о сотрудниках компании, включая их роль в типографии.

# Поля:

first_name (CharField, max_length=50): Имя сотрудника.
last_name (CharField, max_length=50): Фамилия сотрудника.
role (CharField, max_length=20, choices=Role.choices): Роль сотрудника (Менеджер, Редактор, Другое).
email (EmailField, unique=True): Электронная почта сотрудника.
phone_number (CharField, max_length=20, blank=True): Номер телефона.
address (CharField, max_length=255, blank=True): Адрес.
# Метаданные:

verbose_name: "Employee"
verbose_name_plural: "Employees"
# Методы:

__str__(): Возвращает полное имя сотрудника.
Модель Author (Автор)
# Описание:

Хранит информацию об авторах книг.

# Поля:

first_name (CharField, max_length=50): Имя автора.
last_name (CharField, max_length=50): Фамилия автора.
biography (TextField, blank=True): Биография автора.
email (EmailField, unique=True, blank=True, null=True): Электронная почта.
phone_number (CharField, max_length=20, blank=True): Номер телефона.
# Метаданные:

verbose_name: "Author"
verbose_name_plural: "Authors"
# Методы:

__str__(): Возвращает полное имя автора.
Модель Book (Книга)
# Описание:

Хранит информацию о книгах.

# Поля:

title (CharField, max_length=200): Название книги.
authors (ManyToManyField к Author через BookAuthor): Авторы книги.
# Метаданные:

verbose_name: "Book"
verbose_name_plural: "Books"
# Методы:

__str__(): Возвращает название книги.
Модель BookAuthor (Автор книги)
# Описание:

Промежуточная модель для связи многих ко многим между Book и Author с дополнительными полями.

# Поля:

book (ForeignKey к Book): Ссылка на книгу.
author (ForeignKey к Author): Ссылка на автора.
order (PositiveIntegerField): Порядок автора на обложке (влияет на размер гонорара).
royalty_percentage (DecimalField, max_digits=5, decimal_places=2): Процент гонорара.
# Метаданные:

unique_together: ('book', 'author')
ordering: ['order']
verbose_name: "Book Author"
verbose_name_plural: "Book Authors"
# Методы:

__str__(): Возвращает информацию об авторе и книге с указанием порядка на обложке.
Модель Edition (Издание)
# Описание:

Хранит информацию об изданиях книг.

# Поля:

book (ForeignKey к Book): Ссылка на книгу.
edition_number (PositiveIntegerField): Номер издания.
publication_date (DateField): Дата публикации.
number_of_pages (PositiveIntegerField): Количество страниц.
has_illustrations (BooleanField, default=False): Наличие иллюстраций.
editors (ManyToManyField к Employee через EditionEditor): Редакторы издания.
# Метаданные:

unique_together: ('book', 'edition_number')
verbose_name: "Edition"
verbose_name_plural: "Editions"
# Методы:

__str__(): Возвращает название книги и номер издания.
Модель Contract (Контракт)
# Описание:

Хранит информацию о контрактах на издание книг.

# Поля:

edition (OneToOneField к Edition): Ссылка на издание.
manager (ForeignKey к Employee): Менеджер, подписавший контракт.
date_signed (DateField): Дата подписания контракта.
# Метаданные:

verbose_name: "Contract"
verbose_name_plural: "Contracts"
# Методы:

__str__(): Возвращает информацию о контракте и издании.
Модель EditionEditor (Редактор издания)
# Описание:

Промежуточная модель для связи многих ко многим между Edition и Employee с дополнительными полями.

# Поля:

edition (ForeignKey к Edition): Ссылка на издание.
editor (ForeignKey к Employee): Ссылка на редактора.
is_responsible_editor (BooleanField, default=False): Является ли ответственным редактором.
# Метаданные:

unique_together: ('edition', 'editor')
verbose_name: "Edition Editor"
verbose_name_plural: "Edition Editors"
# Методы:

__str__(): Возвращает информацию о редакторе и издании с указанием роли.
Модель Customer (Заказчик)
# Описание:

Хранит информацию о заказчиках.

# Поля:

name (CharField, max_length=100): Наименование заказчика.
email (EmailField, unique=True): Электронная почта.
phone_number (CharField, max_length=20, blank=True): Номер телефона.
address (CharField, max_length=255, blank=True): Адрес.
# Метаданные:

verbose_name: "Customer"
verbose_name_plural: "Customers"
# Методы:

__str__(): Возвращает наименование заказчика.
Модель Order (Заказ)
# Описание:

Хранит информацию о заказах на покупку книг.

# Поля:

customer (ForeignKey к Customer): Ссылка на заказчика.
date_ordered (DateField): Дата заказа.
items (ManyToManyField к Edition через OrderItem): Позиции заказа.
# Метаданные:

verbose_name: "Order"
verbose_name_plural: "Orders"
# Методы:

__str__(): Возвращает идентификатор заказа и имя заказчика.
Модель OrderItem (Позиция заказа)
# Описание:

Промежуточная модель для связи многих ко многим между Order и Edition с дополнительным полем количества.

# Поля:

order (ForeignKey к Order): Ссылка на заказ.
edition (ForeignKey к Edition): Ссылка на издание.
quantity (PositiveIntegerField, default=1): Количество единиц товара.
# Метаданные:

unique_together: ('order', 'edition')
verbose_name: "Order Item"
verbose_name_plural: "Order Items"
# Методы:

__str__(): Возвращает количество и информацию об издании в заказе.
Соответствие требованиям задания
Каждая книга издаётся в рамках контракта:
Модель Contract связывает издание (Edition) с менеджером и датой подписания.

Книга может быть написана несколькими авторами:

Связь ManyToManyField между Book и Author через BookAuthor.

Контракт подписывается одним менеджером и всеми авторами книги:

Модель Contract связывает менеджера и издание; авторы связаны через BookAuthor.

Каждый автор может написать несколько книг (по разным контрактам):

Авторы могут быть связаны с несколькими книгами через BookAuthor.

Порядок, в котором авторы указаны на обложке, влияет на размер гонорара:

Поля order и royalty_percentage в модели BookAuthor отражают порядок и гонорар.

Если сотрудник является редактором, то он может работать одновременно над несколькими книгами:

Связь ManyToManyField между Edition и Employee через EditionEditor позволяет редакторам работать над несколькими изданиями.

У каждой книги может быть несколько редакторов, один из них — ответственный редактор:

Поле is_responsible_editor в модели EditionEditor отмечает ответственного редактора.

Каждый заказ оформляется на одного заказчика; в заказе может быть перечислено несколько книг:

Модель Order связывает заказчика и заказанные издания через OrderItem.
Запросы и отчёты
Список всех изданных книг заданного автора:
Фильтрация модели Book по связанным авторам.

Список ответственных редакторов для всех изданий:

Выборка из EditionEditor с is_responsible_editor=True.

Количество редакторов каждой книги:

Агрегирование по изданию в EditionEditor для подсчёта редакторов.

Количество контрактов за каждый месяц за истекший год:

Группировка по месяцу поля date_signed в Contract.

Список всех менеджеров, которые имеют максимальное количество контрактов за определённый период:

Агрегирование и фильтрация модели Contract по менеджерам и заданному периоду.

Отчёт о всех контрактах за каждый месяц истекшего квартала с указанием для каждого контракта наименования книги, количества авторов и редакторов, количества страниц, наличие иллюстраций; указать количество изданий за каждый месяц и общее количество за квартал:

Комплексный запрос, объединяющий данные из моделей Contract, Edition, Book, BookAuthor, EditionEditor.


---

[Назад к главной странице](index.md)
