from contextlib import asynccontextmanager
from datetime import timedelta, datetime
from fastapi import FastAPI, HTTPException, Depends, status, Query
from typing import List, Optional
import requests
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from models import Task, User, Category, Tag, TaskTag, Schedule, ScheduleTask
from fastapi.security import OAuth2PasswordRequestForm
from security import (
    get_password_hash, 
    authenticate_user, 
    create_access_token, 
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_active_user,
    get_current_admin
)
import schemas
from functions import load_task_with_tags
from celery_tasks import parse_url_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the database
    create_db_and_tables()
    yield

app = FastAPI(
    title="Task Manager API",
    description="API for managing tasks, categories, tags, and schedules",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to Task Manager API"}


@app.get("/parse/{mode}")
async def parse_url(url: str, mode: str):
    if mode not in ["async", "threading", "multiprocessing", "queue"]:
        raise HTTPException(status_code=400, detail="Invalid mode. Use 'async', 'threading', 'multiprocessing', or 'queue'")
    
    try:
        if mode == "queue":
            task = parse_url_task.delay(url, mode)
            return {"task_id": task.id, "status": "Task queued for parsing"}
        else:
            parser_url = f"http://parser:8001/parse/{mode}?url={url}"
            response = requests.get(parser_url)
            response.raise_for_status()
            return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error calling parser service: {str(e)}")

# Эндпоинт для авторизации и получения токена
@app.post("/token", response_model=schemas.Token, tags=["Authentication"])
def login_for_access_token(
    login_data: schemas.LoginRequest,
    session: Session = Depends(get_session)
    ):
    # Аутентификация пользователя
    user = authenticate_user(session, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Проверка, что пользователь активен
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    
    # Создание токена доступа
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username, "id": user.id}, 
        expires_delta=access_token_expires
    )
    
    # Возвращение токена
    return {"access_token": access_token, "token_type": "bearer"}

