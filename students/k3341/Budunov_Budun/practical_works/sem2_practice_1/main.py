from fastapi import FastAPI, HTTPException, Path, Query, Body
from typing import List, Optional

from models import User, Category, Task
from temp_db import users_db, categories_db, tasks_db

app = FastAPI(title="Task Management API")

@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to Task Manager API"}

# User CRUD operations
@app.get("/users/", response_model=List[User], tags=["Users"])
def get_users():
    return users_db

@app.get("/users/{user_id}", response_model=User, tags=["Users"])
def get_user(user_id: int = Path(..., description="The ID of the user to get")):
    """Get a specific user by ID"""
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users/", response_model=User, tags=["Users"])
def create_user(user: User):
    """Create a new user"""
    # Check if user with the same ID already exists
    for existing_user in users_db:
        if existing_user["id"] == user.id:
            raise HTTPException(status_code=400, detail="User with this ID already exists")
    
    users_db.append(user.model_dump())
    return user

@app.put("/users/{user_id}", response_model=User, tags=["Users"])
def update_user(user_id: int, user: User):
    """Update a user"""
    for i, existing_user in enumerate(users_db):
        if existing_user["id"] == user_id:
            users_db[i] = user.model_dump()
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int):
    """Delete a user"""
    for i, user in enumerate(users_db):
        if user["id"] == user_id:
            del users_db[i]
            return {"message": f"User with ID {user_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

# Category CRUD operations
@app.get("/categories/", response_model=List[Category], tags=["Categories"])
def get_categories():
    """Get all categories"""
    return categories_db

@app.get("/categories/{category_id}", response_model=Category, tags=["Categories"])
def get_category(category_id: int = Path(..., description="The ID of the category to get")):
    """Get a specific category by ID"""
    for category in categories_db:
        if category["id"] == category_id:
            return category
    raise HTTPException(status_code=404, detail="Category not found")

@app.post("/categories/", response_model=Category, tags=["Categories"])
def create_category(category: Category):
    """Create a new category"""
    # Check if category with the same ID already exists
    for existing_category in categories_db:
        if existing_category["id"] == category.id:
            raise HTTPException(status_code=400, detail="Category with this ID already exists")
    
    categories_db.append(category.model_dump())
    return category

@app.put("/categories/{category_id}", response_model=Category, tags=["Categories"])
def update_category(category_id: int, category: Category):
    """Update a category"""
    for i, existing_category in enumerate(categories_db):
        if existing_category["id"] == category_id:
            categories_db[i] = category.model_dump()
            return category
    raise HTTPException(status_code=404, detail="Category not found")

@app.delete("/categories/{category_id}", tags=["Categories"])
def delete_category(category_id: int):
    """Delete a category"""
    for i, category in enumerate(categories_db):
        if category["id"] == category_id:
            del categories_db[i]
            return {"message": f"Category with ID {category_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Category not found")

# Task CRUD operations
@app.get("/tasks/", response_model=List[Task], tags=["Tasks"])
def get_tasks(priority: Optional[int] = Query(None, description="Filter tasks by priority")):
    """Get all tasks with optional priority filter"""
    if priority is not None:
        return [task for task in tasks_db if task["priority"] == priority]
    return tasks_db

@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def get_task(task_id: int = Path(..., description="The ID of the task to get")):
    """Get a specific task by ID"""
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks/", response_model=Task, tags=["Tasks"])
def create_task(task: Task):
    """Create a new task"""
    # Check if task with the same ID already exists
    for existing_task in tasks_db:
        if existing_task["id"] == task.id:
            raise HTTPException(status_code=400, detail="Task with this ID already exists")
    
    tasks_db.append(task.model_dump())
    return task

@app.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def update_task(task_id: int, task: Task):
    """Update a task"""
    for i, existing_task in enumerate(tasks_db):
        if existing_task["id"] == task_id:
            tasks_db[i] = task.model_dump()
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(task_id: int):
    """Delete a task"""
    for i, task in enumerate(tasks_db):
        if task["id"] == task_id:
            del tasks_db[i]
            return {"message": f"Task with ID {task_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")

# Additional endpoints for filtering tasks
@app.get("/users/{user_id}/tasks/", response_model=List[Task], tags=["Tasks"])
def get_user_tasks(user_id: int):
    """Get all tasks for a specific user"""
    return [task for task in tasks_db if task.get("user") and task["user"]["id"] == user_id]

@app.get("/categories/{category_id}/tasks/", response_model=List[Task], tags=["Tasks"])
def get_category_tasks(category_id: int):
    """Get all tasks for a specific category"""
    return [task for task in tasks_db if task.get("category") and task["category"]["id"] == category_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
