import os
import django
import datetime
from django.utils import timezone

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Car, Owner, OwnerShip, License


def create_data():

    # Создание автомобилей
    cars = [
        Car(number="A123BC777", model="Camry", brand="Toyota", color="Black"),
        Car(number="B456DE123", model="X5", brand="BMW", color="White"),
        Car(number="C789FG456", model="Civic", brand="Honda", color="Red"),
        Car(number="E321HI789", model="Logan", brand="Renault", color="Blue"),
        Car(number="F654JK321", model="Focus", brand="Ford", color="Gray"),
        Car(number="X987YZ654", model="Solaris", brand="Hyundai", color="Silver"),
    ]

    for car in cars:
        car.save()

    print("Созданы автомобили:")
    for car in Car.objects.all():
        print(f"  - {car}")

    # Создание владельцев
    owners = [
        Owner(second_name="Иванов", first_name="Иван", birth_date=datetime.date(1990, 5, 15)),
        Owner(second_name="Петров", first_name="Петр", birth_date=datetime.date(1985, 8, 22)),
        Owner(second_name="Сидорова", first_name="Мария", birth_date=datetime.date(1992, 3, 10)),
        Owner(second_name="Кузнецов", first_name="Алексей", birth_date=datetime.date(1988, 11, 5)),
        Owner(second_name="Смирнов", first_name="Дмитрий", birth_date=datetime.date(1995, 7, 30)),
        Owner(second_name="Васильев", first_name="Сергей", birth_date=datetime.date(1980, 12, 18)),
        Owner(second_name="Николаева", first_name="Ольга", birth_date=datetime.date(1993, 9, 25)),
    ]

    for owner in owners:
        owner.save()

    print("\nСозданы владельцы:")
    for owner in Owner.objects.all():
        print(f"  - {owner}")

    # Создание водительских удостоверений
    licenses = [
        License(owner=owners[0], number="77AA123456", type="B", issue_date=datetime.date(2010, 6, 1)),
        License(owner=owners[1], number="77BB654321", type="BC", issue_date=datetime.date(2008, 3, 15)),
        License(owner=owners[2], number="77CC789012", type="B", issue_date=datetime.date(2012, 9, 20)),
        License(owner=owners[3], number="77DD345678", type="BCD", issue_date=datetime.date(2009, 1, 10)),
        License(owner=owners[4], number="77EE901234", type="B", issue_date=datetime.date(2015, 7, 5)),
        License(owner=owners[5], number="77FF567890", type="BC", issue_date=datetime.date(2005, 11, 30)),
        License(owner=owners[6], number="77GG112233", type="B", issue_date=datetime.date(2018, 4, 12)),
    ]

    for license_obj in licenses:
        license_obj.save()

    print("\nСозданы водительские удостоверения:")
    for license_obj in License.objects.all():
        print(f"  - {license_obj}")

    # Создание отношений владения автомобилями
    ownerships = [
        # Иванов владеет 2 автомобилями
        OwnerShip(owner=owners[0], car=cars[0], buy_date=datetime.date(2020, 1, 10),
                  sale_date=datetime.date(2023, 5, 20)),
        OwnerShip(owner=owners[0], car=cars[1], buy_date=datetime.date(2023, 6, 1)),

        # Петров владеет 1 автомобилем
        OwnerShip(owner=owners[1], car=cars[2], buy_date=datetime.date(2021, 3, 15)),

        # Сидорова владеет 3 автомобилями
        OwnerShip(owner=owners[2], car=cars[0], buy_date=datetime.date(2023, 5, 21)),
        OwnerShip(owner=owners[2], car=cars[3], buy_date=datetime.date(2022, 8, 10)),
        OwnerShip(owner=owners[2], car=cars[4], buy_date=datetime.date(2020, 12, 5),
                  sale_date=datetime.date(2023, 2, 28)),

        # Кузнецов владеет 2 автомобилями
        OwnerShip(owner=owners[3], car=cars[4], buy_date=datetime.date(2023, 3, 1)),
        OwnerShip(owner=owners[3], car=cars[5], buy_date=datetime.date(2021, 7, 20)),

        # Смирнов владеет 1 автомобилем
        OwnerShip(owner=owners[4], car=cars[1], buy_date=datetime.date(2019, 4, 10),
                  sale_date=datetime.date(2023, 5, 31)),

        # Васильев владеет 2 автомобилями
        OwnerShip(owner=owners[5], car=cars[2], buy_date=datetime.date(2018, 6, 15),
                  sale_date=datetime.date(2021, 2, 28)),
        OwnerShip(owner=owners[5], car=cars[5], buy_date=datetime.date(2020, 9, 1),
                  sale_date=datetime.date(2021, 6, 30)),

        # Николаева владеет 1 автомобилем
        OwnerShip(owner=owners[6], car=cars[3], buy_date=datetime.date(2021, 11, 15),
                  sale_date=datetime.date(2022, 7, 31)),
    ]

    for ownership in ownerships:
        ownership.save()

    print("\nСозданы отношения владения:")
    for ownership in OwnerShip.objects.all():
        sale_info = f" - продажа: {ownership.sale_date}" if ownership.sale_date else " (в собственности)"
        print(
            f"  - {ownership.owner.first_name} {ownership.owner.second_name} -> {ownership.car}: покупка: {ownership.buy_date}{sale_info}")

    # Вывод итоговой информации
    print("\n" + "=" * 50)
    print("ИТОГОВАЯ СТАТИСТИКА:")
    print(f"Всего автомобилей: {Car.objects.count()}")
    print(f"Всего владельцев: {Owner.objects.count()}")
    print(f"Всего удостоверений: {License.objects.count()}")
    print(f"Всего записей о владении: {OwnerShip.objects.count()}")

    print("\nАвтомобили по владельцам:")
    for owner in Owner.objects.all():
        cars_count = OwnerShip.objects.filter(owner=owner).count()
        current_cars = OwnerShip.objects.filter(owner=owner, sale_date__isnull=True)
        print(
            f"  {owner.first_name} {owner.second_name}: {cars_count} автомобилей, из них в собственности: {current_cars.count()}")


if __name__ == "__main__":
    create_data()