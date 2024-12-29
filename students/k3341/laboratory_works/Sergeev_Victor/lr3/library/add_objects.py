import random
from datetime import date
from library_app.models import *
from faker import Faker

fake = Faker(locale="ru_RU")
genres = ['comedy', 'drama', 'tragedy',
          'science fiction', 'technical literature', 'detective']
authors = ['Ivanov Ivan Ivanovich', 'Petrov Petr Petrovich',
           'Vasilyev Vasiliy Vasilyevich', 'Vetrov Victor Victorovich',
           'Fyodorov Fyodor Fyodorovich', 'Dmitrov Dmitriy Dmitriyevich']
book_titles = ['book_1', 'book_2', 'book_3', 'book_4', 'book_5',
               'book_6', 'book_7', 'book_8', 'book_9', 'book_10']
room_names = ['room_1', 'room_2', 'room_3', 'room_4', 'room_5', 'room_6']
room_capacities = [10, 20, 30, 40, 50, 60]
publishers = ['publisher_1', 'publisher_2', 'publisher_3']

def add_core_objects():
    for g in genres:
        i = Genre.objects.create(title=g)
        i.save()
    for a in authors:
        i = Author.objects.create(full_name=a)
        i.save()
    for n, c in zip(room_names, room_capacities):
        i = ReadingRoom.objects.create(name=n, capacity=c)
        i.save()

def add_books():
    for b in book_titles:
        p = random.choice(publishers)
        i = Book.objects.create(title=b,
                                publisher=p)
        i.save()
    genres = Genre.objects.all()
    authors = Author.objects.all()
    books = Book.objects.all()

    for b in books:
        i = random.randint(1, 4)
        j = random.randint(1, 4)
        g = random.choices(genres, i)
        a = random.choices(authors, j)
        for o in g:
            i = BookGenre.objects.create(book=b, genre=o)
            i.save()
        for o in a:
            i = BookAuthor.objects.create(book=b, author=o)
            i.save()
    
    for b in books:
        i = random.randint(2, 5)
        for _ in range(i):
            cipher = fake.pystr(min_chars=12, max_chars=12)
            a = BookCopy.objects.create(book=b, cipher=cipher, publisher_year=2024)
            a.save()

def add_readers(n: int):
    rooms = ReadingRoom.objects.all()
    education_types = ("н", "с", "в")

    for i in range(n):
        room = random.choice(rooms)
        education = random.choice(education_types)
        degree = (education == "в" and random.random() < 0.5)
        r = Reader.objects.create(full_name=fake.name(),
                                  passport_number=fake.passport_number(),
                                  birthdate=fake.date_of_birth(minimum_age=14, maximum_age=80),
                                  address=fake.address(),
                                  phone_number=fake.phone_number(),
                                  education=education,
                                  degree=degree,
                                  registration_date=fake.date_between(start_date='-1y'),
                                  reading_ticket_number=fake.pystr(min_chars=10, max_chars=10),
                                  reading_room=room)
        r.save()

def check_take_date(copy: BookCopy, take_date: date):
    last_take = BookTake.objects.filter(book_copy=copy).last()
    if last_take is None:
        return True
    if last_take.restore_date is None:
        print('wtf')
        return False
    if take_date >= last_take.restore_date:
        return True
    return False 

def add_booktakes(n: int):
    taken_pks = BookTake.objects.filter(restore_date=None).values_list('book_copy')
    taken_copies = list(BookCopy.objects.filter(id__in=taken_pks))
    free_copies = list(BookCopy.objects.exclude(id__in=taken_pks))
    readers = list(Reader.objects.all())

    i = 0
    for copy in taken_copies:
        if random.random() <= 0.5:
            continue
        take_line = BookTake.objects.get(book_copy=copy, restore_date=None)
        take_date = take_line.take_date

        restore_date = fake.date_between(start_date=take_date, end_date='today')
        take_line.restore_date = restore_date
        take_line.save()

        taken_copies.remove(copy)
        free_copies.append(copy)

    while i < n:
        if len(free_copies) == 0:
            print('no free copies. added books:', i)
            break
            
        copy = random.choice(free_copies)
        reader = random.choice(readers)
        take_date = fake.date_between(start_date=reader.registration_date, end_date='today')
        while True:
            if check_take_date(copy, take_date):
                break
            take_date = fake.date_between(start_date=reader.registration_date, end_date='today')

        new_take = BookTake.objects.create(book_copy=copy,
                                           reader=reader,
                                           take_date=take_date)
        
        new_take.save()
        if random.random() <= 0.5:
            i += 1
            free_copies.remove(copy)
            taken_copies.append(copy)
            continue

        restore_date = fake.date_between(start_date=take_date, end_date='today')
        new_take.restore_date = restore_date
        new_take.save()

        i += 1
