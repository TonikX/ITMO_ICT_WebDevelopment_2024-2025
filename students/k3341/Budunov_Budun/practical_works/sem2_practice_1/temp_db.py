# Users data
users_db = [
    {
        "id": 1,
        "username": "admin",
        "is_active": True,
        "is_admin": True
    },
    {
        "id": 2,
        "username": "user1",
        "is_active": True,
        "is_admin": False
    },
    {
        "id": 3,
        "username": "user2",
        "is_active": False,
        "is_admin": False
    }
]

# Categories data
categories_db = [
    {
        "id": 1,
        "name": "Work",
        "description": "Work-related tasks"
    },
    {
        "id": 2,
        "name": "Personal",
        "description": "Personal tasks"
    },
    {
        "id": 3,
        "name": "Study",
        "description": "Educational tasks"
    }
]

# Tasks data
tasks_db = [
    {
        "id": 1,
        "description": "Complete project report",
        "priority": 1,
        "user": users_db[0],
        "category": categories_db[0]
    },
    {
        "id": 2,
        "description": "Buy groceries",
        "priority": 2,
        "user": users_db[1],
        "category": categories_db[1]
    },
    {
        "id": 3,
        "description": "Study for exam",
        "priority": 1,
        "user": users_db[1],
        "category": categories_db[2]
    },
    {
        "id": 4,
        "description": "Prepare presentation",
        "priority": 3,
        "user": users_db[0],
        "category": categories_db[0]
    }
]
