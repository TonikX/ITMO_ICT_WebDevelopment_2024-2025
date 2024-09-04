# ITMO_ICT_WebDevelopment_2024-2025
Репозиторий для реализации дистанционного обучения по дисциплине "Web-программирование".

[Учебный журнал](https://docs.google.com/spreadsheets/d/1QYiKw_NWfZw6G1vodMN73pRoM7P9aVxmGQRUw8-90tc/edit?usp=sharing) по дисциплине. Тут доступна информация о сроках сдачи работ, о текущей успеваемости студентов и описаны все материалы необходимые для реализации курса.

Составляющие финальной оценки:
- 70 баллов - лабы (их делать обязательно). В курсе всего 4 работы.
- 10 баллов - тесты.
- 10 баллов - дисскусии на практиках (1+ доклад за семестр). Доклад на 5-7 минут. Нужны примеры кода или модели процессов, которые ведется речь в докладе.
- 10 - экзамен.

При выполнении всех лаб по дисциплине в срок + две недели - экзамен-автомат.

Все лабы необходимо сдать до **20 декабря**, иначе есть риск, что преподаватель не успеет их проверить.

Если лабораторная работа выполнена не в срок, требуется получить допуск к ее защите. Для допуска необходимо выполнть задания на https://leetcode.com/. 1 неделя просрочки - 1 задание.

Преподавателю можно писать в телеграмме, при возможности он ответит (преподаватель не обязан отвечать в месенджерах во внеурочное врем). Лучше прийти на пару и спросить лично.

## Инструкции к использованию полезных материалов
Дополнительные материалы делятся на 3 категории:

1. Для тех, кто считает, что имеет недостаточно базовых знаний об информатике, веб-разработке и сетях (обзначается **(+)**).
2. Для тех, кто считает, что имеет базовые знания  (обзначается **(++)**).
3. Для тех, кто хочет поглубже изучить материал  (обзначается **(+++)**).

### Лекция 1.1 - Концепции разработки веб сервисов.
Презентация с лекции [тут](https://drive.google.com/file/d/1uZMyzGn_42krfuEdR-pLmcrb2LGqYNmx/view?usp=sharing).

Допонительные материалы:

1. [Иерархия компьютерных информационных систем для разработки сайта](https://habr.com/ru/post/513486/) **(+)**
2. [Топ-5 наиболее популярных CMS: какую выбрать?](https://habr.com/ru/post/151879/) **(++)**
3. [Веб-фреймворки: введение для новичков (классификация фреймворков)](https://tproger.ru/translations/web-frameworks-how-to-get-started/) **(++)**
4. [Чем отличаются фронтенд- и бэкенд-разработка](https://techrocks.ru/2020/07/01/front-end-vs-back-end-development/) **(+)**
5. [Что такое MVC: базовые концепции и пример приложения](https://skillbox.ru/media/code/chto_takoe_mvc_bazovye_kontseptsii_i_primer_prilozheniya/) **(++)**

# Лабораторная работа 1. Работа с сокетами.

Важное сообщение для тех, кому "препод опять втирает какую-то ненужную лабу непонятно про что". Эта лабораторная работа и заданя в ней помогут Вам понять, как происходит сетевое взаимодействие в вебе, и не только. Сокеты используеются всегда, при любом сетевой взаимодействии. Если Вы будете веб-разработчиком, Вам придется работать с средствами, которые их используют (100%) и настраивать их в ручную (очень вероятно).

[Лекция с практики](https://docs.google.com/presentation/d/1w1CxQJ8w6kxJ54H-ouiNOucqRlpPFcXW/edit?usp=sharing&ouid=112464767591249503382&rtpof=true&sd=true)<br>
[Текст работы](https://drive.google.com/file/d/1p5FUB09uZlniENeAmPSuXjYvI-G7bCGy/view?usp=sharing)

**Общий** срок сдачи: **30.10.2024** (включительно) (необходимо отправить pull-реквест с работой). Вес работы в баллах – 12,5. Выполнение пунктов 1-5 - 100%. После срока сдачи максимальный бал 6.

## Сдача работы №1

Полученную модель, код и отчет залить в папку репозитория **students/группа/laboratory_works/фамилия_имя/laboratory_work_1**. Инструкция о загрузке работы ниже. Не забывайте о файле gitignor.

На git должен быть загружен pdf-файл с отчетом, код программамы, **где каждая папка соотвествует части работы (task_1, task_2...)**.

Шаблон имени файла отчета: **Фамилия_Имя_группа_№лабы**. Отчет должен содержать титульный лист, листинг кода по каждому пункту с комментариями, скрины работы программ.

Как делать пул-реквест описано в разделе **[Сдача работ](https://github.com/TonikX/ITMO_ICT_WebDevelopment_2024-2025/blob/master/README.md#%D1%81%D0%B4%D0%B0%D1%87%D0%B0-%D1%80%D0%B0%D0%B1%D0%BE%D1%82)**

#### Дополнительный контент к первой лабе
Те студенты, которые хотят получить более обширное представление о работе с конструкторами сайтов, могут пройти [этот курс](https://geekbrains.ru/courses/74).


## Сдача работ

Все отчеты делаются средствами markdown и mkdocs. Инструкция по созданию веб-страничек из markdown средствами mkdocs доступна тут в пункте 3.2.2 https://docs.google.com/document/d/1rIfREFvCB4pp8uF990Tz3PLXRJ5u_w-Y3vLxfXWKoxg/edit?usp=sharing . Краткое описание работы с markdown доступно в пункте 3.1

Все отчеты должны храниться на одном "сайте", сгенерированном из ваших markdown файлов в форке этого репозитория.

Весь студенческий код необходимо загрузить в папку **Students**
Для загрузки работы необходимо:

1. Зарегистрироваться на Git.
2. Сделать форк репозитория с заданиями в свой аккаунт (на странице https://github.com/TonikX/ITMO_ICT_WebDevelopment_2023-2024 кнопка fork справа, сверху).
3. Установить Git на компьютер.
4. Открыть папку, где хранятся Ваши проекты. В контекстом меню нажать "Open Git Bash here". Склонировать форкнутый репозиторий на комьютер (git clone https://github.com/ваш аккаунт/ITMO_ICT_WebDevelopment_2023-2024).
5. В файловой системе Вашего компрьютера в склонированном репозитории создать в папке students/группа Вашу личную папку в формате Фамилия_Имя латиницей (Пример **students/k3340/Petrov_Vasya**).
6. В личной папке сделать подпапку с текущей работой в формате lr_номер (Пример **students/k3340/Petrov_Vasya/Lr1**).
7. Записать в папку отчетные материалы.
8. Сделать коммит, описать его адекватно (Пример "был добавлен файл перезентация_петров.pdf"). Набрать команлы git add и git commit -m "название комита".
9. Сделать push в Ваш форкнутый репозиторий (git push).
