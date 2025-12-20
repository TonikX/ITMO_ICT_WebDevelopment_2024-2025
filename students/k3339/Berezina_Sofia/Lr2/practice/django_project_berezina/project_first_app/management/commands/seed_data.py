from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from project_first_app.models import Car, Ownership
from django.utils import timezone
from datetime import date, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем заполнение базы данных...')

        # Создаем пользователей (владельцев)
        users_data = [
            {
                'username': 'ivanov',
                'first_name': 'Иван',
                'last_name': 'Иванов',
                'email': 'ivanov@example.com',
                'passport_number': '4501123456',
                'home_address': 'г. Москва, ул. Ленина, д. 10, кв. 25',
                'nationality': 'Русский',
                'birth_date': date(1985, 5, 15)
            },
            {
                'username': 'petrova',
                'first_name': 'Мария',
                'last_name': 'Петрова', 
                'email': 'petrova@example.com',
                'passport_number': '4602987654',
                'home_address': 'г. Санкт-Петербург, Невский пр., д. 45, кв. 12',
                'nationality': 'Русская',
                'birth_date': date(1990, 8, 22)
            },
            {
                'username': 'sidorov',
                'first_name': 'Алексей',
                'last_name': 'Сидоров',
                'email': 'sidorov@example.com',
                'passport_number': '4711333444',
                'home_address': 'г. Екатеринбург, ул. Мира, д. 33, кв. 7',
                'nationality': 'Русский',
                'birth_date': date(1988, 3, 10)
            },
            {
                'username': 'kuznetsova',
                'first_name': 'Ольга',
                'last_name': 'Кузнецова',
                'email': 'kuznetsova@example.com',
                'passport_number': '4822555666',
                'home_address': 'г. Новосибирск, пр. Карла Маркса, д. 78, кв. 34',
                'nationality': 'Русская',
                'birth_date': date(1992, 11, 5)
            },
            {
                'username': 'smith',
                'first_name': 'Джон',
                'last_name': 'Смит',
                'email': 'smith@example.com',
                'passport_number': 'AB1234567',
                'home_address': 'г. Москва, ул. Тверская, д. 15, кв. 8',
                'nationality': 'Американец',
                'birth_date': date(1980, 12, 20)
            },
            {
                'username': 'kim',
                'first_name': 'Анна',
                'last_name': 'Ким',
                'email': 'kim@example.com',
                'passport_number': '123456789',
                'home_address': 'г. Владивосток, ул. Русская, д. 67, кв. 19',
                'nationality': 'Кореянка',
                'birth_date': date(1995, 7, 30)
            }
        ]

        users = []
        for user_data in users_data:
            user = User.objects.create_user(
                username=user_data['username'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password='testpass123',  # одинаковый пароль для всех тестовых пользователей
                passport_number=user_data['passport_number'],
                home_address=user_data['home_address'],
                nationality=user_data['nationality'],
                birth_date=user_data['birth_date']
            )
            users.append(user)
            self.stdout.write(f'Создан пользователь: {user}')

        # Создаем автомобили
        cars_data = [
            {'number': 'А123ВС77', 'brand': 'Toyota', 'model': 'Camry', 'color': 'Черный'},
            {'number': 'В456ОР78', 'brand': 'BMW', 'model': 'X5', 'color': 'Белый'},
            {'number': 'С789ТТ77', 'brand': 'Mercedes', 'model': 'E-Class', 'color': 'Серый'},
            {'number': 'Е001КХ77', 'brand': 'Kia', 'model': 'Rio', 'color': 'Красный'},
            {'number': 'М002АВ77', 'brand': 'Hyundai', 'model': 'Solaris', 'color': 'Синий'},
            {'number': 'Р003СТ77', 'brand': 'Skoda', 'model': 'Octavia', 'color': 'Зеленый'},
            {'number': 'У004ЕЕ77', 'brand': 'Lada', 'model': 'Vesta', 'color': 'Оранжевый'},
            {'number': 'Х005ММ77', 'brand': 'Volkswagen', 'model': 'Polo', 'color': 'Желтый'},
            {'number': 'Т006РР77', 'brand': 'Nissan', 'model': 'Qashqai', 'color': 'Фиолетовый'},
            {'number': 'О007СС77', 'brand': 'Audi', 'model': 'A4', 'color': 'Коричневый'}
        ]

        cars = []
        for car_data in cars_data:
            car = Car.objects.create(
                number=car_data['number'],
                brand=car_data['brand'],
                model=car_data['model'],
                color=car_data['color']
            )
            cars.append(car)
            self.stdout.write(f'Создан автомобиль: {car}')

        # Создаем связи владения (каждый пользователь владеет несколькими автомобилями)
        ownerships_data = [
            # Иванов владеет 3 автомобилями
            {'user': users[0], 'car': cars[0], 'start_date': date(2022, 1, 15)},
            {'user': users[0], 'car': cars[3], 'start_date': date(2023, 3, 10)},
            {'user': users[0], 'car': cars[6], 'start_date': date(2024, 1, 5)},
            
            # Петрова владеет 2 автомобилями
            {'user': users[1], 'car': cars[1], 'start_date': date(2021, 6, 20)},
            {'user': users[1], 'car': cars[4], 'start_date': date(2023, 8, 15)},
            
            # Сидоров владеет 2 автомобилями
            {'user': users[2], 'car': cars[2], 'start_date': date(2020, 11, 5)},
            {'user': users[2], 'car': cars[7], 'start_date': date(2023, 12, 1)},
            
            # Кузнецова владеет 2 автомобилями
            {'user': users[3], 'car': cars[5], 'start_date': date(2022, 9, 12)},
            {'user': users[3], 'car': cars[8], 'start_date': date(2024, 2, 20)},
            
            # Смит владеет 1 автомобилем
            {'user': users[4], 'car': cars[9], 'start_date': date(2023, 5, 30)},
            
            # Ким владеет 1 автомобилем (продала его)
            {'user': users[5], 'car': cars[0], 'start_date': date(2021, 1, 1), 'end_date': date(2022, 1, 14)},
        ]

        for ownership_data in ownerships_data:
            ownership = Ownership.objects.create(
                owner=ownership_data['user'],
                car=ownership_data['car'],
                start_date=ownership_data['start_date'],
                end_date=ownership_data.get('end_date')
            )
            self.stdout.write(f'Создано владение: {ownership}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно создано: {len(users)} пользователей, {len(cars)} автомобилей, {len(ownerships_data)} владений'
            )
        )