# User endpoints
@app.post("/users/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED, tags=["Users"])
def registrate(
    user: schemas.UserCreate, 
    session: Session = Depends(get_session)):
    # check if username already exists
    existing_username = session.exec(select(User).where(User.username == user.username)).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # create user with hashed password
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/users/me/", response_model=schemas.UserRead, tags=["Users"])
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.patch("/users/me/", response_model=schemas.UserRead, tags=["Users"])
def update_user(
    user_update: schemas.UserUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
    ):
    # check if new username is already taken
    if user_update.username and user_update.username != current_user.username:
        existing_username = session.exec(
            select(User).where(User.username == user_update.username)
        ).first()
        if existing_username:
            raise HTTPException(status_code=400, detail="Username already taken")
    
    # update user
    user_data = user_update.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(current_user, key, value)
    
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

@app.post("/users/me/change-password/", response_model=schemas.UserRead, tags=["Users"])
def change_password(
    password_change: schemas.UserPasswordChange,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
    ):
    # current user check
    if not authenticate_user(session, current_user.username, password_change.current_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    
    # update password
    current_user.hashed_password = get_password_hash(password_change.new_password)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

@app.get("/users/", response_model=List[schemas.UserRead], tags=["Users"])
def get_users(
    skip: int = 0, 
    limit: int = 100, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
    ):
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    return users

# Подзапрос для получения пользователей с наибольшим количеством задач
@app.get("/users/most-active", response_model=List[schemas.UserWithTaskCount], tags=["Users"])
def get_most_active_users(
    limit: int = 5,
    current_user: User = Depends(get_current_admin),  # Только для админов
    session: Session = Depends(get_session)
):
    # Подзапрос для подсчета задач каждого пользователя
    user_task_counts = []
    users = session.exec(select(User)).all()
    
    for user in users:
        # Исправленный способ подсчета задач
        tasks = session.exec(select(Task).where(Task.user_id == user.id)).all()
        task_count = len(tasks)
        
        # Альтернативный способ с использованием func.count()
        # from sqlalchemy import func
        # task_count = session.exec(
        #     select(func.count()).select_from(Task).where(Task.user_id == user.id)
        # ).one()
        
        user_task_counts.append({
            "id": user.id,
            "username": user.username,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
            "task_count": task_count
        })
    
    # Сортировка по количеству задач (по убыванию)
    user_task_counts.sort(key=lambda x: x["task_count"], reverse=True)
    
    # Возвращаем только указанное количество пользователей
    return user_task_counts[:limit]



@app.get("/users/{user_id}", response_model=schemas.UserRead, tags=["Users"])
def get_user(
    user_id: int, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Category endpoints
@app.post("/categories/", response_model=schemas.CategoryRead, status_code=status.HTTP_201_CREATED, tags=["Categories"])
def create_category(
    category: schemas.CategoryCreate, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)):
    # Check if category name already exists
    existing_category = session.exec(select(Category).where(Category.name == category.name)).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category name already exists")
    
    db_category = Category(**category.model_dump())
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@app.get("/categories/", response_model=List[schemas.CategoryRead], tags=["Categories"])
def get_categories(
    skip: int = 0, 
    limit: int = 100, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)):
    categories = session.exec(select(Category).offset(skip).limit(limit)).all()
    return categories

@app.get("/categories/{category_id}", response_model=schemas.CategoryRead, tags=["Categories"])
def get_category(
    category_id: int, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# Tag endpoints
@app.post("/tags/", response_model=schemas.TagRead, status_code=status.HTTP_201_CREATED, tags=["Tags"])
def create_tag(
    tag: schemas.TagCreate, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)):
    # Check if tag name already exists
    existing_tag = session.exec(select(Tag).where(Tag.name == tag.name)).first()
    if existing_tag:
        raise HTTPException(status_code=400, detail="Tag name already exists")
    
    db_tag = Tag(**tag.model_dump())
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag

@app.get("/tags/", response_model=List[schemas.TagRead], tags=["Tags"])
def get_tags(
    skip: int = 0, 
    limit: int = 100, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)):
    tags = session.exec(select(Tag).offset(skip).limit(limit)).all()
    return tags

