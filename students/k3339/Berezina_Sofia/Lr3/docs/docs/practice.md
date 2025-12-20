# Практическая работа

## Практическая часть 3.1

`Задание № 1:`

Воспользуйтесь проектом из практики 2.1:

![Снимок экрана 2025-11-25 в 14.16.06.png](%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-11-25%20%D0%B2%2014.16.06.png)
Напишите запрос на создание 6-7 новых автовладельцев и 5-6 автомобилей, каждому автовладельцу назначьте удостоверение и от 1 до 3 автомобилей. Задание можете выполнить либо в интерактивном режиме интерпретатора, либо в отдельном python-файле. Результатом должны стать запросы и отображение созданных объектов. 
Если вы добавляете автомобили владельцу через метод .add(), не забудьте заполнить также ассоциативную сущность “владение”

1. Создаем БД

```python
from django.db import models

# Create your models here.
class Car(models.Model):
    number = models.CharField(max_length=15, unique=True)
    model = models.CharField(max_length=20)
    brand = models.CharField(max_length=20, )
    color = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.number})"

class Owner(models.Model):
    second_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.second_name} {self.first_name} {self.birth_date}"

class OwnerShip(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    buy_date = models.DateField()
    sale_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.owner} {self.car} {self.buy_date} {self.sale_date}"

class License(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    number = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=10)
    issue_date = models.DateField()

    def __str__(self):
        return f"{self.owner} {self.number} {self.type} {self.issue_date}"
```

2. Создаем файл для заполнения данными

```python
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
```

`Задание № 2:`

По созданным в пр.1 данным написать следующие запросы на фильтрацию:

- Где это необходимо, добавьте related_name к полям модели
- Выведете все машины марки “Toyota” (или любой другой марки, которая у вас есть)
- Найти всех водителей с именем “Олег” (или любым другим именем на ваше усмотрение)
- Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта модели (можно в 2 запроса)
- Вывести всех владельцев красных машин (или любого другого цвета, который у вас присутствует)
- Найти всех владельцев, чей год владения машиной начинается с 2010 (или любой другой год, который присутствует у вас в базе)

1. Выполнение запросов

```python
# 1. Машины Toyota
Car.objects.filter(brand="Toyota")
<QuerySet [<Car: Toyota Camry (A123BC777)>]>
```
```python
# 2. Владельцы с именем Иван
Owner.objects.filter(first_name="Иван")
<QuerySet [<Owner: Иванов Иван 1990-05-15>]>
```
```python
# 3. Удостоверение случайного владельца
import random
owners = list(Owner.objects.all())
owner = random.choice(owners)
License.objects.get(owner_id=owner.id)
<License: Смирнов Дмитрий 1995-07-30 77EE901234 B 2015-07-05>
```
```python
# 4. Владельцы красных машин
 Owner.objects.filter(ownership__car__color="Red").distinct()
<QuerySet [<Owner: Петров Петр 1985-08-22>, <Owner: Васильев Сергей 1980-12-18>]>
```
```python
# 5. Владельцы с 2020 года
Owner.objects.filter(ownership__buy_date__year__gte=2020).distinct()
<QuerySet [<Owner: Иванов Иван 1990-05-15>, <Owner: Петров Петр 1985-08-22>, <Owner: Сидорова Мария 1992-03-10>, <Owner: Кузнецов Алексей 1988-11-05>, <Owner: Васильев Сергей 1980-12-18>, <Owner: Николаева Ольга 1993-09-25>]>
```

`Задание № 3:`

Необходимо реализовать следующие запросы c применением описанных методов:

