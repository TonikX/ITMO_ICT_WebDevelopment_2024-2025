# your_app/management/commands/seed_db.py
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import transaction

from education.models import (
    ClassRoom, Teacher, Group, Student,
    Subject, TeacherSubject, Schedule, Grade
)

fake = Faker('ru_RU')  # Русские данные


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Количество записей для создания (по умолчанию 10)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Принудительная очистка всех данных без подтверждения'
        )

    def handle(self, *args, **options):
        count = options['count']
        force = options['force']

        # Очистка старых данных с подтверждением
        if not force:
            confirm = input(
                '⚠️  ВНИМАНИЕ: Все существующие данные будут удалены!\n'
                'Вы уверены? [y/N]: '
            )
            if confirm.lower() != 'y':
                self.stdout.write('❌ Операция отменена.')
                return

        self.stdout.write('Очистка старых данных...')
        self.clear_data()

        self.stdout.write('Создание кабинетов...')
        classrooms = self.create_classrooms(count // 2)

        self.stdout.write('Создание преподавателей...')
        teachers = self.create_teachers(count, classrooms)

        self.stdout.write('Создание групп...')
        groups = self.create_groups(count // 3, teachers)

        self.stdout.write('Создание студентов...')
        students = self.create_students(count * 3, groups)

        self.stdout.write('Создание дисциплин...')
        subjects = self.create_subjects()

        self.stdout.write('Связывание преподавателей с дисциплинами...')
        self.assign_teachers_to_subjects(teachers, subjects)

        self.stdout.write('Создание расписания...')
        self.create_schedule(groups, subjects, teachers, classrooms)

        self.stdout.write('Создание оценок...')
        self.create_grades(students, subjects, teachers)

        self.stdout.write(f'✅ База данных успешно заполнена! Создано:')
        self.stdout.write(f'   Кабинеты: {ClassRoom.objects.count()}')
        self.stdout.write(f'   Преподаватели: {Teacher.objects.count()}')
        self.stdout.write(f'   Группы: {Group.objects.count()}')
        self.stdout.write(f'   Студенты: {Student.objects.count()}')
        self.stdout.write(f'   Дисциплины: {Subject.objects.count()}')
        self.stdout.write(f'   Расписание: {Schedule.objects.count()}')
        self.stdout.write(f'   Оценки: {Grade.objects.count()}')
        self.stdout.write(f'\n📋 Тестовые пользователи:')
        self.stdout.write(f'   Преподаватели: teacher_1, teacher_2, ... (пароль: password123)')
        self.stdout.write(f'   Студенты: student_1, student_2, ... (пароль: password123)')

    def clear_data(self):
        """Очистка всех данных в правильном порядке"""
        try:
            # Очищаем в обратном порядке зависимостей
            with transaction.atomic():
                Grade.objects.all().delete()
                Schedule.objects.all().delete()
                TeacherSubject.objects.all().delete()
                Subject.objects.all().delete()
                Student.objects.all().delete()
                Group.objects.all().delete()
                Teacher.objects.all().delete()
                ClassRoom.objects.all().delete()

                # Удаляем тестовых пользователей (кроме суперпользователя)
                User.objects.filter(is_superuser=False).delete()

            # Сбрасываем автоинкремент (без VACUUM)
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sqlite_sequence;")

        except Exception as e:
            self.stdout.write(f'   ⚠️  Ошибка при очистке: {e}')
            # Если не удалось, просто продолжаем
            pass

        self.stdout.write('   ✅ Данные успешно очищены')

    def create_classrooms(self, count):
        """Создание кабинетов с реалистичными названиями"""
        classrooms = []

        classroom_names = [
            "Кабинет математики", "Кабинет информатики", "Кабинет физики",
            "Кабинет химии", "Лаборатория программирования", "Компьютерный класс 1",
            "Компьютерный класс 2", "Актовый зал", "Конференц-зал",
            "Кабинет иностранных языков", "Кабинет истории", "Спортивный зал",
            "Библиотека", "Кабинет черчения", "Кабинет электротехники",
            "Лаборатория сетевых технологий", "Кабинет базы данных",
            "Кабинет веб-разработки", "Мультимедийный класс", "Кабинет робототехники"
        ]

        room_numbers = list(range(100, 500, 10))

        for i in range(min(count, len(room_numbers))):
            classroom = ClassRoom.objects.create(
                room_number=room_numbers[i],
                name=random.choice(classroom_names),
                capacity=random.choice([20, 25, 30, 35, 40, 50])
            )
            classrooms.append(classroom)

        self.stdout.write(f'   Создано кабинетов: {len(classrooms)}')
        return classrooms

    def create_teachers(self, count, classrooms):
        """Создание преподавателей"""
        teachers = []
        positions = [
            'преподаватель', 'старший преподаватель',
            'доцент', 'профессор', 'заведующий кафедрой'
        ]

        for i in range(count):
            username = f"teacher_{i + 1}"

            # Создаем пользователя
            user = User.objects.create_user(
                username=username,
                password='password123',
                first_name=fake.first_name_male() if i % 2 else fake.first_name_female(),
                last_name=fake.last_name_male() if i % 2 else fake.last_name_female(),
                email=fake.email(),
            )

            teacher = Teacher.objects.create(
                surname=fake.last_name_male() if i % 2 else fake.last_name_female(),
                name=fake.first_name_male() if i % 2 else fake.first_name_female(),
                middle_name=fake.middle_name_male() if i % 2 else fake.middle_name_female(),
                position=random.choice(positions),
                classroom=random.choice(classrooms) if classrooms else None,
                is_active=random.choice([True, True, True, False]),  # 75% активных
                user_account=user
            )
            teachers.append(teacher)

        self.stdout.write(f'   Создано преподавателей: {len(teachers)}')
        return teachers

    def create_groups(self, count, teachers):
        """Создание групп"""
        groups = []
        specialties = [
            'Информационные системы и программирование',
            'Компьютерные сети',
            'Прикладная информатика',
            'Веб-технологии',
            'Кибербезопасность',
            'Разработка программного обеспечения',
            'Системное администрирование'
        ]

        group_names = []
        for course in range(1, 5):
            for letter in ['А', 'Б', 'В']:
                group_names.append(f"К{course}{letter}-01-23")

        for i in range(min(count, len(group_names))):
            group = Group.objects.create(
                name=group_names[i],
                course=random.randint(1, 4),
                specialty=random.choice(specialties),
                curator=random.choice(teachers) if teachers else None,
                created_year=2020 + random.randint(0, 4)
            )
            groups.append(group)

        self.stdout.write(f'   Создано групп: {len(groups)}')
        return groups

    def create_students(self, count, groups):
        """Создание студентов"""
        students = []
        statuses = ['active', 'active', 'active', 'dropped', 'academic_leave', 'graduated']

        for i in range(count):
            is_male = random.choice([True, False])

            # Создаем пользователя для каждого 4-го студента
            user = None
            if i % 4 == 0:
                username = f"student_{i + 1}"
                user = User.objects.create_user(
                    username=username,
                    password='password123',
                    first_name=fake.first_name_male() if is_male else fake.first_name_female(),
                    last_name=fake.last_name_male() if is_male else fake.last_name_female(),
                    email=fake.email(),
                )

            student = Student.objects.create(
                surname=fake.last_name_male() if is_male else fake.last_name_female(),
                name=fake.first_name_male() if is_male else fake.first_name_female(),
                middle_name=fake.middle_name_male() if is_male else fake.middle_name_female(),
                group=random.choice(groups) if groups else None,
                enrollment_date=timezone.now().date() - timedelta(days=random.randint(100, 1000)),
                status=random.choice(statuses),
                user_account=user
            )
            students.append(student)

        self.stdout.write(f'   Создано студентов: {len(students)}')
        return students

    def create_subjects(self):
        """Создание дисциплин"""
        subjects_data = [
            # 1 курс
            {'name': 'Основы программирования', 'course': 1, 'semester': 1, 'hours': 120},
            {'name': 'Математика', 'course': 1, 'semester': 1, 'hours': 100},
            {'name': 'Английский язык для IT', 'course': 1, 'semester': 1, 'hours': 80},
            {'name': 'Информационные технологии', 'course': 1, 'semester': 1, 'hours': 90},
            {'name': 'Базы данных', 'course': 1, 'semester': 2, 'hours': 110},
            {'name': 'Веб-разработка', 'course': 1, 'semester': 2, 'hours': 130},

            # 2 курс
            {'name': 'Алгоритмы и структуры данных', 'course': 2, 'semester': 1, 'hours': 140},
            {'name': 'Объектно-ориентированное программирование', 'course': 2, 'semester': 1, 'hours': 150},
            {'name': 'Администрирование Linux', 'course': 2, 'semester': 1, 'hours': 120},
            {'name': 'Мобильная разработка', 'course': 2, 'semester': 2, 'hours': 130},
            {'name': 'Тестирование ПО', 'course': 2, 'semester': 2, 'hours': 100},

            # 3 курс
            {'name': 'Машинное обучение', 'course': 3, 'semester': 1, 'hours': 160},
            {'name': 'Кибербезопасность', 'course': 3, 'semester': 1, 'hours': 140},
            {'name': 'Большие данные', 'course': 3, 'semester': 1, 'hours': 130},
            {'name': 'DevOps практики', 'course': 3, 'semester': 2, 'hours': 150},
            {'name': 'Проектирование ИС', 'course': 3, 'semester': 2, 'hours': 130},

            # 4 курс
            {'name': 'Дипломное проектирование', 'course': 4, 'semester': 1, 'hours': 200},
            {'name': 'Преддипломная практика', 'course': 4, 'semester': 1, 'hours': 180},
            {'name': 'Карьерное развитие в IT', 'course': 4, 'semester': 2, 'hours': 80},
        ]

        subjects = []
        for data in subjects_data:
            subject = Subject.objects.create(
                name=data['name'],
                course=data['course'],
                semester=data['semester'],
                hours=data['hours'],
                description=fake.text(max_nb_chars=100)
            )
            subjects.append(subject)

        self.stdout.write(f'   Создано дисциплин: {len(subjects)}')
        return subjects

    def assign_teachers_to_subjects(self, teachers, subjects):
        """Связывание преподавателей с дисциплинами"""
        for subject in subjects:
            # Назначаем 1-3 случайных активных преподавателя на предмет
            active_teachers = [t for t in teachers if t.is_active]
            if not active_teachers:
                continue

            num_teachers = random.randint(1, min(3, len(active_teachers)))
            subject_teachers = random.sample(active_teachers, num_teachers)

            for teacher in subject_teachers:
                TeacherSubject.objects.get_or_create(
                    teacher=teacher,
                    subject=subject
                )

        self.stdout.write(f'   Создано связей преподаватель-дисциплина: {TeacherSubject.objects.count()}')

    def create_schedule(self, groups, subjects, teachers, classrooms):
        """Создание расписания"""
        days_of_week = [1, 2, 3, 4, 5]  # Пн-Пт
        lesson_numbers = [1, 2, 3, 4, 5]
        lesson_types = ['lecture', 'practice', 'lab', 'seminar']
        week_types = ['odd', 'even', 'both']

        schedule_count = 0
        for group in groups:
            group_subjects = [s for s in subjects if s.course == group.course]
            if not group_subjects:
                continue

            for _ in range(random.randint(5, 8)):  # 5-8 занятий на группу
                subject = random.choice(group_subjects)

                # Находим преподавателей для этого предмета
                subject_teachers = TeacherSubject.objects.filter(subject=subject)
                if not subject_teachers:
                    continue

                teacher_subject = random.choice(list(subject_teachers))
                classroom = random.choice(classrooms) if classrooms else None

                Schedule.objects.create(
                    day_of_week=random.choice(days_of_week),
                    lesson_number=random.choice(lesson_numbers),
                    group=group,
                    subject=subject,
                    teacher=teacher_subject.teacher,
                    classroom=classroom,
                    lesson_type=random.choice(lesson_types),
                    week_type=random.choice(week_types),
                    start_date=timezone.now().date(),
                    end_date=timezone.now().date() + timedelta(days=90)
                )
                schedule_count += 1

        self.stdout.write(f'   Создано расписаний: {schedule_count}')

    def create_grades(self, students, subjects, teachers):
        """Создание оценок"""
        grade_types = ['current', 'semester', 'exam', 'credit']
        grade_count = 0

        for student in students:
            if student.status != 'active':
                continue

            # Создаем 3-8 оценок для активного студента
            for _ in range(random.randint(3, 8)):
                subject = random.choice(subjects)
                grade_type = random.choice(grade_types)
                grade_value = random.choice([3, 4, 5])  # Только положительные оценки

                # Находим преподавателя для этого предмета
                subject_teachers = TeacherSubject.objects.filter(subject=subject)
                teacher = None
                if subject_teachers:
                    teacher = random.choice(list(subject_teachers)).teacher

                Grade.objects.create(
                    student=student,
                    subject=subject,
                    grade=grade_value,
                    grade_type=grade_type,
                    semester=random.randint(1, 8),
                    date=timezone.now().date() - timedelta(days=random.randint(1, 365)),
                    teacher=teacher,
                    comments=random.choice([
                        '', 'Хорошая работа', 'Нужно больше стараться',
                        'Отличный результат', 'Присутствовали ошибки'
                    ])
                )
                grade_count += 1

        self.stdout.write(f'   Создано оценок: {grade_count}')