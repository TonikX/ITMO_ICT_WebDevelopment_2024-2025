# Практика 3.1 — ORM-запросы, related_name, M2M

Эта страница — «дока» по практике к ЛР (по просьбе преподавателя), с акцентом на:
- что такое `related_name`
- как делать запросы через `related_name`
- как работают связи **many-to-many** в Django
- примеры агрегаций (Count/Avg)

---

## 1) Что такое related_name
`related_name` задаёт имя обратной связи.

Пример из проекта:
```python
# TeamMember.team = ForeignKey(Team, related_name="members")
team = Team.objects.get(id=1)
members = team.members.all()  # обратная связь через related_name="members"
```

Если `related_name` не указать, Django создаст имя по умолчанию вроде `teammember_set`.

---

## 2) One-to-One: пользователь → профиль
В проекте:
```python
# UserProfile.user = OneToOneField(User, related_name="profile")
user = User.objects.get(username="cap1")
role = user.profile.role
```

---

## 3) One-to-Many: задача → ссылки/файлы
В проекте:
```python
# TaskResourceLink.task = ForeignKey(Task, related_name="resource_links")
task = Task.objects.get(id=1)
links = task.resource_links.all()
files = task.resource_files.all()
```

---

## 4) Many-to-Many: задача → теги
В проекте:
```python
# Task.tags = ManyToManyField(Tag, related_name="tasks")
task = Task.objects.get(id=1)

# Получить все теги задачи
tags = task.tags.all()

# Добавить теги
tag1 = Tag.objects.create(name="Django")
tag2 = Tag.objects.create(name="PostgreSQL")
task.tags.add(tag1, tag2)

# Установить точный список тегов
task.tags.set([tag1.id, tag2.id])

# Найти все задачи по тегу (обратная связь через Tag.tasks)
django_tag = Tag.objects.get(name="Django")
tasks = django_tag.tasks.all()
```

---

## 5) Примеры сложных запросов с related_name

### 5.1. Все решения по задаче (Task -> solutions)
```python
task = Task.objects.get(id=1)
solutions = task.solutions.all()  # related_name="solutions" в модели Solution.task
```

### 5.2. Все оценки по решению (Solution -> evaluations)
```python
solution = Solution.objects.get(id=1)
evaluations = solution.evaluations.all()  # related_name="evaluations"
```

---

## 6) Агрегации / аналитика (Count, Avg)

### 6.1. Сколько команд выбрали каждую задачу
```python
from django.db.models import Count
Task.objects.annotate(teams_count=Count("teams")).values("id", "title", "teams_count")
```

### 6.2. Средний балл по каждому решению
```python
from django.db.models import Avg
Solution.objects.annotate(avg_score=Avg("evaluations__score")).values("id", "title", "avg_score")
```

### 6.3. Активность жюри (сколько оценок поставил)
```python
User.objects.filter(profile__role="JURY").annotate(
    eval_count=Count("evaluations_given"),
    avg_given=Avg("evaluations_given__score"),
).values("username", "eval_count", "avg_given")
```

---

## 7) Проверка вложенных объектов в API (что показать преподавателю)

### 7.1. 1-to-many вложенность
`GET /api/tasks/{id}/` вернёт:
- `resource_links` (список ссылок)
- `resource_files` (список файлов)

### 7.2. many-to-many вложенность
`GET /api/tasks/{id}/` вернёт:
- `tags` (список тегов)

### 7.3. 1-to-many для команды
`GET /api/teams/{id}/` вернёт:
- `members` (участники команды)

---

Если нужно — можно добавить ещё примеры запросов под ваш вариант (фильтрации, сортировки, prefetch_related/select_related).
