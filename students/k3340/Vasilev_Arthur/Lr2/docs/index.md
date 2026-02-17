# Лабораторная работа 2: Django приложение для автогонок

## Выбор лабораторной работы

<div class="lab-cards">
  <div class="lab-card">
    <h3>🔌 Лабораторная работа 1</h3>
    <p>Работа с сетевыми сокетами в Python</p>
    <a href="https://pppestto.github.io/lr1-sockets-report/" class="btn">Перейти →</a>
  </div>

  <div class="lab-card">
    <h3>🏎️ Лабораторная работа 2</h3>
    <p>Django приложение для автогонок</p>
    <p><strong>Текущая работа</strong></p>
  </div>

  <div class="lab-card">
    <h3>🎯 Лабораторная работа 3</h3>
    <p>Хакатон API</p>
    <a href="https://pppestto.github.io/lr3-hackathon-report/" class="btn">Перейти →</a>
  </div>
</div>

<style>
.lab-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin: 30px 0;
}

.lab-card {
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  background: #fafafa;
  transition: transform 0.2s, box-shadow 0.2s;
}

.lab-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.lab-card h3 {
  color: #4caf50;
  margin-bottom: 10px;
}

.lab-card p {
  margin: 10px 0;
  color: #666;
}

.btn {
  display: inline-block;
  background: #4caf50;
  color: white;
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 5px;
  margin-top: 10px;
  transition: background 0.2s;
}

.btn:hover {
  background: #45a049;
}
</style>

## Описание проекта

Веб-приложение для управления автогонками, разработанное с использованием Django 4.2 и PostgreSQL. Приложение позволяет управлять участниками автогонок, командами, автомобилями, гонками и комментариями.

## Основной функционал

### Для пользователей:
- **Регистрация и аутентификация**
- **Просмотр доступных гонок**
- **Регистрация на гонки**
- **Управление своими регистрациями** (редактирование, удаление)
- **Написание отзывов и комментариев** к гонкам
- **Просмотр результатов гонок**

### Для администраторов:
- **Управление гонками** (создание, редактирование)
- **Установка времени и результатов заездов**
- **Управление пользователями и командами**
- **Модерация комментариев**

## Архитектура приложения

### Модели данных

- **User** - Расширенная модель пользователя с уровнем опыта и классом гонщика
- **Team** - Команды участников
- **Car** - Автомобили участников
- **Race** - Гонки с датой, местом проведения
- **RaceRegistration** - Регистрации участников на гонки
- **Comment** - Комментарии и отзывы к гонкам

### Структура проекта

```
racing_project/
├── racing_app/
│   ├── models.py          # Модели данных
│   ├── views.py           # Представления
│   ├── urls.py            # Маршруты
│   ├── forms.py           # Формы
│   ├── admin.py           # Админка
│   └── templates/         # Шаблоны
├── manage.py
├── requirements.txt       # Зависимости
└── settings.py           # Настройки
```

## Технологии

- **Backend:** Django 4.2.7
- **База данных:** PostgreSQL
- **Frontend:** HTML, CSS, Bootstrap (в шаблонах)
- **Аутентификация:** Django Auth
- **Админка:** Django Admin

## Установка и запуск

Подробная инструкция по установке находится в разделе [Установка](installation.md).