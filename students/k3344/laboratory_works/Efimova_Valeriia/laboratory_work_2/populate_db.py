import sqlite3
from random import randint, choice
from datetime import datetime, timedelta

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# iloveweb для админа (11111)
# password123 для сгенерированных юзеров
password_hash = 'pbkdf2_sha256$260000$OZ3UkWb1NJcUMppgyBV0Gp$vvTDF50K6YW7XwR8T4OBYnuwL1Y8sRcDR2Ufe6NUJJw='


def generate_users():
    first_names = ['Александр', 'Максим', 'Иван', 'Артем', 'Дмитрий', 'Николай', 'Сергей', 'Андрей', 'Екатерина', 'Мария', 'Анна', 'Ольга', 'Наталья', 'Елена']
    last_names = ['Иванов', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев', 'Петров', 'Соколов', 'Михайлов', 'Новиков', 'Федоров', 'Кравцов', 'Никитин', 'Соловьев', 'Борисов']
    patronymics = ['Александрович', 'Михайлович', 'Сергеевич', 'Владимирович', 'Николаевич', 'Иванович', 'Петрович', 'Андреевич', 'Алексеевич', 'Викторович', 'Юрьевич', 'Анатольевич']

    users = []
    for _ in range(10):
        first_name = choice(first_names)
        last_name = choice(last_names)
        patronymic = choice(patronymics)
        full_name = f"{last_name} {first_name} {patronymic}"
        passport_number = str(randint(10000, 99999))
        users.append((passport_number, password_hash, full_name))
    return users

def generate_flights():
    airlines = ['Аэрофлот', 'S7 Airlines', 'Уральские авиалинии', 'Победа', 'Россия']
    gates = [f"{chr(65 + i)}{j}" for i in range(6) for j in range(1, 5)]

    flights = []
    for _ in range(5):
        flight_number = str(randint(1000, 9999))
        airline = choice(airlines)
        departure_datetime = datetime.now() + timedelta(days=randint(1, 10))
        arrival_datetime = departure_datetime + timedelta(hours=randint(1, 5))
        gate_number = choice(gates)
        flights.append((flight_number, airline, departure_datetime.strftime('%Y-%m-%d %H:%M:%S'), arrival_datetime.strftime('%Y-%m-%d %H:%M:%S'), gate_number))
    return flights

def generate_bookings(users, flights):
    bookings = []
    for user in users:
        flight = choice(flights)
        booking_number = str(randint(100, 999))
        ticket_number = f"TKT{randint(100000, 999999)}"
        bookings.append((user[0], flight[0], booking_number, ticket_number))
    return bookings

def generate_reviews(bookings):
    review_texts = [
        'Отличный полет, все прошло хорошо.',
        'Задержали рейс на час.',
        'Экипаж был очень дружелюбен.',
        'Плохое обслуживание на борту.',
        'Очень комфортные сидения.',
        'Еда оставляет желать лучшего.',
        'Быстрая регистрация и посадка.',
        'Не понравилась турбулентность.',
        'Прекрасный вид из окна.',
        'Обязательно полечу снова с этой авиакомпанией.'
    ]

    reviews = []
    for booking in bookings:
        rating = randint(1, 10)
        text = choice(review_texts)
        review_date = datetime.now().strftime('%Y-%m-%d')
        reviews.append((booking[2], review_date, text, rating))
    return reviews


users = generate_users()
flights = generate_flights()
bookings = generate_bookings(users, flights)
reviews = generate_reviews(bookings)

try:
    for user in users:
        passport_number, password, full_name = user
        cursor.execute('''
            INSERT INTO flights_app_user (passport_number, password, full_name, is_active, is_staff, is_superuser)
            VALUES (?, ?, ?, 1, 0, 0)
        ''', (passport_number, password, full_name))

    for flight in flights:
        flight_number, airline, departure_datetime, arrival_datetime, gate_number = flight
        cursor.execute('''
            INSERT INTO flights_app_flight (flight_number, airline, departure_datetime, arrival_datetime, gate_number)
            VALUES (?, ?, ?, ?, ?)
        ''', (flight_number, airline, departure_datetime, arrival_datetime, gate_number))

    for booking in bookings:
        user_passport, flight_number, booking_number, ticket_number = booking
        cursor.execute('''
            INSERT INTO flights_app_booking (user_id, flight_id, booking_number, ticket_number)
            VALUES (?, ?, ?, ?)
        ''', (user_passport, flight_number, booking_number, ticket_number))

    for review in reviews:
        booking_number, review_date, text, rating = review
        cursor.execute('''
            SELECT id FROM flights_app_booking WHERE booking_number=?
        ''', (booking_number,))
        booking_id = cursor.fetchone()[0]
        cursor.execute('''
            INSERT INTO flights_app_review (booking_id, review_date, text, rating)
            VALUES (?, ?, ?, ?)
        ''', (booking_id, review_date, text, rating))

    conn.commit()
    print("База данных успешно заполнена!")
except Exception as e:
    print("Произошла ошибка:", e)
    conn.rollback()
finally:
    conn.close()
