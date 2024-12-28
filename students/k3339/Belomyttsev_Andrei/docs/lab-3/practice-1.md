# Практическая работа №3.1

## Задание

Цель работы: получить представление о работе с запросами в Django ORM.

Необходимо выполнить все задания с пометкой **Практическое задание** [из практической работы №3.1] (https://docs.google.com/document/d/1jB8EYOWk-bbjB6sLr1s7dOmLYRC9Z5jIV6xIpnigdvY/edit?usp=sharing).

Полученную программу залить в папку этого репозитория **sutdents/группа/practical_works/фамилия_имя/simple_drf_project**. 

Инструкция о загрузке работы ниже. Не забывайте о файле gitignore.

**Сдача практический работы №3.1**: Оформить, как часть документации все задания с пометкой "практическая работа" и сдать Сергею.

## Code

```python
>>> from project_first_app.models import *
>>> from datetime import datetime, timedelta
>>> import random
>>> 
>>> Owner.objects.create(last_name='Musk', first_name='Elon', date_of_birth='1971-06-28')
<Owner: Elon Musk>
>>> Owner.objects.create(last_name='Zuckerberg', first_name='Mark', date_of_birth='1984-05-14')
<Owner: Mark Zuckerberg>
>>> Owner.objects.create(last_name='Stark', first_name='Tony', date_of_birth='1970-05-29')
<Owner: Tony Stark>
>>> Owner.objects.create(last_name='Bezos', first_name='Jeff', date_of_birth='1964-01-12')
<Owner: Jeff Bezos>
>>> Owner.objects.create(last_name='Gates', first_name='Bill', date_of_birth='1955-10-28')
<Owner: Bill Gates>
>>> Owner.objects.create(last_name='Trump', first_name='Donald', date_of_birth='1946-06-14')
<Owner: Donald Trump>
>>> 
>>> Car.objects.create(number='TIIIME', brand='DeLorean', model='DMC-12', color='Silver')
<Car: TIIIME, DeLorean, DMC-12>
>>> Car.objects.create(number='AUTOBOT', brand='Chevrolet', model='Camaro', color='Yellow')
<Car: AUTOBOT, Chevrolet, Camaro>
>>> Car.objects.create(number='BATMAN', brand='Wayne Enterprises', model='Batmobile', color='Black')
<Car: BATMAN, Wayne Enterprises, Batmobile>
>>> Car.objects.create(number='CYBER', brand='Tesla', model='Cybertruck', color='Silver')
<Car: CYBER, Tesla, Cybertruck>
>>> Car.objects.create(number='NIKOLA', brand='Tesla', model='Model S', color='White')
<Car: NIKOLA, Tesla, Model S>
>>> Car.objects.create(number='SERBIA', brand='Tesla', model='Model X', color='Blue')
<Car: SERBIA, Tesla, Model X>
>>> 
>>> def r_date():
...   start = datetime(2005, 1, 1)
...   end = datetime(2010, 1, 1)
...   return (start + timedelta(days=random.randint(0, (end - start).days))).strftime('%Y-%m-%d')
... 
>>> def r_number():
...   return str(random.randint(1000000000, 9999999999))
...
>>> License.objects.create(owner_id=1, number=r_number(), type='B', date_of_issue=r_date())
<License: Elon Musk>
>>> License.objects.create(owner_id=2, number=r_number(), type='B', date_of_issue=r_date())
<License: Mark Zuckerberg>
>>> License.objects.create(owner_id=3, number=r_number(), type='B', date_of_issue=r_date())
<License: Tony Stark>
>>> License.objects.create(owner_id=4, number=r_number(), type='B', date_of_issue=r_date())
<License: Jeff Bezos>
>>> License.objects.create(owner_id=5, number=r_number(), type='B', date_of_issue=r_date())
<License: Bill Gates>
>>> License.objects.create(owner_id=6, number=r_number(), type='B', date_of_issue=r_date())
<License: Donald Trump>
>>> 
>>> Ownership.objects.create(owner_id=1, car_id=1, start_date='2000-01-01', end_date='2010-01-01')
<Ownership: TIIIME, Elon Musk, 2000-01-01 - 2010-01-01>
>>> Ownership.objects.create(owner_id=2, car_id=2, start_date='2007-04-07', end_date='2009-06-24')
<Ownership: AUTOBOT, Mark Zuckerberg, 2007-04-07 - 2009-06-24>
>>> Ownership.objects.create(owner_id=2, car_id=3, start_date='2008-09-14')
<Ownership: BATMAN, Mark Zuckerberg, 2008-09-14 - None>
>>> Ownership.objects.create(owner_id=1, car_id=4, start_date='2024-02-02')
<Ownership: CYBER, Elon Musk, 2024-02-02 - None>
>>> Ownership.objects.create(owner_id=2, car_id=1, start_date='2015-10-21')
<Ownership: TIIIME, Mark Zuckerberg, 2015-10-21 - None>
>>> Ownership.objects.create(owner_id=1, car_id=2, start_date='2011-06-28')
<Ownership: AUTOBOT, Elon Musk, 2011-06-28 - None>
>>> Ownership.objects.create(owner_id=5, car_id=5, start_date='2020-05-05')
<Ownership: NIKOLA, Bill Gates, 2020-05-05 - None>
>>> Ownership.objects.create(owner_id=6, car_id=6, start_date='2020-06-06')
<Ownership: SERBIA, Donald Trump, 2020-06-06 - None>
>>> Ownership.objects.create(owner_id=3, car_id=5, start_date='2012-03-03', end_date='2019-03-03')
<Ownership: NIKOLA, Tony Stark, 2012-03-03 - 2019-03-03>
>>> Ownership.objects.create(owner_id=4, car_id=6, start_date='2012-04-04', end_date='2019-04-04')
<Ownership: SERBIA, Jeff Bezos, 2012-04-04 - 2019-04-04>
```

```python
>>> from project_first_app.models import *
>>> Car.objects.filter(brand='Tesla')
<QuerySet [<Car: CYBER, Tesla, Cybertruck>, <Car: NIKOLA, Tesla, Model S>, <Car: SERBIA, Tesla, Model X>]>
>>> Owner.objects.filter(first_name='Elon')
<QuerySet [<Owner: Elon Musk>]>
>>> License.objects.get(owner_id=Owner.objects.get(first_name='Elon').pk)
<License: Elon Musk>
>>> Owner.objects.filter(cars__color='Blue')
<QuerySet [<Owner: Donald Trump>, <Owner: Jeff Bezos>]>
>>> Owner.objects.filter(ownership__start_date__gte='2020-01-01')
<QuerySet [<Owner: Elon Musk>, <Owner: Bill Gates>, <Owner: Donald Trump>]>
```

```python
>>> from django.db.models import Min, Max, Count
>>> License.objects.aggregate(Min('date_of_issue'))
{'date_of_issue__min': datetime.date(2005, 3, 26)}
>>> Ownership.objects.filter(car__model='Cybertruck').aggregate(Max('start_date'))
{'start_date__max': datetime.date(2024, 2, 2)}
>>> for i in Owner.objects.annotate(count=Count('cars')):
...   print(i, i.count)
Elon Musk 3
Mark Zuckerberg 3
Tony Stark 1
Jeff Bezos 1
Bill Gates 1
Donald Trump 1
>>> Car.objects.values('brand').annotate(count=Count('pk'))
<QuerySet [{'brand': 'Chevrolet', 'count': 1}, {'brand': 'DeLorean', 'count': 1}, {'brand': 'Tesla', 'count': 3}, {'brand': 'Wayne Enterprises', 'count': 1}]>
>>> License.objects.order_by('date_of_issue')
<QuerySet [<License: Mark Zuckerberg>, <License: Elon Musk>, <License: Tony Stark>, <License: Jeff Bezos>, <License: Bill Gates>, <License: Donald Trump>]>
```