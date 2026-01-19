from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from ...models import RacingUser, Team, Car, Racer, Race, RaceRegistration, Comment, RaceResult


class Command(BaseCommand):
    help = 'Fill database with test data'

    def handle(self, *args, **options):
        # Очистка существующих данных (опционально)
        # RacingUser.objects.all().delete()
        # Team.objects.all().delete()

        # Создание команд
        teams = [
            Team(name="Red Bull Racing", country="Austria", founded_date="2005-01-01"),
            Team(name="Ferrari", country="Italy", founded_date="1929-01-01"),
            Team(name="Mercedes AMG", country="Germany", founded_date="2010-01-01"),
            Team(name="McLaren", country="UK", founded_date="1963-01-01"),
            Team(name="Alpine", country="France", founded_date="2021-01-01"),
        ]

        # Используем bulk_create для эффективности
        Team.objects.bulk_create(teams)
        self.stdout.write(f'Created {len(teams)} teams')

        # Создание автомобилей
        cars = []
        car_models = [
            ("RB20", "F1", "Honda", 1050),
            ("SF-24", "F1", "Ferrari", 1040),
            ("W15", "F1", "Mercedes", 1035),
            ("MCL38", "F1", "Mercedes", 1030),
            ("A524", "F1", "Renault", 1025),
        ]

        for i, (model, car_class, engine, hp) in enumerate(car_models):
            cars.append(Car(
                model=model,
                team=teams[i],
                car_class=car_class,
                engine=engine,
                horsepower=hp
            ))

        Car.objects.bulk_create(cars)
        self.stdout.write(f'Created {len(cars)} cars')

        # Создание тестовых пользователей
        users_data = [
            ("max_verstappen", "Max", "Verstappen", "max@example.com", 8),
            ("charles_leclerc", "Charles", "Leclerc", "charles@example.com", 6),
            ("lewis_hamilton", "Lewis", "Hamilton", "lewis@example.com", 16),
            ("lando_norris", "Lando", "Norris", "lando@example.com", 5),
            ("fernando_alonso", "Fernando", "Alonso", "fernando@example.com", 20),
        ]

        users = []
        for username, first_name, last_name, email, experience in users_data:
            user = RacingUser(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                experience_years=experience
            )
            user.set_password("password123")  # Устанавливаем пароль
            users.append(user)

        RacingUser.objects.bulk_create(users)
        self.stdout.write(f'Created {len(users)} users')

        # Создание гонщиков
        racers = []
        racer_classes = ["Pro", "Pro", "Pro", "Semi-pro", "Pro"]
        license_numbers = ["FIA001", "FIA002", "FIA003", "FIA004", "FIA005"]

        for i, user in enumerate(users):
            racers.append(Racer(
                user=user,
                team=teams[i],
                racer_class=racer_classes[i],
                license_number=license_numbers[i],
                wins_count=random.randint(0, 50)
            ))

        Racer.objects.bulk_create(racers)
        self.stdout.write(f'Created {len(racers)} racers')

        # Создание гонок
        races = []
        race_data = [
            ("Гран-при Австралии", "Melbourne", "Main", 30),
            ("Гран-при Монако", "Monte Carlo", "Main", 15),
            ("Гран-при Италии", "Monza", "Main", 25),
            ("Гран-при Японии", "Suzuka", "Main", 20),
            ("Гран-при Абу-Даби", "Yas Marina", "Main", 10),
        ]

        base_date = timezone.now() + timedelta(days=10)
        for i, (name, location, race_type, days_offset) in enumerate(race_data):
            start_date = base_date + timedelta(days=i * 7)
            races.append(Race(
                name=name,
                race_type=race_type,
                location=location,
                start_date=start_date,
                end_date=start_date + timedelta(hours=3),
                description=f"Престижная гонка в {location}",
                is_active=True
            ))

        Race.objects.bulk_create(races)
        self.stdout.write(f'Created {len(races)} races')

        # Создание регистраций на гонки
        registrations = []
        for race in races:
            for racer in racers:
                if random.choice([True, False]):  # 50% chance to register
                    registrations.append(RaceRegistration(
                        racer=racer,
                        race=race,
                        car=random.choice(cars),
                        is_confirmed=random.choice([True, False])
                    ))

        RaceRegistration.objects.bulk_create(registrations)
        self.stdout.write(f'Created {len(registrations)} race registrations')

        # Создание комментариев
        comments = []
        comment_types = ["cooperation", "racing", "other"]

        for race in races[:3]:  # Комментарии только к первым 3 гонкам
            for user in users[:3]:  # Комментарии от первых 3 пользователей
                comments.append(Comment(
                    race=race,
                    author=user,
                    text=f"Отличная гонка в {race.location}! Жду не дождусь.",
                    comment_type=random.choice(comment_types),
                    rating=random.randint(7, 10)
                ))

        Comment.objects.bulk_create(comments)
        self.stdout.write(f'Created {len(comments)} comments')

        self.stdout.write(
            self.style.SUCCESS('Successfully filled database with comprehensive test data!')
        )