## **Задание 3.1:**

```python
Owner(last_name="Мавзовин", first_name="Петр", birth_date="2003-07-12").save()
Owner(last_name="Ребров", first_name="Сергей", birth_date="2003-12-08").save()
Owner(last_name="Иванов", first_name="Алексей", birth_date="2004-03-15").save()
Owner(last_name="Смирнова", first_name="Анна", birth_date="2003-11-22").save()
Owner(last_name="Кузнецов", first_name="Дмитрий", birth_date="2004-01-30").save()
Owner(last_name="Петрова", first_name="Мария", birth_date="2003-05-18").save()

Car(number="Н072ЕМ", mark="BMW", model="M3", color="Красный").save()
Car(number="А123ВС", mark="Audi", model="R8", color="Синий").save()
Car(number="М456ОР", mark="Mercedes", model="C-Class", color="Белый").save()
Car(number="К789ТС", mark="Toyota", model="Camry", color="Черный").save()
Car(number="Р321НО", mark="Lexus", model="RX 350", color="Серый").save()

License(owner=Owner.objects.get(id=1), number="7715123456", type="private", date="2024-07-13").save()
License(owner=Owner.objects.get(id=2), number="1234351234", type="private", date="2023-08-13").save()
License(owner=Owner.objects.get(id=3), number="5033123456", type="commercial", date="2023-05-20").save()
License(owner=Owner.objects.get(id=4), number="3412987654", type="private", date="2022-09-15").save()
License(owner=Owner.objects.get(id=5), number="7800456789", type="special", date="2024-01-10").save()
License(owner=Owner.objects.get(id=6), number="4612345678", type="private", date="2023-03-25").save()

CarOwner(owner=Owner.objects.get(id=1), car=Car.objects.get(id=1), start_date="2020-10-10", end_date="2021-10-09").save()
CarOwner(owner=Owner.objects.get(id=1), car=Car.objects.get(id=2), start_date="2020-11-10").save()
CarOwner(owner=Owner.objects.get(id=1), car=Car.objects.get(id=3), start_date="2020-12-10").save()
CarOwner(owner=Owner.objects.get(id=2), car=Car.objects.get(id=2), start_date="2020-11-10").save()
CarOwner(owner=Owner.objects.get(id=3), car=Car.objects.get(id=5), start_date="2021-09-13").save()
CarOwner(owner=Owner.objects.get(id=4), car=Car.objects.get(id=4), start_date="2024-05-02").save()
CarOwner(owner=Owner.objects.get(id=5), car=Car.objects.get(id=1), start_date="2021-10-09").save()
CarOwner(owner=Owner.objects.get(id=6), car=Car.objects.get(id=4), start_date="2024-05-02").save()

Owner.objects.all()
Car.objects.all()
License.objects.all()
CarOwner.objects.all()
```

## **Задание 3.2:**

```python
Car.objects.filter(mark="Toyota")
Owner.objects.filter(first_name="Петр")
License.objects.filter(owner=Owner.objects.get(id=2))
Owner.objects.filter(car_owner__car__color="Красный")
Owner.objects.filter(car_owner__start_date__gte="2021-01-01")
```

## **Задание 3.3:**

```python
License.objects.aggregate(max_date=Max("date"))
CarOwner.objects.aggregate(max_date=Max("end_date"))
[[owner, owner.cars] for owner in Owner.objects.annotate(cars=Count("car_owner__car__id"))]
Car.objects.values("mark").annotate(Count("id"))
Owner.objects.order_by("license_owner__date")
```