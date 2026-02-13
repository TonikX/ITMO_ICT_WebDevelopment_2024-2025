# Все API Endpoints

## Базовый URL

```
http://127.0.0.1:8000/api/v1/
```

---

## Авторизация

### Регистрация

**POST** `/users/`

**Body:**
```json
{
  "username": "newuser",
  "password": "securepass123",
  "email": "user@example.com"
}
```

**Response:** `201 Created`

---

### Получение токена

**POST** `/token/login/`

**Body:**
```json
{
  "username": "admin",
  "password": "yourpassword"
}
```

**Response:**
```json
{
  "auth_token": "e66aef423337ec0a48f7e7562fc94cd4743f7501"
}
```

---

### Информация о пользователе

**GET** `/users/me/`

**Headers:**
```
Authorization: Token <your_token>
```

**Response:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@hotel.com"
}
```

---

### Выход

**POST** `/token/logout/`

**Headers:**
```
Authorization: Token <your_token>
```

**Response:** `204 No Content`

---

## Номера

### Список номеров

**GET** `/rooms/`

**Query параметры:**
- `type` — фильтр по типу (single, double, triple)
- `floor` — фильтр по этажу

**Примеры:**
```
GET /api/v1/rooms/
GET /api/v1/rooms/?floor=2
GET /api/v1/rooms/?type=double&floor=3
```

**Response:**
```json
[
  {
    "id": 1,
    "number": 101,
    "type": "single",
    "floor": 1,
    "phone": "101",
    "price_per_day": "2500.00"
  },
  {
    "id": 2,
    "number": 201,
    "type": "double",
    "floor": 2,
    "phone": "201",
    "price_per_day": "4000.00"
  }
]
```

---

### Создание номера

**POST** `/rooms/`

**Headers:**
```
Authorization: Token <your_token>
Content-Type: application/json
```

**Body:**
```json
{
  "number": 301,
  "type": "triple",
  "floor": 3,
  "phone": "301",
  "price_per_day": 5000
}
```

**Response:** `201 Created`

---

### Получение номера

**GET** `/rooms/{id}/`

**Response:**
```json
{
  "id": 1,
  "number": 101,
  "type": "single",
  "floor": 1,
  "phone": "101",
  "price_per_day": "2500.00"
}
```

---

### Обновление номера

**PUT** `/rooms/{id}/`

**Body:**
```json
{
  "number": 101,
  "type": "single",
  "floor": 1,
  "phone": "101",
  "price_per_day": 2800
}
```

**PATCH** `/rooms/{id}/` — частичное обновление

**Body:**
```json
{
  "price_per_day": 2800
}
```

---

### Удаление номера

**DELETE** `/rooms/{id}/`

**Response:** `204 No Content`

---

## Клиенты

### Список клиентов

**GET** `/clients/`

**Query параметры:**
- `city` — фильтр по городу

**Примеры:**
```
GET /api/v1/clients/
GET /api/v1/clients/?city=Москва
```

**Response:**
```json
[
  {
    "id": 1,
    "passport": "1234567890",
    "last_name": "Иванов",
    "first_name": "Иван",
    "patronymic": "Иванович",
    "city": "Москва"
  }
]
```

---

### Создание клиента

**POST** `/clients/`

**Body:**
```json
{
  "passport": "9876543210",
  "last_name": "Петров",
  "first_name": "Петр",
  "patronymic": "Петрович",
  "city": "Санкт-Петербург"
}
```

**Response:** `201 Created`

---

### Получение клиента

**GET** `/clients/{id}/`

**Response:**
```json
{
  "id": 1,
  "passport": "1234567890",
  "last_name": "Иванов",
  "first_name": "Иван",
  "patronymic": "Иванович",
  "city": "Москва"
}
```

---

### Обновление клиента

**PUT** `/clients/{id}/`

**Body:**
```json
{
  "passport": "1234567890",
  "last_name": "Иванов",
  "first_name": "Иван",
  "patronymic": "Иванович",
  "city": "Казань"
}
```

**PATCH** `/clients/{id}/` — частичное обновление

---

### Удаление клиента

**DELETE** `/clients/{id}/`

**Response:** `204 No Content`

---

## Проживания

### Список проживаний

**GET** `/stays/`

**Response:**
```json
[
  {
    "id": 1,
    "client": 1,
    "room": 2,
    "check_in": "2026-01-20",
    "check_out": "2026-01-25"
  }
]
```

---

### Создание проживания

**POST** `/stays/`

**Body:**
```json
{
  "client": 1,
  "room": 2,
  "check_in": "2026-01-26",
  "check_out": "2026-01-30"
}
```

**Response:** `201 Created`

---

### Получение проживания

**GET** `/stays/{id}/`

---

### Обновление проживания

**PUT** `/stays/{id}/`

**PATCH** `/stays/{id}/`

---

### Удаление проживания

**DELETE** `/stays/{id}/`

**Response:** `204 No Content`

---

## Персонал

### Список персонала

**GET** `/staff/`

**Response:**
```json
[
  {
    "id": 1,
    "last_name": "Петров",
    "first_name": "Петр",
    "patronymic": "Петрович"
  }
]
```

---

### Создание служащего

**POST** `/staff/`

**Body:**
```json
{
  "last_name": "Сидоров",
  "first_name": "Сергей",
  "patronymic": "Сергеевич"
}
```

---

### Получение служащего

**GET** `/staff/{id}/`

---

### Обновление служащего

**PUT** `/staff/{id}/`

**PATCH** `/staff/{id}/`

---

### Удаление служащего

**DELETE** `/staff/{id}/`

---

## Расписание уборки

### Список расписаний

**GET** `/schedules/`

**Query параметры:**
- `floor` — фильтр по этажу
- `day` — фильтр по дню недели

**Примеры:**
```
GET /api/v1/schedules/
GET /api/v1/schedules/?floor=2
GET /api/v1/schedules/?day=mon
```

**Response:**
```json
[
  {
    "id": 1,
    "staff": 1,
    "floor": 2,
    "day": "mon"
  }
]
```

---

### Создание расписания

**POST** `/schedules/`

**Body:**
```json
{
  "staff": 1,
  "floor": 2,
  "day": "mon"
}
```

**Дни недели:**
- `mon` — понедельник
- `tue` — вторник
- `wed` — среда
- `thu` — четверг
- `fri` — пятница
- `sat` — суббота
- `sun` — воскресенье

---

## Кастомные запросы

### Свободные номера

**GET** `/queries/free-rooms/`

Возвращает количество свободных номеров на текущую дату.

**Response:**
```json
{
  "free_rooms": 5
}
```

---

### Клиенты из города

**GET** `/queries/clients-from-city/`

**Query параметры:**
- `city` (обязательный) — название города

**Пример:**
```
GET /api/v1/queries/clients-from-city/?city=Москва
```

**Response:**
```json
{
  "city": "Москва",
  "count": 12
}
```

---

### Клиенты в номере за период

**GET** `/queries/clients-in-room/`

**Query параметры:**
- `room_number` (обязательный) — номер комнаты
- `start_date` (обязательный) — дата начала (YYYY-MM-DD)
- `end_date` (обязательный) — дата окончания (YYYY-MM-DD)

**Пример:**
```
GET /api/v1/queries/clients-in-room/?room_number=101&start_date=2026-01-01&end_date=2026-01-31
```

**Response:**
```json
[
  {
    "id": 1,
    "client": {
      "id": 1,
      "passport": "1234567890",
      "last_name": "Иванов",
      "first_name": "Иван",
      "patronymic": "Иванович",
      "city": "Москва"
    },
    "room": {
      "id": 1,
      "number": 101,
      "type": "single",
      "floor": 1,
      "phone": "101",
      "price_per_day": "2500.00"
    },
    "check_in": "2026-01-15",
    "check_out": "2026-01-20"
  }
]
```

---

### Служащие убирали номер

**GET** `/queries/staff-for-client/`

**Query параметры:**
- `passport` (обязательный) — номер паспорта клиента
- `day` (обязательный) — день недели (mon, tue, wed, thu, fri, sat, sun)

**Пример:**
```
GET /api/v1/queries/staff-for-client/?passport=1234567890&day=mon
```

**Response:**
```json
[
  {
    "id": 1,
    "staff": {
      "id": 1,
      "last_name": "Петров",
      "first_name": "Петр",
      "patronymic": "Петрович"
    },
    "floor": 1,
    "day": "mon"
  }
]
```

---

## Отчеты

### Квартальный отчет

**GET** `/report/quarter/{quarter}/`

**URL параметры:**
- `quarter` — номер квартала (1, 2, 3, 4)

**Примеры:**
```
GET /api/v1/report/quarter/1/
GET /api/v1/report/quarter/2/
```

**Response:**
```json
{
  "quarter": 1,
  "year": 2026,
  "period": "2026-01-01 - 2026-03-31",
  "clients_per_room": [
    {
      "room__number": 101,
      "client_count": 5
    },
    {
      "room__number": 201,
      "client_count": 3
    }
  ],
  "rooms_per_floor": [
    {
      "floor": 1,
      "room_count": 3
    },
    {
      "floor": 2,
      "room_count": 2
    }
  ],
  "income_per_room": {
    "101": 50000,
    "201": 45000
  },
  "total_income": 95000
}
```

**Описание полей:**
- `clients_per_room` — количество уникальных клиентов по каждому номеру
- `rooms_per_floor` — распределение номеров по этажам
- `income_per_room` — доход по каждому номеру за квартал
- `total_income` — суммарный доход по всей гостинице

---

## Коды ответов

- `200 OK` — успешный запрос
- `201 Created` — объект создан
- `204 No Content` — успешное удаление
- `400 Bad Request` — некорректные параметры
- `401 Unauthorized` — требуется авторизация
- `404 Not Found` — объект не найден
- `500 Internal Server Error` — ошибка сервера
