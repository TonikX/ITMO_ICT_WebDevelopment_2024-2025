from datetime import datetime
from models import Task, Category, Tag

# Временная база данных
tasks_db = []

# Пример данных
tasks_db.append(
    Task(
        id=1,
        description="Подготовить отчет",
        deadline=datetime(2025, 10, 15),
        priority=1,
        time_spent=120,
        category=Category(name="Работа", description="Задачи по работе"),
        tags=[Tag(name="срочно"), Tag(name="отчет")],
    )
)

tasks_db.append(
    Task(
        id=2,
        description="Купить продукты",
        deadline=datetime(2025, 10, 10),
        priority=2,
        time_spent=30,
        category=Category(name="Личное", description="Личные задачи"),
        tags=[Tag(name="покупки")],
    )
)