- Вывод даты выдачи самого старшего водительского удостоверения
- Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе
- Выведите количество машин для каждого водителя
- Подсчитайте количество машин каждой марки
- Отсортируйте всех автовладельцев по дате выдачи удостоверения (Примечание: чтобы не выводить несколько раз одни и те же записи воспользуйтесь методом .distinct()

  1. Выполнение запросов

```python
# 1. Вывод даты выдачи самого старшего водительского удостоверения
from django.db.models import Min, Max, Count, Avg
License.objects.aggregate(oldest_date=Min('issue_date'))['oldest_date']
datetime.date(2005, 11, 30)
```

```python
# 2. Самая поздняя дата владения машиной для существующих моделей
OwnerShip.objects.aggregate(latest_date=Max('buy_date'))['latest_date']
datetime.date(2023, 6, 1)
```

```python
# 3. Количество машин для каждого водителя
owners_with_car_count = Owner.objects.annotate(car_count=Count('ownership'))
for owner in owners_with_car_count:
    print(f"   {owner.first_name} {owner.second_name}: {owner.car_count} машин(ы)")
... 
   Иван Иванов: 2 машин(ы)
   Петр Петров: 1 машин(ы)
   Мария Сидорова: 3 машин(ы)
   Алексей Кузнецов: 2 машин(ы)
   Дмитрий Смирнов: 1 машин(ы)
   Сергей Васильев: 2 машин(ы)
   Ольга Николаева: 1 машин(ы)
```

```python
# 4. Количество машин по маркам
brands = Car.objects.values('brand').annotate(total=Count('id'))
for brand in brands:
    print(f"   {brand['brand']}: {brand['total']}")
... 
   BMW: 1
   Ford: 1
   Honda: 1
   Hyundai: 1
   Renault: 1
   Toyota: 1
```

```python
# 5. Владельцы по дате удостоверения
owners_sorted = Owner.objects.filter(license__isnull=False).annotate(license_date=Min('license__issue_date')).order_by('license_date').distinct()
for owner in owners_sorted:
    print(f"   {owner.first_name} {owner.second_name}: {owner.license_date}")
... 
   Сергей Васильев: 2005-11-30
   Петр Петров: 2008-03-15
   Алексей Кузнецов: 2009-01-10
   Иван Иванов: 2010-06-01
   Мария Сидорова: 2012-09-20
   Дмитрий Смирнов: 2015-07-05
   Ольга Николаева: 2018-04-12
```

## Практическая часть 3.2

`Задание № 1:`

Реализовать ендпоинты для добавления и просмотра скилов методом, описанным в пункте выше.

В `serializers.py`:

```python
from rest_framework import serializers
from .models import *


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"

class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"
```

В `views.py`:

```python
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SkillSerializer, WarriorSerializer
from .models import Warrior, Skill


# Create your views here.
class WarriorAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


# Эндпоинты для умений (скилов)
class SkillAPIView(APIView):
    # GET - просмотр всех скилов
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})

    # POST - добавление нового скила
    def post(self, request):
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

В `urls.py`:

```python
from django.urls import path
from .views import *


app_name = "warriors_app"


urlpatterns = [
    path('warriors/', WarriorAPIView.as_view(), name='warriors'),
    path('skills/', SkillAPIView.as_view(), name='skills'),  # Новый эндпоинт для скилов
]
```

Получаем:

![Снимок экрана 2025-11-25 в 22.30.38.png](%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-11-25%20%D0%B2%2022.30.38.png)
![Снимок экрана 2025-11-25 в 22.30.54.png](%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-11-25%20%D0%B2%2022.30.54.png)
![Снимок экрана 2025-11-25 в 22.31.02.png](%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-11-25%20%D0%B2%2022.31.02.png)


`Задание № 2:`

Реализовать ендпоинты:
- Вывод полной информации о всех войнах и их профессиях (в одном запросе).
- Вывод полной информации о всех войнах и их скилах (в одном запросе).
- Вывод полной информации о войне (по id), его профессиях и скилах.
- Удаление война по id.
- Редактирование информации о войне.


В `serializers.py`:

```python
class ProfessionNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ["id", "title", "description"]


class SkillNestedSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = ["id", "title", "level"]

    def get_level(self, obj):
        # Получаем уровень умения для конкретного воина
        warrior = self.context.get('warrior')
        if warrior:
            try:
                skill_of_warrior = SkillOfWarrior.objects.get(warrior=warrior, skill=obj)
                return skill_of_warrior.level
            except SkillOfWarrior.DoesNotExist:
                return None
        return None


# 1. Воины с профессиями
class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionNestedSerializer(read_only=True)
    race = serializers.CharField(source='get_race_display')

    class Meta:
        model = Warrior
        fields = ["id", "name", "race", "level", "profession"]


# 2. Воины со скилами
class WarriorSkillsSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    race = serializers.CharField(source='get_race_display')

    class Meta:
        model = Warrior
        fields = ["id", "name", "race", "level", "skills"]

    def get_skills(self, obj):
        skills = obj.skill.all()
        return SkillNestedSerializer(skills, many=True, context={'warrior': obj}).data


# 3. Полная информация о воине
class WarriorFullSerializer(serializers.ModelSerializer):
    profession = ProfessionNestedSerializer(read_only=True)
    skills = serializers.SerializerMethodField()
    race = serializers.CharField(source='get_race_display')

    class Meta:
        model = Warrior
        fields = ["id", "name", "race", "level", "profession", "skills"]

    def get_skills(self, obj):
        skills = obj.skill.all()
        return SkillNestedSerializer(skills, many=True, context={'warrior': obj}).data


# 4. Сериализатор для редактирования воина
class WarriorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = ["name", "race", "level", "profession"]
```

В `views.py`:

```python
# 1. Вывод всех воинов с их профессиями
class WarriorProfessionListAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.select_related('profession').all()
        serializer = WarriorProfessionSerializer(warriors, many=True)
        return Response({
            "count": warriors.count(),
            "warriors": serializer.data
        })


# 2. Вывод всех воинов с их скилами
class WarriorSkillsListAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.prefetch_related('skill').all()
        serializer = WarriorSkillsSerializer(warriors, many=True)
        return Response({
            "count": warriors.count(),
            "warriors": serializer.data
        })


# 3. Вывод полной информации о воине по ID
class WarriorDetailAPIView(APIView):
    def get(self, request, pk):
        warrior = get_object_or_404(Warrior.objects.prefetch_related('skill'), pk=pk)
        serializer = WarriorFullSerializer(warrior)
        return Response(serializer.data)


# 4. Удаление воина по ID
class WarriorDeleteAPIView(APIView):
    def delete(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        warrior_name = warrior.name
        warrior.delete()
        return Response(
            {"message": f"Воин {warrior_name} успешно удален"},
            status=status.HTTP_204_NO_CONTENT
        )


# 5. Редактирование информации о воине
class WarriorUpdateAPIView(APIView):
    def get(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        serializer = WarriorFullSerializer(warrior)
        return Response(serializer.data)

    def put(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        serializer = WarriorUpdateSerializer(warrior, data=request.data)

        if serializer.is_valid():
            serializer.save()
            # Возвращаем обновленные данные
            updated_warrior = Warrior.objects.get(pk=pk)
            full_serializer = WarriorFullSerializer(updated_warrior)
            return Response({
                "message": "Информация о воине успешно обновлена",
                "warrior": full_serializer.data
            })

        return Response(
            {"error": "Ошибка валидации", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        serializer = WarriorUpdateSerializer(warrior, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            # Возвращаем обновленные данные
            updated_warrior = Warrior.objects.get(pk=pk)
            full_serializer = WarriorFullSerializer(updated_warrior)
            return Response({
                "message": "Информация о воине успешно обновлена",
                "warrior": full_serializer.data
            })

        return Response(
            {"error": "Ошибка валидации", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
```

В `urls.py`:

```python
urlpatterns = [
    path('warriors/', WarriorAPIView.as_view(), name='warriors'),
    path('skills/', SkillAPIView.as_view(), name='skills'),
    path('warriors/professions/', WarriorProfessionListAPIView.as_view(), name='warriors-professions'),
    path('warriors/skills/', WarriorSkillsListAPIView.as_view(), name='warriors-skills'),
    path('warriors/<int:pk>/', WarriorDetailAPIView.as_view(), name='warrior-detail'),
    path('warriors/<int:pk>/delete/', WarriorDeleteAPIView.as_view(), name='warrior-delete'),
    path('warriors/<int:pk>/update/', WarriorUpdateAPIView.as_view(), name='warrior-update'),
]
```