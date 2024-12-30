import random
from datetime import date
from library_app.models import *
from faker import Faker

fake = Faker()

def check_take_date(copy: BookCopy, take_date: date):
    last_take = BookTake.objects.filter(book=copy).last()
    if last_take is None:
        return True
    if last_take.restore_date is None:
        print('wtf')
        return False
    if take_date >= last_take.restore_date:
        return True
    return False 

def add_booktakes(n: int):
    taken_pks = BookTake.objects.filter(restore_date=None).values_list('book')
    taken_copies = list(BookCopy.objects.filter(id__in=taken_pks))
    free_copies = list(BookCopy.objects.exclude(id__in=taken_pks))
    readers = list(Reader.objects.all())

    i = 0
    for copy in taken_copies:
        if random.random() <= 0.5:
            continue
        take_line = BookTake.objects.get(book=copy, restore_date=None)
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

        new_take = BookTake.objects.create(book=copy,
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
