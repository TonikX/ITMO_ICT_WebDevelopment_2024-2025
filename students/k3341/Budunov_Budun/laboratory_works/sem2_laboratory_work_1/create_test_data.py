import datetime
from sqlmodel import Session, select
from database import create_db_and_tables, engine
from models import User, Category, Tag, Task, TaskTag, Schedule, ScheduleTask
from security import get_password_hash

def create_test_data():
    # Создаем таблицы
    create_db_and_tables()
    
    # Открываем сессию
    with Session(engine) as session:
        # Проверяем, есть ли уже данные в базе
        # existing_users = session.exec(select(User)).all()
        # if existing_users:
        #     print("База данных уже содержит тестовые данные. Пропускаем создание.")
        #     return
        
        print("Создание тестовых данных...")
        
        # Создаем пользователей
        new_admin_user = User(
            username="new_admin", # new_admin_updated
            hashed_password=get_password_hash("new_adminpass"),
            is_active=True,
            is_admin=True
        )
        
        regular_new_user1 = User(
            username="new_user1",
            hashed_password=get_password_hash("new_user1pass"),
            is_active=True
        )
        
        regular_alex = User(
            username="alex",
            hashed_password=get_password_hash("alexpass"),
            is_active=True
        )
        
        inactive_user = User(
            username="inactive",
            hashed_password=get_password_hash("inactivepass"),
            is_active=False
        )
        
        session.add(new_admin_user)
        session.add(regular_new_user1)
        session.add(regular_alex)
        session.add(inactive_user)
        session.commit()
        
        # Обновляем объекты пользователей, чтобы получить их ID
        new_admin_user = session.exec(select(User).where(User.username == "new_admin")).one()
        regular_new_user1 = session.exec(select(User).where(User.username == "new_user1")).one()
        regular_alex = session.exec(select(User).where(User.username == "alex")).one()
        
        # Создаем категории
        categories = [
            Category(name="Работа", description="Рабочие задачи"),
            Category(name="Учеба", description="Учебные задачи"),
            Category(name="Личное", description="Личные задачи"),
            Category(name="Срочное", description="Срочные задачи"),
            Category(name="Хобби", description="Хобби и развлечения")
        ]
        
        for category in categories:
            session.add(category)
        session.commit()
        
        # Получаем созданные категории
        categories = session.exec(select(Category)).all()
        
        # Создаем теги
        tags = [
            Tag(name="важно"),
            Tag(name="срочно"),
            Tag(name="отложено"),
            Tag(name="встреча"),
            Tag(name="звонок"),
            Tag(name="email"),
            Tag(name="документ"),
            Tag(name="проект")
        ]
        
        for tag in tags:
            session.add(tag)
        session.commit()
        
        # Получаем созданные теги
        tags = session.exec(select(Tag)).all()
        
        # Текущее время и даты для задач
        now = datetime.datetime.now()
        tomorrow = now + datetime.timedelta(days=1)
        next_week = now + datetime.timedelta(days=7)
        last_week = now - datetime.timedelta(days=7)
        yesterday = now - datetime.timedelta(days=1)
        
        # Создаем задачи для первого пользователя
        tasks_new_user1 = [
            # Активная задача (начата, но не завершена)
            Task(
                description="Подготовить отчет",
                deadline=tomorrow,
                priority=8,
                start_time=now - datetime.timedelta(hours=2),
                end_time=None,
                user_id=regular_new_user1.id,
                category_id=categories[0].id  # Работа
            ),
            # Завершенная задача
            Task(
                description="Позвонить клиенту",
                deadline=yesterday,
                priority=5,
                start_time=yesterday - datetime.timedelta(hours=3),
                end_time=yesterday - datetime.timedelta(hours=2),
                user_id=regular_new_user1.id,
                category_id=categories[0].id  # Работа
            ),
            # Просроченная задача (не начата)
            Task(
                description="Отправить email",
                deadline=yesterday,
                priority=4,
                start_time=None,
                end_time=None,
                user_id=regular_new_user1.id,
                category_id=categories[0].id  # Работа
            ),
            # Будущая задача
            Task(
                description="Подготовиться к экзамену",
                deadline=next_week,
                priority=9,
                start_time=None,
                end_time=None,
                user_id=regular_new_user1.id,
                category_id=categories[1].id  # Учеба
            ),
            # Личная задача
            Task(
                description="Купить продукты",
                deadline=tomorrow,
                priority=3,
                start_time=None,
                end_time=None,
                user_id=regular_new_user1.id,
                category_id=categories[2].id  # Личное
            )
        ]
        
        for task in tasks_new_user1:
            session.add(task)
        session.commit()
        
        # Создаем задачи для второго пользователя
        tasks_alex = [
            # Активная задача
            Task(
                description="Разработать новую функцию",
                deadline=tomorrow,
                priority=7,
                start_time=now - datetime.timedelta(hours=1),
                end_time=None,
                user_id=regular_alex.id,
                category_id=categories[0].id  # Работа
            ),
            # Завершенная задача
            Task(
                description="Прочитать статью",
                deadline=yesterday,
                priority=2,
                start_time=yesterday - datetime.timedelta(hours=5),
                end_time=yesterday - datetime.timedelta(hours=4),
                user_id=regular_alex.id,
                category_id=categories[1].id  # Учеба
            ),
            # Срочная задача
            Task(
                description="Подготовить презентацию",
                deadline=tomorrow,
                priority=10,
                start_time=None,
                end_time=None,
                user_id=regular_alex.id,
                category_id=categories[3].id  # Срочное
            )
        ]
        
        for task in tasks_alex:
            session.add(task)
        session.commit()
        
        # Создаем задачи для админа
        tasks_new_admin = [
            Task(
                description="Проверить систему",
                deadline=tomorrow,
                priority=6,
                start_time=None,
                end_time=None,
                user_id=new_admin_user.id,
                category_id=categories[0].id  # Работа
            ),
            Task(
                description="Обновить документацию",
                deadline=next_week,
                priority=4,
                start_time=None,
                end_time=None,
                user_id=new_admin_user.id,
                category_id=categories[0].id  # Работа
            )
        ]
        
        for task in tasks_new_admin:
            session.add(task)
        session.commit()
        
        # Получаем все созданные задачи
        all_tasks = session.exec(select(Task)).all()
        
        # Добавляем теги к задачам
        task_tags = [
            # Для первого пользователя
            TaskTag(task_id=tasks_new_user1[0].id, tag_id=tags[0].id),  # важно
            TaskTag(task_id=tasks_new_user1[0].id, tag_id=tags[1].id),  # срочно
            TaskTag(task_id=tasks_new_user1[1].id, tag_id=tags[4].id),  # звонок
            TaskTag(task_id=tasks_new_user1[2].id, tag_id=tags[5].id),  # email
            TaskTag(task_id=tasks_new_user1[3].id, tag_id=tags[0].id),  # важно
            TaskTag(task_id=tasks_new_user1[4].id, tag_id=tags[2].id),  # отложено
            
            # Для второго пользователя
            TaskTag(task_id=tasks_alex[0].id, tag_id=tags[7].id),  # проект
            TaskTag(task_id=tasks_alex[1].id, tag_id=tags[6].id),  # документ
            TaskTag(task_id=tasks_alex[2].id, tag_id=tags[0].id),  # важно
            TaskTag(task_id=tasks_alex[2].id, tag_id=tags[1].id),  # срочно
            
            # Для админа
            TaskTag(task_id=tasks_new_admin[0].id, tag_id=tags[0].id),  # важно
            TaskTag(task_id=tasks_new_admin[1].id, tag_id=tags[6].id),  # документ
        ]
        
        for task_tag in task_tags:
            session.add(task_tag)
        session.commit()
        
        # Создаем расписания
        today_schedule_new_user1 = Schedule(
            date=now.date(),
            user_id=regular_new_user1.id
        )
        
        tomorrow_schedule_new_user1 = Schedule(
            date=tomorrow.date(),
            user_id=regular_new_user1.id
        )
        
        today_schedule_alex = Schedule(
            date=now.date(),
            user_id=regular_alex.id
        )
        
        session.add(today_schedule_new_user1)
        session.add(tomorrow_schedule_new_user1)
        session.add(today_schedule_alex)
        session.commit()
        
        # Обновляем объекты расписаний, чтобы получить их ID
        today_schedule_new_user1 = session.exec(
            select(Schedule).where(
                Schedule.date == now.date(),
                Schedule.user_id == regular_new_user1.id
            )
        ).one()
        
        tomorrow_schedule_new_user1 = session.exec(
            select(Schedule).where(
                Schedule.date == tomorrow.date(),
                Schedule.user_id == regular_new_user1.id
            )
        ).one()
        
        today_schedule_alex = session.exec(
            select(Schedule).where(
                Schedule.date == now.date(),
                Schedule.user_id == regular_alex.id
            )
        ).one()
        
        # Добавляем задачи в расписания
        schedule_tasks = [
            # Сегодняшнее расписание пользователя 1
            ScheduleTask(
                schedule_id=today_schedule_new_user1.id,
                task_id=tasks_new_user1[0].id,
                planned_start=now.replace(hour=9, minute=0),
                planned_duration=datetime.timedelta(hours=2)
            ),
            ScheduleTask(
                schedule_id=today_schedule_new_user1.id,
                task_id=tasks_new_user1[2].id,
                planned_start=now.replace(hour=11, minute=0),
                planned_duration=datetime.timedelta(minutes=30)
            ),
            
            # Завтрашнее расписание пользователя 1
            ScheduleTask(
                schedule_id=tomorrow_schedule_new_user1.id,
                task_id=tasks_new_user1[3].id,
                planned_start=tomorrow.replace(hour=10, minute=0),
                planned_duration=datetime.timedelta(hours=3)
            ),
            ScheduleTask(
                schedule_id=tomorrow_schedule_new_user1.id,
                task_id=tasks_new_user1[4].id,
                planned_start=tomorrow.replace(hour=14, minute=0),
                planned_duration=datetime.timedelta(hours=1)
            ),
            
            # Сегодняшнее расписание пользователя 2
            ScheduleTask(
                schedule_id=today_schedule_alex.id,
                task_id=tasks_alex[0].id,
                planned_start=now.replace(hour=9, minute=0),
                planned_duration=datetime.timedelta(hours=4)
            ),
            ScheduleTask(
                schedule_id=today_schedule_alex.id,
                task_id=tasks_alex[2].id,
                planned_start=now.replace(hour=14, minute=0),
                planned_duration=datetime.timedelta(hours=2)
            )
        ]
        
        for schedule_task in schedule_tasks:
            session.add(schedule_task)
        session.commit()
        
        print("Тестовые данные успешно созданы!")
        print("\nУчетные данные для тестирования:")
        print("1. Администратор:")
        print("   - Логин: new_admin")
        print("   - Пароль: new_adminpass")
        print("2. Обычный пользователь 1:")
        print("   - Логин: new_user1")
        print("   - Пароль: new_user1pass")
        print("3. Обычный пользователь 2:")
        print("   - Логин: alex")
        print("   - Пароль: alexpass")
        print("4. Неактивный пользователь:")
        print("   - Логин: inactive")
        print("   - Пароль: inactivepass")

if __name__ == "__main__":
    create_test_data()
