import random
from faker import Faker
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from airport_app.models import (Airline, Airport, Route, Transit, AirplaneModel, Airplane, 
                          AirplaneMaintenance, Employee, Crew, CrewMember, Flight)

def gen_data():

    fake = Faker()

    # Очистка базы данных
    Flight.objects.all().delete()
    CrewMember.objects.all().delete()
    Crew.objects.all().delete()
    Employee.objects.all().delete()
    AirplaneMaintenance.objects.all().delete()
    Airplane.objects.all().delete()
    AirplaneModel.objects.all().delete()
    Transit.objects.all().delete()
    Route.objects.all().delete()
    Airport.objects.all().delete()
    Airline.objects.all().delete()

    # Создаем авиалинии
    airlines = [Airline.objects.create(name=fake.company(), country=fake.country(), type=random.randint(1, 5)) for _ in range(5)]

    # Создаем аэропорты
    airports = [Airport.objects.create(code=fake.unique.bothify(text='??###'), name=fake.city(), city=fake.city(), country=fake.country()) for _ in range(10)]

    # Создаем модели самолетов
    airplane_models = [AirplaneModel.objects.create(
        name=fake.word(), 
        speed=random.randint(600, 900), 
        seats=random.randint(100, 400),
        year_of_manufacture=make_aware(fake.date_time_this_century().replace(second=0, microsecond=0)),
        manufacture_name=fake.company()
    ) for _ in range(10)]

    # Создаем самолеты
    airplanes = [Airplane.objects.create(
        airline=random.choice(airlines),
        serial_number=fake.unique.bothify(text='SN###???'),
        airplane_model=random.choice(airplane_models),
        status=random.choice(['active', 'maintenance', 'retired'])
    ) for _ in range(200)]

    # Создаем маршруты
    routes = []
    for _ in range(50):
        departure_time = make_aware(fake.date_time_this_year().replace(second=0, microsecond=0))
        arrival_time = departure_time + timedelta(hours=random.randint(1, 12))
        route = Route.objects.create(
            departure_airport=random.choice(airports),
            arrival_airport=random.choice(airports),
            airline=random.choice(airlines),
            name=fake.unique.bothify(text='RN##??'),
            departure_time=departure_time,
            arrival_time=arrival_time,
            total_time=arrival_time - departure_time,
            periodicity=random.choice(['daily', 'weekly', 'monthly']),
            transit_id_sequence=[]
        )
        routes.append(route)

    # Создаем пересадки (transits)
    for route in routes:
        num_transits = random.randint(0, 3)
        transit_airports = random.sample(airports, num_transits)
        transit_ids = []
        for i, airport in enumerate(transit_airports):
            transit = Transit.objects.create(
                route=route,
                departure_airport=route.departure_airport if i == 0 else transit_airports[i - 1],
                arrival_airport=airport,
                departure_time=route.departure_time + timedelta(hours=i * 2),
                arrival_time=route.departure_time + timedelta(hours=i * 2 + 1),
                transit_order=i + 1
            )
            transit_ids.append(transit.id)
        route.transit_id_sequence = transit_ids
        route.save()

    # Создаем сотрудников
    employees = [Employee.objects.create(
        airline=random.choice(airlines),
        age=random.randint(22, 60),
        full_name=fake.name(),
        education=fake.job(),
        passport_data=fake.unique.bothify(text='????######'),
        experience=fake.word(),
        job_title=random.choice(['Pilot', 'Flight Attendant', 'Mechanic', 'Dispatcher'])
    ) for _ in range(100)]

    # Создаем экипажи
    crews = [Crew.objects.create(is_approved=random.choice([True, False])) for _ in range(50)]

    # Добавляем членов экипажей
    for crew in crews:
        num_members = random.randint(2, 6)
        crew_employees = random.sample(employees, num_members)
        for emp in crew_employees:
            CrewMember.objects.create(crew=crew, employee=emp, role=emp.job_title)

    # Создаем рейсы
    flights = [Flight.objects.create(
        airplane=random.choice(airplanes),
        crew=random.choice(crews),
        route=random.choice(routes),
        sold_tickets=random.randint(0, 200),
        flight_number=fake.unique.bothify(text='FL###???'),
        flight_status=random.choice(['scheduled', 'delayed', 'cancelled'])
    ) for _ in range(100)]

    # Создаем записи о техническом обслуживании самолетов
    for airplane in airplanes:
        num_maintenances = random.randint(1, 5)
        for _ in range(num_maintenances):
            AirplaneMaintenance.objects.create(
                airplane=airplane,
                maintenance_date=make_aware(fake.date_time_this_decade().replace(second=0, microsecond=0)),
                is_completed=random.choice([True, False]),
                notes=fake.text()
            )

    print("Тестовые данные успешно созданы!")
