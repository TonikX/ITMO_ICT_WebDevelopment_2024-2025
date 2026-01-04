import os
import django
import random
from datetime import date, timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_project.settings')
django.setup()

from django.contrib.auth.models import User
from hotels.models import Hotel, Room, Amenity, Booking, Review
from faker import Faker

print("🧹 Очищаем старые данные...")
Booking.objects.all().delete()
Review.objects.all().delete()
Room.objects.all().delete()
Hotel.objects.all().delete()
Amenity.objects.all().delete()
User.objects.exclude(is_superuser=True).delete()

fake = Faker('ru_RU')  # Русские имена, города, адреса

# === 1. Пользователи ===
print("👤 Создаём пользователей...")
users = []
for i in range(5):
    username = f'user{i}'
    user = User.objects.create_user(
        username=username,
        email=f'{username}@example.com',
        password='test1234'
    )
    users.append(user)

# === 2. Удобства ===
print("🪟 Создаём удобства...")
amenity_names = [
    "Wi-Fi", "Телевизор", "Кондиционер", "Холодильник",
    "Балкон", "Фен", "Мини-бар", "Сейф", "Кофемашина", "Парковка"
]
amenities = [Amenity.objects.create(name=name) for name in amenity_names]

print("🏨 Создаём отели...")
hotels = []

hotel_prefixes = ["Grand", "Royal", "Sunny", "Crystal", "Imperial", "Golden", "Blue", "Green", "Luxury"]
hotel_suffixes = ["Hotel", "Inn", "Resort", "Suites", "Palace", "Lodge", "Retreat"]

for _ in range(5):
    owner = random.choice(users)

    # Генерация реалистичного названия отеля
    name = f"{random.choice(hotel_prefixes)} {random.choice(hotel_suffixes)}"

    # Генерация описания с логической связкой предложений
    description = (
        f"{name} расположен в прекрасном районе города. "
        f"Отель предлагает комфортабельные номера с современными удобствами. "
        f"Идеальное место для отдыха и деловых поездок. "
        f"{fake.sentence(nb_words=12)}"
    )

    h = Hotel.objects.create(
        name=name,
        owner=owner,
        address=fake.address(),
        description=description
    )
    hotels.append(h)

# === 4. Комнаты ===
print("🚪 Создаём комнаты...")
from hotels.models import ROOM_TYPES

rooms = []
room_type_keys = [rt[0] for rt in ROOM_TYPES]  # ['single', 'double', 'suite']

for hotel in hotels:
    for i in range(random.randint(3, 7)):
        room = Room.objects.create(
            hotel=hotel,
            number=str(random.randint(100, 999)),
            room_type=random.choice(room_type_keys),
            price=random.randint(2500, 9500),
        )
        room.amenities.add(*random.sample(amenities, k=2))
        rooms.append(room)


# === 5. Бронирования ===
print("📅 Создаём бронирования...")
for i in range(10):
    user = random.choice(users)
    room = random.choice(rooms)
    check_in = date.today() + timedelta(days=random.randint(1, 15))
    check_out = check_in + timedelta(days=random.randint(1, 5))
    Booking.objects.create(
        user=user,
        room=room,
        check_in=check_in,
        check_out=check_out,
        status=random.choice(['reserved', 'checked_in', 'checked_out'])
    )

# === 6. Отзывы ===
print("📝 Создаём отзывы...")
for i in range(10):
    user = random.choice(users)
    room = random.choice(rooms)
    stay_from = date.today() - timedelta(days=random.randint(20, 40))
    stay_to = stay_from + timedelta(days=random.randint(2, 6))
    Review.objects.create(
        user=user,
        room=room,
        stay_from=stay_from,
        stay_to=stay_to,
        rating=random.randint(6, 10),
        text=fake.sentence(nb_words=12)
    )

print("✅ База данных успешно заполнена!")
