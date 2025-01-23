# Админ-панель концертной площадки

## Исполнители (Performer)

- Фильтрация по менеджеру исполнителя.
- Поиск по имени исполнителя, имени менеджера и электронной почте.
- Сортировка исполнителей по имени.

```python
@admin.register(Performer)
class PerformerAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'email', 'phone')
    search_fields = ('name', 'manager', 'email')
    list_filter = ('manager',)
    ordering = ('name',)
```

## Концерты (Concert)

- Фильтрация концертов по статусу, дате проведения и исполнителю.
- Поиск по названию концерта и имени исполнителя.
- Сортировка концертов по дате.

```python
@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ('title', 'performer', 'date', 'status', 'age_limit')
    search_fields = ('title', 'performer__name')
    list_filter = ('status', 'date', 'performer')
    ordering = ('date',)
```

## Оборудование (Equipment)

- Фильтрация оборудования по названию.
- Поиск по названию оборудования.
- Сортировка оборудования по имени.

```python
@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
```

## Оборудование для концерта (ConcertEquipment)

- Фильтрация по концерту и оборудованию.
- Поиск по названию концерта и оборудования.
- Сортировка по названию концерта.

```python
@admin.register(ConcertEquipment)
class ConcertEquipmentAdmin(admin.ModelAdmin):
    list_display = ('concert', 'equipment', 'quantity')
    search_fields = ('concert__title', 'equipment__name')
    list_filter = ('concert', 'equipment')
    ordering = ('concert',)
```

## Билеты (Ticket)

- Фильтрация билетов по концерту и цене.
- Поиск по названию билета и названию концерта.
- Сортировка билетов по концерту и цене.

```python
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'concert', 'price', 'total_quantity', 'sold_quantity', 'available_quantity')
    search_fields = ('name', 'concert__title')
    list_filter = ('concert', 'price')
    ordering = ('concert', 'price')
```

## Заказы (Order)

- Фильтрация заказов по статусу и дате создания.
- Поиск по имени пользователя, названию билета и статусу заказа.
- Сортировка заказов по дате.

```python
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'ticket', 'quantity', 'date', 'total_price', 'status')
    search_fields = ('user__username', 'ticket__name', 'status')
    list_filter = ('status', 'date')
    ordering = ('date',)
```

## Сотрудники (Employee)

- Фильтрация сотрудников по должности.
- Поиск по имени и должности.
- Сортировка сотрудников по имени.

```python
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'salary', 'phone', 'email')
    search_fields = ('name', 'position')
    list_filter = ('position',)
    ordering = ('name',)
```

## Организаторы (Organizer)

- Фильтрация по концерту.
- Поиск по имени организатора и названию концерта.
- Сортировка по названию концерта.

```python
@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('employee', 'concert')
    search_fields = ('employee__name', 'concert__title')
    list_filter = ('concert',)
    ordering = ('concert',)
```

