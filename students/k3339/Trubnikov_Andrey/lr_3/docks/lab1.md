# Личный финансовый сервис

Личный финансовый сервис — это приложение для управления личными финансами. Оно позволяет пользователям фиксировать доходы и расходы, устанавливать бюджеты для различных категорий, создавать финансовые цели и просматривать отчёты по своим транзакциям. Дополнительно сервис может уведомлять о превышении бюджета и помогать в анализе трат.

## Используемые технологии

Приложение построено на основе FastAPI, для работы с базой данных используется SQLAlchemy, управление миграциями осуществляется через Alembic. В качестве базы данных можно использовать PostgreSQL или SQLite. Аутентификация реализована с помощью JWT (PyJWT + Passlib).

## Структура проекта
```text
app/
├── models/
│   ├── user.py
│   ├── transaction.py
│   ├── budget.py
│   ├── category.py
│   ├── goal.py
│   └── transaction_category.py
├── schemas/
├── crud/
├── api/
├── core/
├── db/
```


```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

    transactions = relationship("Transaction", back_populates="user", cascade="all, delete")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete")
    goals = relationship("Goal", back_populates="user", cascade="all, delete")
```


```python
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud_user.create_user(db, user)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud_user.get_user(db, user_id)
```

# Alembic
Alembic — это инструмент для управления миграциями базы данных в проектах на SQLAlchemy/SQLModel.

Позволяет создавать, изменять и откатывать схемы БД без потери данных.

Генерирует скрипты миграций автоматически или вручную.

Упрощает поддержку базы при развитии проекта, когда меняются таблицы, колонки или связи.

Проще говоря: Alembic нужен, чтобы безболезненно обновлять структуру базы данных при изменениях в моделях.


![swaggerт](путь_к_картинке)
