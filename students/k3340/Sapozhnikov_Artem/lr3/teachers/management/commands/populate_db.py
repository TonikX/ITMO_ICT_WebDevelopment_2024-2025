from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
import random

fake = Faker()

from teachers.models import Teacher
from students.models import Student, SchoolClass, Grade, Lesson
try:
    from teachers.models import Subject
except ImportError:
    Subject = None

# Через какую модель связываем учителей и предметы
TeacherSubjectPeriod = None
try:
    TeacherSubjectPeriod = getattr(__import__('teachers.models', fromlist=['TeacherSubjectPeriod']), 'TeacherSubjectPeriod')
except Exception:
    TeacherSubjectPeriod = None


class Command(BaseCommand):
    help = 'Заполняет базу случайными данными: предметы, классы, учителя, учеников, оценки, расписание'

    def handle(self, *args, **options):
        with transaction.atomic():
            # --- Subjects ---
            subject_names = ["Математика", "Русский язык", "Физика", "Химия", "Биология",
                             "История", "Литература", "Информатика", "География", "Английский"]
            created_subjects = []
            if Subject is not None:
                for name in subject_names:
                    subj, _ = Subject.objects.get_or_create(name=name)
                    created_subjects.append(subj)
                self.stdout.write(self.style.SUCCESS(f'Создано/найдено {len(created_subjects)} предметов.'))
            else:
                self.stdout.write(self.style.WARNING('Модель Subject не найдена — пропускаем создание предметов.'))

            # --- SchoolClass ---
            class_names = ["5А", "6А", "7А", "8А", "9А", "10А", "11А"]
            created_classes = []
            for cname in class_names:
                c, _ = SchoolClass.objects.get_or_create(name=cname)
                created_classes.append(c)
            self.stdout.write(self.style.SUCCESS(f'Создано/найдено {len(created_classes)} классов.'))

            # --- Teachers ---
            teachers = []
            for _ in range(12):
                t = Teacher.objects.create(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    cabinet=(str(random.randint(100, 500)) if random.random() > 0.2 else None)
                )
                if created_subjects:
                    chosen = random.sample(created_subjects, random.randint(1, min(3, len(created_subjects))))
                    if TeacherSubjectPeriod:
                        for subj in chosen:
                            TeacherSubjectPeriod.objects.create(
                                teacher=t,
                                subject=subj,
                                period=str(random.randint(2020, 2025))
                            )
                    else:
                        t.subjects.add(*chosen)
                teachers.append(t)
            self.stdout.write(self.style.SUCCESS(f'Создано {len(teachers)} учителей.'))

            # --- Students ---
            students = []
            for _ in range(80):
                cls = random.choice(created_classes)
                s = Student.objects.create(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    gender=random.choice(['M', 'F']),
                    school_class=cls
                )
                students.append(s)
            self.stdout.write(self.style.SUCCESS(f'Создано {len(students)} учеников.'))

            # --- Grades ---
            if created_subjects:
                created_grades = 0
                for student in students:
                    subjects_for_student = random.sample(created_subjects, min(4, len(created_subjects)))
                    for subj in subjects_for_student:
                        Grade.objects.create(
                            student=student,
                            subject=subj,
                            quarter=1,
                            value=round(random.uniform(2.0, 5.0), 1)
                        )
                        created_grades += 1
                self.stdout.write(self.style.SUCCESS(f'Создано {created_grades} оценок.'))

            # --- Lessons / Расписание ---
            # weekday: IntegerField (1=Monday, 5=Friday)
            weekdays = [1, 2, 3, 4, 5]
            if created_classes and created_subjects and teachers:
                lessons_created = 0
                for cls in created_classes:
                    for wd in weekdays:
                        for num in range(1, 6):  # 1..5 уроки
                            subj = random.choice(created_subjects)
                            teacher = random.choice(teachers)
                            Lesson.objects.create(
                                school_class=cls,
                                subject=subj,
                                teacher=teacher,
                                weekday=wd,
                                number=num
                            )
                            lessons_created += 1
                self.stdout.write(self.style.SUCCESS(f'Создано {lessons_created} уроков (расписание).'))

        self.stdout.write(self.style.SUCCESS('populate_db завершён.'))
