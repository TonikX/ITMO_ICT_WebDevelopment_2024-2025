import sqlite3
from datetime import date

# Создание базы данных
conn = sqlite3.connect('flights.db')
cursor = conn.cursor()

# Создание таблиц
cursor.execute('''CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT NOT NULL,
    airline TEXT NOT NULL,
    departure TEXT NOT NULL,
    arrival TEXT NOT NULL,
    flight_type TEXT NOT NULL,
    gate TEXT NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    flight_id INTEGER NOT NULL,
    seat_number TEXT NOT NULL,
    FOREIGN KEY (flight_id) REFERENCES flights (id)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_id INTEGER NOT NULL,
    user TEXT NOT NULL,
    date TEXT NOT NULL,
    text TEXT NOT NULL,
    rating INTEGER NOT NULL,
    FOREIGN KEY (flight_id) REFERENCES flights (id)
)''')

conn.commit()

# Функции для работы с базой данных
def add_flight(number, airline, departure, arrival, flight_type, gate):
    cursor.execute('''INSERT INTO flights (number, airline, departure, arrival, flight_type, gate)
                      VALUES (?, ?, ?, ?, ?, ?)''', (number, airline, departure, arrival, flight_type, gate))
    conn.commit()

def list_flights():
    cursor.execute('SELECT * FROM flights')
    return cursor.fetchall()

def add_reservation(user, flight_id, seat_number):
    cursor.execute('''INSERT INTO reservations (user, flight_id, seat_number)
                      VALUES (?, ?, ?)''', (user, flight_id, seat_number))
    conn.commit()

def list_reservations():
    cursor.execute('SELECT * FROM reservations')
    return cursor.fetchall()

def add_review(flight_id, user, review_date, text, rating):
    cursor.execute('''INSERT INTO reviews (flight_id, user, date, text, rating)
                      VALUES (?, ?, ?, ?, ?)''', (flight_id, user, review_date, text, rating))
    conn.commit()

def list_reviews():
    cursor.execute('SELECT * FROM reviews')
    return cursor.fetchall()

# Пример работы с базой данных
if __name__ == "__main__":
    # Добавление данных
    add_flight("SU123", "Aeroflot", "Moscow", "Paris", "departure", "A1")
    add_flight("BA456", "British Airways", "London", "New York", "arrival", "B2")

    add_reservation("john_doe", 1, "12A")
    add_reservation("jane_smith", 2, "14B")

    add_review(1, "john_doe", str(date.today()), "Great flight!", 9)
    add_review(2, "jane_smith", str(date.today()), "Very comfortable.", 8)

    # Список данных
    print("Flights:")
    for flight in list_flights():
        print(flight)

    print("\nReservations:")
    for reservation in list_reservations():
        print(reservation)

    print("\nReviews:")
    for review in list_reviews():
        print(review)

# Закрытие соединения
conn.close()
