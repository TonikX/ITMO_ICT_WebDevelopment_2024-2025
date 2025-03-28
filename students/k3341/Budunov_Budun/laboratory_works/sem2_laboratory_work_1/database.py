from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
engine = create_engine(db_url, echo=True)  # echo=True для логирования SQL-запросов

# Функция для создания таблиц
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Функция для получения сессии
def get_session():
    with Session(engine) as session:
        yield session