# Документация моделей для концертной площадки

## 1. Исполнитель (Performer)

```python
class Performer(models.Model):
    name = models.CharField(max_length=255)
    manager = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
```

**Описание:** Хранит информацию об исполнителях.
- `name` — Имя исполнителя.
- `manager` — Менеджер исполнителя.
- `email` — Контактный email.
- `phone` — Контактный телефон.

---

## 2. Концерт (Concert)

```python
class Concert(models.Model):
    STATUS_CHOICES = [
        ('held', 'Проведен'),
        ('cancelled', 'Отменен'),
        ('prepared', 'Подготовлен'),
        ('in_progress', 'В работе')
    ]

    image = models.ImageField(upload_to='concerts', default='concerts.jpg')
    title = models.CharField(max_length=255)
    description = models.TextField()
    performer = models.ForeignKey(Performer, on_delete=models.CASCADE, related_name="concerts")
    date = models.DateField()
    age_limit = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='in_progress')
```

**Описание:** Хранит информацию о концертах.
- `image` — Обложка концерта.
- `title` — Название концерта.
- `description` — Описание концерта.
- `performer` — Исполнитель.
- `date` — Дата проведения.
- `age_limit` — Возрастное ограничение.
- `status` — Статус концерта (`held`, `cancelled`, `prepared`, `in_progress`).

---

## 3. Оборудование (Equipment)

```python
class Equipment(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
```

**Описание:** Хранит список оборудования.
- `name` — Название оборудования.
- `quantity` — Количество.

---

## 4. Оборудование для концерта (ConcertEquipment)

```python
class ConcertEquipment(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name="equipment")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="concerts")
    quantity = models.PositiveIntegerField()
```

**Описание:** Связывает концерты с необходимым оборудованием.
- `concert` — Концерт.
- `equipment` — Оборудование.
- `quantity` — Количество оборудования.

---

## 5. Билет (Ticket)

```python
class Ticket(models.Model):
    concert = models.ForeignKey('Concert', on_delete=models.CASCADE, related_name='ticket_categories')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_quantity = models.PositiveIntegerField()
    sold_quantity = models.PositiveIntegerField(default=0)
```

**Описание:** Хранит информацию о билетах на концерт.
- `concert` — Концерт.
- `name` — Название категории билетов.
- `price` — Цена билета.
- `total_quantity` — Всего билетов.
- `sold_quantity` — Количество проданных билетов.

Методы:
- `available_quantity` — Возвращает количество доступных билетов.
- `sell_tickets(quantity)` — Продает указанное количество билетов.

---

## 6. Заказ (Order)

```python
class Order(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Подтверждено'),
        ('pending', 'В ожидании'),
        ('returned', 'Возврат'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
```

**Описание:** Хранит информацию о заказах билетов.
- `user` — Пользователь.
- `ticket` — Выбранный билет.
- `quantity` — Количество билетов.
- `date` — Дата создания заказа.
- `total_price` — Итоговая стоимость.
- `status` — Статус заказа (`confirmed`, `pending`, `returned`).

Методы:
- `save()` — Пересчитывает `total_price` перед сохранением.

---

## 7. Сотрудник (Employee)

```python
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="employee")
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
```

**Описание:** Хранит информацию о сотрудниках концертной площадки.
- `user` — Привязка к учетной записи.
- `name` — Имя сотрудника.
- `position` — Должность.
- `salary` — Зарплата.
- `phone` — Контактный телефон.
- `email` — Контактный email.

---

## 8. Организатор (Organizer)

```python
class Organizer(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="organized_concerts")
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name="organizers")
```

**Описание:** Связывает сотрудников-организаторов с концертами.
- `employee` — Организатор.
- `concert` — Концерт.