@app.get("/tags/{tag_id}", response_model=schemas.TagRead, tags=["Tags"])
def get_tag(
    tag_id: int, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@app.delete("/tags/range/", tags=["Tags"])
def delete_tags_by_id_range(
    min_id: int = Query(..., description="Минимальное значение ID для удаления"),
    max_id: int = Query(..., description="Максимальное значение ID для удаления"),
    current_user: User = Depends(get_current_admin),  # Только для администраторов
    session: Session = Depends(get_session)
):
    """
    Удаляет теги, ID которых находятся в заданном диапазоне.
    
    Args:
        min_id: Минимальное значение ID для удаления (включительно)
        max_id: Максимальное значение ID для удаления (включительно)
        
    Returns:
        Информацию о количестве удаленных тегов
    """
    # Проверка корректности диапазона
    if min_id > max_id:
        raise HTTPException(status_code=400, detail="min_id должен быть меньше или равен max_id")
    
    # Находим все теги в заданном диапазоне
    tags_to_delete = session.exec(
        select(Tag).where(Tag.id >= min_id, Tag.id <= max_id)
    ).all()
    
    # Если теги не найдены, возвращаем соответствующее сообщение
    if not tags_to_delete:
        return {"message": "Теги в указанном диапазоне не найдены", "deleted_count": 0}
    
    # Получаем список ID тегов для информационных целей
    deleted_tag_ids = [tag.id for tag in tags_to_delete]
    deleted_tag_names = [tag.name for tag in tags_to_delete]
    
    # Удаляем связи тегов с задачами
    for tag in tags_to_delete:
        # Находим все связи TaskTag для данного тега
        task_tags = session.exec(
            select(TaskTag).where(TaskTag.tag_id == tag.id)
        ).all()
        
        # Удаляем найденные связи
        for task_tag in task_tags:
            session.delete(task_tag)
    
    # Удаляем теги
    delete_count = 0
    for tag in tags_to_delete:
        session.delete(tag)
        delete_count += 1
    
    # Сохраняем изменения
    session.commit()
    
    # Возвращаем информацию об удаленных тегах
    return {
        "message": f"Успешно удалено {delete_count} тегов",
        "deleted_count": delete_count,
        "deleted_tag_ids": deleted_tag_ids,
        "deleted_tag_names": deleted_tag_names
    }

# Task endpoints
@app.post("/tasks/", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(
    task: schemas.TaskCreate, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)):
    # Validate user exists
    user = session.get(User, task.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate category exists if provided
    if task.category_id:
        category = session.get(Category, task.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    # Validate tags exist
    for tag_id in task.tag_ids:
        tag = session.get(Tag, tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail=f"Tag with id {tag_id} not found")
    
    # Create task
    db_task = Task(
        description=task.description,
        deadline=task.deadline,
        priority=task.priority,
        user_id=task.user_id,
        category_id=task.category_id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    # Add tags
    for tag_id in task.tag_ids:
        task_tag = TaskTag(task_id=db_task.id, tag_id=tag_id)
        session.add(task_tag)
    
    session.commit()
    session.refresh(db_task)
    
    return db_task

@app.get("/tasks/", response_model=List[schemas.TaskRead], tags=["Tasks"])
def get_tasks(
    skip: int = 0, 
    limit: int = 100, 
    user_id: Optional[int] = None,
    category_id: Optional[int] = None,
    priority: Optional[int] = None,
    is_active: Optional[bool] = None,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    query = select(Task)
    
    # Apply filters if provided
    if user_id:
        query = query.where(Task.user_id == user_id)
    if category_id:
        query = query.where(Task.category_id == category_id)
    if priority:
        query = query.where(Task.priority == priority)
    if is_active is not None:
        if is_active:
            # Active tasks have start_time but no end_time
            query = query.where(Task.start_time.is_not(None), Task.end_time.is_(None))
        else:
            # Inactive tasks either haven't started or have ended
            query = query.where((Task.start_time.is_(None)) | (Task.end_time.is_not(None)))
    
    tasks = session.exec(query.offset(skip).limit(limit)).all()
    # Преобразуем задачи в формат, соответствующий схеме TaskRead
    result = []
    for task in tasks:
        # Загружаем связанные данные
        task_with_tags = load_task_with_tags(session, task)
        result.append(task_with_tags)
    
    return result

# Подзапрос для получения просроченных задач
@app.get("/tasks/overdue", response_model=List[schemas.TaskRead], tags=["Tasks"])
def get_overdue_tasks(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    # Подзапрос для получения задач с дедлайном в прошлом и без отметки о завершении
    now = datetime.now()
    tasks = session.exec(
        select(Task).where(
            Task.deadline < now,
            Task.end_time.is_(None)
        )
    ).all()
    
    return tasks


@app.get("/tasks/{task_id}", response_model=schemas.TaskRead, tags=["Tasks"])
def get_task(
    task_id: int, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Преобразуем задачу в формат TaskRead
    task_read = load_task_with_tags(session, task)
    return task_read

@app.patch("/tasks/{task_id}", response_model=schemas.TaskRead, tags=["Tasks"])
def update_task(
    task_id: int, 
    task_update: schemas.TaskUpdate, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    # Проверяем существование задачи
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Проверяем, принадлежит ли задача текущему пользователю
    if db_task.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=403, 
            detail="You don't have permission to update this task"
        )
    
    # Получаем данные для обновления, исключая неуказанные поля
    task_data = task_update.model_dump(exclude_unset=True)
    
    # Отдельно обрабатываем список тегов
    tag_ids = task_data.pop("tag_ids", None)
    
    # Обрабатываем числовые поля - игнорируем значения меньше 1
    numeric_fields = ["priority", "category_id"]
    for field in numeric_fields:
        if field in task_data and task_data[field] is not None and task_data[field] < 1:
            # Удаляем поле из данных обновления, чтобы игнорировать его
            task_data.pop(field)
    
    # Обновляем атрибуты задачи
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    # Обновляем теги, если они предоставлены
    if tag_ids is not None:
        # Фильтруем недопустимые ID тегов (меньше 1)
        valid_tag_ids = [tag_id for tag_id in tag_ids if tag_id >= 1]
        
        # Получаем существующие связи тегов
        existing_task_tags = session.exec(
            select(TaskTag).where(TaskTag.task_id == task_id)
        ).all()
        
        # Удаляем существующие связи тегов
        for task_tag in existing_task_tags:
            if task_tag.tag_id not in valid_tag_ids:
                session.delete(task_tag)
            else:
                valid_tag_ids.remove(task_tag.tag_id)
        
        # Добавляем новые связи тегов
        for tag_id in valid_tag_ids:
            tag = session.get(Tag, tag_id)
            if not tag:
                raise HTTPException(status_code=404, detail=f"Tag with id {tag_id} not found")
            
            task_tag = TaskTag(task_id=task_id, tag_id=tag_id)
            session.add(task_tag)
    
    # Сохраняем изменения в базе данных
    session.commit()
    session.refresh(db_task)
    
    # Преобразуем задачу в формат TaskRead
    return load_task_with_tags(session, db_task)



@app.delete("/tasks/{task_id}", response_model=schemas.TaskRead, tags=["Tasks"])
def delete_task(
    task_id: int, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(task)
    session.commit()
    return task

# New endpoints for task actions
@app.post("/tasks/{task_id}/start", response_model=schemas.TaskRead, tags=["Task Actions"])
def start_task(
    task_id: int, 
    action: Optional[schemas.TaskStartAction] = None, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check if task is already started but not completed
    if task.start_time and not task.end_time:
        raise HTTPException(status_code=400, detail="Task is already in progress")
    
    # Set start time (use provided time or current time)
    start_time = None
    if action and action.start_time:
        start_time = action.start_time
    else:
        start_time = datetime.now()
    
    task.start_time = start_time
    task.end_time = None  # Reset end time if task is being restarted
    
    session.commit()
    session.refresh(task)
    return task

@app.post("/tasks/{task_id}/end", response_model=schemas.TaskRead, tags=["Task Actions"])
def end_task(
    task_id: int, 
    action: Optional[schemas.TaskEndAction] = None, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check if task is started
    if not task.start_time:
        raise HTTPException(status_code=400, detail="Task has not been started yet")
    
    # Check if task is already completed
    if task.end_time:
        raise HTTPException(status_code=400, detail="Task is already completed")
    
    # Set end time (use provided time or current time)
    end_time = None
    if action and action.end_time:
        end_time = action.end_time
    else:
        end_time = datetime.now()
    
    # Validate end time is after start time
    if end_time < task.start_time:
        raise HTTPException(status_code=400, detail="End time cannot be before start time")
    
    task.end_time = end_time
    
    session.commit()
    session.refresh(task)
    return task

@app.get("/tasks/{task_id}/time-spent", tags=["Task Actions"])
def get_task_time_spent(
    task_id: int, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Calculate time spent
    if not task.start_time:
        return {"time_spent_minutes": 0, "message": "Task has not been started yet"}
    
    if not task.end_time:
        # Task is still in progress, calculate time spent so far
        time_spent = datetime.now() - task.start_time
        minutes = int(time_spent.total_seconds() // 60)  # Round down to minutes
        return {
            "time_spent_minutes": minutes,
            "message": "Task is in progress",
            "is_active": True
        }
    else:
        # Task is completed
        time_spent = task.end_time - task.start_time
        minutes = int(time_spent.total_seconds() // 60)  # Round down to minutes
        return {
            "time_spent_minutes": minutes,
            "message": "Task is completed",
            "is_active": False
        }

# Schedule endpoints
@app.post("/schedules/", response_model=schemas.ScheduleRead, status_code=status.HTTP_201_CREATED, tags=["Schedules"])
def create_schedule(
    schedule: schemas.ScheduleCreate, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)):
    # Validate user exists
    user = session.get(User, schedule.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create schedule
    db_schedule = Schedule(
        date=schedule.date,
        user_id=schedule.user_id
    )
    session.add(db_schedule)
    session.commit()
    session.refresh(db_schedule)
    
    # Add tasks to schedule
    for task_id in schedule.task_ids:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        
        schedule_task = ScheduleTask(
            schedule_id=db_schedule.id,
            task_id=task_id
        )
        session.add(schedule_task)
    
    session.commit()
    session.refresh(db_schedule)
    return db_schedule

@app.get("/schedules/", response_model=List[schemas.ScheduleRead], tags=["Schedules"])
def get_schedules(
    skip: int = 0, 
    limit: int = 100, 
    user_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    query = select(Schedule)
    
    if user_id:
        query = query.where(Schedule.user_id == user_id)
    
    schedules = session.exec(query.offset(skip).limit(limit)).all()
    return schedules

@app.get("/schedules/{schedule_id}", response_model=schemas.ScheduleRead, tags=["Schedules"])
def get_schedule(schedule_id: int, session: Session = Depends(get_session)):
    schedule = session.get(Schedule, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

# Добавление задачи в расписание
@app.post("/schedules/{schedule_id}/add-task", response_model=schemas.ScheduleRead, tags=["Schedules"])
def add_task_to_schedule(
    schedule_id: int,
    task_id: int,
    planned_start: Optional[datetime] = None,
    planned_duration: Optional[int] = None,  # в минутах
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    # Проверяем существование расписания
    schedule = session.get(Schedule, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    # Проверяем, принадлежит ли расписание текущему пользователю
    if schedule.user_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="You don't have permission to modify this schedule"
        )
    
    # Проверяем существование задачи
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Проверяем, принадлежит ли задача текущему пользователю
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="You don't have permission to add this task"
        )
    
    # Проверяем, не добавлена ли уже эта задача в расписание
    existing_schedule_task = session.exec(
        select(ScheduleTask).where(
            ScheduleTask.schedule_id == schedule_id,
            ScheduleTask.task_id == task_id
        )
    ).first()
    
    if existing_schedule_task:
        raise HTTPException(
            status_code=400, 
            detail="This task is already in the schedule"
        )
    
    # Преобразуем длительность из минут в timedelta, если указана
    duration_timedelta = None
    if planned_duration is not None:
        duration_timedelta = timedelta(minutes=planned_duration)
    
    # Создаем связь между расписанием и задачей
    schedule_task = ScheduleTask(
        schedule_id=schedule_id,
        task_id=task_id,
        planned_start=planned_start,
        planned_duration=duration_timedelta
    )
    
    session.add(schedule_task)
    session.commit()
    session.refresh(schedule)
    
    return schedule

# Получение всех расписаний текущего пользователя
@app.get("/users/me/schedules", response_model=List[schemas.ScheduleRead], tags=["Schedules"])
def get_user_schedules(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    # Создаем базовый запрос для получения расписаний пользователя
    query = select(Schedule).where(Schedule.user_id == current_user.id)
    
    # Добавляем фильтры по датам, если они указаны
    if start_date:
        query = query.where(Schedule.date >= start_date)
    
    if end_date:
        query = query.where(Schedule.date <= end_date)
    
    # Сортируем по дате (от ближайшей к более поздней)
    query = query.order_by(Schedule.date)
    
    # Выполняем запрос с пагинацией
    schedules = session.exec(query.offset(skip).limit(limit)).all()
    
    return schedules
