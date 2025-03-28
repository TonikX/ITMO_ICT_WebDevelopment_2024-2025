from getpass import getpass
from sqlmodel import Session, select
from models import Task, User
from database import engine, get_session
from security import get_password_hash, authenticate_user, create_access_token
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from models import User
from schemas import TokenData
from database import get_session
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# Инициализация контекста для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Инициализация OAuth2 с использованием Bearer токенов
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    """Проверка соответствия пароля хешу"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Получение хеша пароля"""
    return pwd_context.hash(password)

def get_password_from_hash(hashed_password):
    """Получение пароля из хеша"""
    return pwd_context.verify(hashed_password)

def create_admin():
    # Проверка, существует ли уже администратор
    with Session(engine) as session:
        existing_admin = session.exec(select(User).where(User.is_admin == True)).first()
        
        if existing_admin:
            print(f"Администратор уже существует: {existing_admin.username}")
            choice = input("Хотите создать еще одного администратора? (y/n): ")
            if choice.lower() != 'y':
                return
        
        # Запрос данных для нового администратора
        username = input("Введите имя пользователя: ")
        
        # Проверка, существует ли пользователь с таким именем или email
        existing_user = session.exec(
            select(User).where((User.username == username))
        ).first()
        
        if existing_user:
            print("Пользователь с таким именем уже существует.")
            return
        
        # Запрос и подтверждение пароля
        while True:
            password = getpass("Введите пароль: ")
            confirm_password = getpass("Подтвердите пароль: ")
            
            if password == confirm_password:
                break
            print("Пароли не совпадают. Попробуйте снова.")
        
        # Создание администратора
        admin_user = User(
            username=username,
            hashed_password=get_password_hash(password),
            is_active=True,
            is_admin=True
        )
        
        session.add(admin_user)
        session.commit()
        
        print(f"Администратор {username} успешно создан!")

def change_password(username: str, new_password: str):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
        if user:
            user.hashed_password = get_password_hash(new_password)
            session.commit()
            print(f"Пароль для пользователя {username} успешно изменен.")
            print(f"Хеш нового пароля: {user.hashed_password}")
        else:
            print(f"Пользователь {username} не найден.")

def get_task_by_id(task_id: int):
    with Session(engine) as session:
        task = session.exec(select(Task).where(Task.id == task_id)).first()
        if task:
            return task
        else:
            return None

if __name__ == "__main__":
    # create_admin()
    password = 'default'
    username = 'admin'
    task_id = 9

    print(get_task_by_id(task_id))
