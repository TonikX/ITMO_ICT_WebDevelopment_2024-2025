import os
import sys
from datetime import datetime
from django.utils.timezone import make_aware
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_django_web_project.settings')
django.setup()

from project_first_app.models import CarOwner

def add_olegs():
    birth_date_1 = make_aware(datetime(1990, 5, 20))
    birth_date_2 = make_aware(datetime(1985, 8, 15))
    birth_date_3 = make_aware(datetime(1995, 12, 30))

    oleg1 = CarOwner.objects.create_user(
        username="Oleg_Vladinirov", 
        passport_number="PN101_123", 
        home_address="Moscow", 
        nationality="Russian", 
        birth_date=birth_date_1
    )

    oleg2 = CarOwner.objects.create_user(
        username="Oleg_Fedorov", 
        passport_number="PN102_456", 
        home_address="Saint Petersburg", 
        nationality="Russian", 
        birth_date=birth_date_2
    )

    oleg3 = CarOwner.objects.create_user(
        username="Oleg_Panchin", 
        passport_number="PN003_789", 
        home_address="Novosibirsk", 
        nationality="Russian", 
        birth_date=birth_date_3
    )

    print("Added Olegs:")
    for oleg in [oleg1, oleg2, oleg3]:
        print(f"Username: {oleg.username}, Passport: {oleg.passport_number}, Address: {oleg.home_address}, Birth Date: {oleg.birth_date}")

if __name__ == "__main__":
    add_olegs()
