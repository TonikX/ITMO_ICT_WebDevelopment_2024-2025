# Шаблоны и стилизация

## 🔹 Базовый шаблон `base.html`

Содержит навигационное меню и подключение Bootstrap:

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
  <div class="container">
    <a class="navbar-brand" href="{% url 'hotels:hotel_list' %}">🏨 Отели</a>
    <ul class="navbar-nav ms-auto">
      {% if user.is_authenticated %}
        <li class="nav-item">
          <a class="nav-link" href="{% url 'hotels:user_bookings' %}">Мои бронирования</a>
        </li>
        <li class="nav-item d-flex align-items-center">
          <span class="navbar-text text-light me-2">Привет, {{ user.username }}!</span>
          <form method="post" action="{% url 'logout' %}">
            {% csrf_token %}
            <button type="submit" class="btn btn-link nav-link">Выйти</button>
          </form>
        </li>
      {% else %}
        <li class="nav-item"><a class="nav-link" href="{% url 'login' %}">Войти</a></li>
        <li class="nav-item"><a class="nav-link" href="{% url 'hotels:register' %}">Регистрация</a></li>
      {% endif %}
    </ul>
  </div>
</nav>
```

## Стилизация заголовков

```html
.hotel-title {
    display: inline-block;
    background: rgba(255, 255, 255, 0.8);
    padding: 10px 25px;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    font-weight: bold;
    color: #333;
    font-size: 2rem;
}
```

## Фон главной страницы

```html
    body {
    background: url('https://avatars.mds.yandex.net/get-mpic/3741589/img_id5879705607728791950.jpeg/orig') no-repeat center center fixed;
    background-size: cover;
    background-attachment: fixed;
    min-height: 100vh;
}
```

## Модальное окно

```html
<div class="modal fade" id="editModal{{ booking.id }}" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать бронирование</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form method="post" action="{% url 'hotels:booking_edit' booking.id %}">
              {% csrf_token %}
              <div class="mb-3">
                <label for="check_in_{{ booking.id }}" class="form-label">Дата заезда</label>
                <input type="date" name="check_in" id="check_in_{{ booking.id }}" class="form-control"
                       value="{{ booking.check_in|date:'Y-m-d' }}">
              </div>
              <div class="mb-3">
                <label for="check_out_{{ booking.id }}" class="form-label">Дата выезда</label>
                <input type="date" name="check_out" id="check_out_{{ booking.id }}" class="form-control"
                       value="{{ booking.check_out|date:'Y-m-d' }}">
              </div>
              <div class="text-end">
                <button type="submit" class="btn btn-primary">💾 Сохранить</button>
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
```
