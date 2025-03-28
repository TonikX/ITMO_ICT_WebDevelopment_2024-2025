from sqlmodel import Session, select
from models import Task, Tag, User, Category, TaskTag
import schemas

def load_task_with_tags(session: Session, task: Task) -> schemas.TaskRead:
    """
    Преобразует объект Task из базы данных в объект TaskRead с правильно загруженными тегами
    """
    # Загружаем пользователя
    user = session.get(User, task.user_id)
    user_read = schemas.UserRead(
        id=user.id,
        username=user.username,
        is_active=user.is_active,
        is_admin=user.is_admin,
        created_at=user.created_at
    )
    
    # Загружаем категорию, если она есть
    category_read = None
    if task.category_id:
        category = session.get(Category, task.category_id)
        if category:
            category_read = schemas.CategoryRead(
                id=category.id,
                name=category.name,
                description=category.description
            )
    
    # Загружаем теги
    tags_read = []
    for task_tag in task.tags:
        tag = session.get(Tag, task_tag.tag_id)
        if tag:
            tags_read.append(schemas.TagRead(
                id=tag.id,
                name=tag.name
            ))
    
    # Создаем объект TaskRead
    task_read = schemas.TaskRead(
        id=task.id,
        description=task.description,
        deadline=task.deadline,
        priority=task.priority,
        start_time=task.start_time,
        end_time=task.end_time,
        user=user_read,
        category=category_read,
        tags=tags_read
    )
    
    return task_read
