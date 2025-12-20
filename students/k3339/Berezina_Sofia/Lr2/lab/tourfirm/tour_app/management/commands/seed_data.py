import os
import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tour_app.models import Tour, Reservation, Review

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **options):
        self.stdout.write('Создание тестовых данных...')
        
        # Очищаем существующие данные (опционально)
        User.objects.filter(username__in=['alex_ivanov', 'maria_petrova', 'serg_sidorov', 'olga_kuznetsova', 'admin_user']).delete()
        Tour.objects.all().delete()
        
        # Создаем пользователей
        users_data = [
            {'username': 'alex_ivanov', 'email': 'alex@mail.com', 'password': 'password123'},
            {'username': 'maria_petrova', 'email': 'maria@mail.com', 'password': 'password123'},
            {'username': 'serg_sidorov', 'email': 'serg@mail.com', 'password': 'password123'},
            {'username': 'olga_kuznetsova', 'email': 'olga@mail.com', 'password': 'password123'},
            {'username': 'admin_user', 'email': 'admin@mail.com', 'password': 'admin123', 'is_staff': True},
        ]
        
        users = {}
        for user_data in users_data:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                is_staff=user_data.get('is_staff', False)
            )
            users[user_data['username']] = user
            self.stdout.write(f'Создан пользователь: {user.username}')

        # Создаем туры
        tours_data = [
            {
                'title': 'Отдых в Турции: Все включено',
                'agency': 'ТурЭкспресс',
                'country': 'Турция',
                'description': 'Прекрасный отдых на побережье Средиземного моря. Отели 5*, система все включено, экскурсии к историческим местам.',
                'start_date': datetime.now().date() + timedelta(days=30),
                'end_date': datetime.now().date() + timedelta(days=37),
                'payment_conditions': 'Предоплата 30% при бронировании, остальное за 14 дней до вылета',
                'price': 45000
            },
            {
                'title': 'Горнолыжный курорт в Альпах',
                'agency': 'АльпТур',
                'country': 'Франция',
                'description': 'Катание на лучших склонах Альп. Проживание в шале, питание полупансион, прокат оборудования.',
                'start_date': datetime.now().date() + timedelta(days=45),
                'end_date': datetime.now().date() + timedelta(days=52),
                'payment_conditions': 'Полная оплата за 21 день до начала тура',
                'price': 78000
            },
            {
                'title': 'Экскурсионный тур по Италии',
                'agency': 'ЕвроТур',
                'country': 'Италия',
                'description': 'Рим, Флоренция, Венеция. Посещение главных достопримечательностей, гастрономические туры, винные дегустации.',
                'start_date': datetime.now().date() + timedelta(days=60),
                'end_date': datetime.now().date() + timedelta(days=67),
                'payment_conditions': 'Рассрочка: 3 платежа',
                'price': 62000
            },
            {
                'title': 'Пляжный отдых в Таиланде',
                'agency': 'АзияТур',
                'country': 'Таиланд',
                'description': 'Отдых на островах Пхукет и Пхи-Пхи. Дайвинг, экскурсии к храмам, тайский массач, национальная кухня.',
                'start_date': datetime.now().date() + timedelta(days=75),
                'end_date': datetime.now().date() + timedelta(days=85),
                'payment_conditions': 'Предоплата 50%, остальное за 30 дней',
                'price': 55000
            },
            {
                'title': 'Культурный тур по Японии',
                'agency': 'ВостокТур',
                'country': 'Япония',
                'description': 'Токио, Киото, Осака. Сакура, древние храмы, современные технологии, мастер-классы по суши.',
                'start_date': datetime.now().date() + timedelta(days=90),
                'end_date': datetime.now().date() + timedelta(days=100),
                'payment_conditions': 'Полная предоплата за 45 дней',
                'price': 89000
            },
            {
                'title': 'Отдых в Сочи',
                'agency': 'РусТур',
                'country': 'Россия',
                'description': 'Комфортабельные отели, экскурсии в горы, дегустации вин, посещение Олимпийского парка.',
                'start_date': datetime.now().date() + timedelta(days=15),
                'end_date': datetime.now().date() + timedelta(days=22),
                'payment_conditions': 'Оплата при бронировании',
                'price': 35000
            },
            {
                'title': 'Экзотика Бали',
                'agency': 'ЭкзоТур',
                'country': 'Индонезия',
                'description': 'Райские пляжи, серфинг, йога-туры, древние храмы, рисовые террасы.',
                'start_date': datetime.now().date() + timedelta(days=120),
                'end_date': datetime.now().date() + timedelta(days=135),
                'payment_conditions': 'Рассрочка на 2 платежа',
                'price': 68000
            }
        ]

        tours = {}
        for tour_data in tours_data:
            tour = Tour.objects.create(**tour_data)
            tours[tour_data['title']] = tour
            self.stdout.write(f'Создан тур: {tour.title}')

        # Создаем резервирования
        reservations_data = [
            # Подтвержденные резервирования
            {'user': 'alex_ivanov', 'tour': 'Отдых в Турции: Все включено', 'status': 'confirmed', 'notes': 'Хочу номер с видом на море'},
            {'user': 'maria_petrova', 'tour': 'Горнолыжный курорт в Альпах', 'status': 'confirmed', 'notes': 'Нужен инструктор для начинающих'},
            {'user': 'serg_sidorov', 'tour': 'Экскурсионный тур по Италии', 'status': 'confirmed', 'notes': 'Вегетарианское питание'},
            {'user': 'olga_kuznetsova', 'tour': 'Пляжный отдых в Таиланде', 'status': 'confirmed', 'notes': 'Трансфер из аэропорта'},
            
            # Ожидающие подтверждения
            {'user': 'alex_ivanov', 'tour': 'Культурный тур по Японии', 'status': 'pending', 'notes': 'Интересуюсь экскурсиями'},
            {'user': 'maria_petrova', 'tour': 'Отдых в Сочи', 'status': 'pending', 'notes': 'Уточнить наличие мест'},
            {'user': 'serg_sidorov', 'tour': 'Экзотика Бали', 'status': 'pending', 'notes': 'Групповая поездка'},
            
            # Отмененные
            {'user': 'olga_kuznetsova', 'tour': 'Горнолыжный курорт в Альпах', 'status': 'cancelled', 'notes': 'Изменение планов'},
        ]

        for res_data in reservations_data:
            user = users[res_data['user']]
            tour = tours[res_data['tour']]
            
            reservation = Reservation.objects.create(
                user=user,
                tour=tour,
                status=res_data['status'],
                notes=res_data['notes']
            )
            self.stdout.write(f'Создано резервирование: {user.username} - {tour.title}')

        # Создаем отзывы
        reviews_data = [
            {
                'user': 'alex_ivanov',
                'tour': 'Отдых в Турции: Все включено',
                'text': 'Отличный отель, вкусная еда, прекрасный сервис. Обязательно поеду еще раз!',
                'rating': 9,
                'tour_start_date': datetime.now().date() - timedelta(days=60),
                'tour_end_date': datetime.now().date() - timedelta(days=53)
            },
            {
                'user': 'maria_petrova',
                'tour': 'Горнолыжный курорт в Альпах',
                'text': 'Великолепные склоны, профессиональные инструкторы. Немного дороговато, но стоит того.',
                'rating': 8,
                'tour_start_date': datetime.now().date() - timedelta(days=45),
                'tour_end_date': datetime.now().date() - timedelta(days=38)
            },
            {
                'user': 'serg_sidorov',
                'tour': 'Экскурсионный тур по Италии',
                'text': 'Очень насыщенная программа, немного устали, но впечатления незабываемые. Гиды отличные!',
                'rating': 9,
                'tour_start_date': datetime.now().date() - timedelta(days=30),
                'tour_end_date': datetime.now().date() - timedelta(days=23)
            },
            {
                'user': 'olga_kuznetsova',
                'tour': 'Пляжный отдых в Таиланде',
                'text': 'Райское место! Отличные пляжи, море теплое. Единственное - долгий перелет.',
                'rating': 10,
                'tour_start_date': datetime.now().date() - timedelta(days=75),
                'tour_end_date': datetime.now().date() - timedelta(days=65)
            },
            {
                'user': 'alex_ivanov',
                'tour': 'Экзотика Бали',
                'text': 'Не понравилось обслуживание в отеле. Природа прекрасная, но сервис хромает.',
                'rating': 6,
                'tour_start_date': datetime.now().date() - timedelta(days=90),
                'tour_end_date': datetime.now().date() - timedelta(days=75)
            },
            {
                'user': 'maria_petrova',
                'tour': 'Отдых в Сочи',
                'text': 'Хороший отдых за свои деньги. Погода была не очень, но развлечений хватало.',
                'rating': 7,
                'tour_start_date': datetime.now().date() - timedelta(days=15),
                'tour_end_date': datetime.now().date() - timedelta(days=8)
            }
        ]

        for review_data in reviews_data:
            user = users[review_data['user']]
            tour = tours[review_data['tour']]
            
            review = Review.objects.create(
                user=user,
                tour=tour,
                text=review_data['text'],
                rating=review_data['rating'],
                tour_start_date=review_data['tour_start_date'],
                tour_end_date=review_data['tour_end_date']
            )
            self.stdout.write(f'Создан отзыв: {user.username} - {tour.title} - {review_data["rating"]}/10')

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно создано:\n'
                f'- Пользователей: {len(users)}\n'
                f'- Туров: {len(tours)}\n'
                f'- Резервирований: {Reservation.objects.count()}\n'
                f'- Отзывов: {Review.objects.count()}'
            )
        )