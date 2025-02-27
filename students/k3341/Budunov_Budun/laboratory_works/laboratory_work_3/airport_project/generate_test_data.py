import os
import random
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airport_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from airport_app.models import *
from django.utils import timezone
from datetime import datetime, timedelta

def create_airlines():
    Airline.objects.create(name='Qatar Airways', country='Qatar', type=1)
    Airline.objects.create(name='Lufthansa', country='Germany', type=2)
    Airline.objects.create(name='Singapore Airlines', country='Singapore', type=3)
    Airline.objects.create(name='British Airways', country='UK', type=4)
    Airline.objects.create(name='Air France', country='France', type=5)

def create_airports():
    Airport.objects.create(name='Changi', code='SIN', city='Singapore', country='Singapore')
    Airport.objects.create(name='Heathrow', code='LHR', city='London', country='UK')
    Airport.objects.create(name='Charles de Gaulle', code='CDG', city='Paris', country='France')
    Airport.objects.create(name='Frankfurt', code='FRA', city='Frankfurt', country='Germany')
    Airport.objects.create(name='Munich', code='MUC', city='Munich', country='Germany')
    Airport.objects.create(name='Hamad', code='DOH', city='Doha', country='Qatar')
    Airport.objects.create(name='Schiphol', code='AMS', city='Amsterdam', country='Netherlands')
    Airport.objects.create(name='Zurich', code='ZRH', city='Zurich', country='Switzerland')
    Airport.objects.create(name='Vienna', code='VIE', city='Vienna', country='Austria')

def create_airplane_models():
    AirplaneModel.objects.create(name='Airbus A380', manufacture_name="Airbus", speed=945, seats=525, year_of_manufacture='2007-01-01')
    AirplaneModel.objects.create(name='Boeing 787', manufacture_name="Boeing", speed=903, seats=330, year_of_manufacture='2011-01-01')
    AirplaneModel.objects.create(name='Airbus A350', manufacture_name="Airbus", speed=945, seats=440, year_of_manufacture='2013-01-01')
    AirplaneModel.objects.create(name='Boeing 777X', manufacture_name="Boeing", speed=896, seats=426, year_of_manufacture='2020-01-01')
    AirplaneModel.objects.create(name='Airbus A330neo', manufacture_name="Airbus", speed=870, seats=300, year_of_manufacture='2018-01-01')

def create_airplanes():
    airline1 = Airline.objects.get(name='Qatar Airways')
    airline2 = Airline.objects.get(name='Lufthansa')
    model1 = AirplaneModel.objects.get(name='Airbus A380')
    model2 = AirplaneModel.objects.get(name='Boeing 787')
    model3 = AirplaneModel.objects.get(name='Airbus A350', manufacture_name="Airbus", speed=945, seats=440, year_of_manufacture='2013-01-01')
    model4 = AirplaneModel.objects.get(name='Boeing 777X')
    model5 = AirplaneModel.objects.get(name='Airbus A330neo')
    
    Airplane.objects.create(airline=airline1, serial_number='A380-QTR001', airplane_model=model1, status='Active')
    Airplane.objects.create(airline=airline1, serial_number='B787-QTR101', airplane_model=model2, status='Active')
    Airplane.objects.create(airline=airline2, serial_number='A350-LH201', airplane_model=model3, status='Active')
    Airplane.objects.create(airline=airline2, serial_number='B777X-LH301', airplane_model=model4, status='Active')
    Airplane.objects.create(airline=airline1, serial_number='A330N-QTR401', airplane_model=model5, status='Maintenance')
    Airplane.objects.create(airline=airline2, serial_number='B787-LH501', airplane_model=model2, status='Decommissioned')
    Airplane.objects.create(airline=airline1, serial_number='A350-QTR601', airplane_model=model3, status='Active')
    Airplane.objects.create(airline=airline1, serial_number='A330N-QTR701', airplane_model=model5, status='Active')

def create_employees(password):
    airline1 = Airline.objects.get(name='Qatar Airways')
    airline2 = Airline.objects.get(name='Lufthansa')
    User = get_user_model()
    
    employees_data = [
        ('pilot_smith', 'James Smith', airline1, 'Pilot', '1975-05-15'),
        ('copilot_mueller', 'Hans Mueller', airline2, 'Co-Pilot', '1982-03-20'),
        ('engineer_chen', 'Li Chen', airline1, 'Flight Engineer', '1980-11-10'),
        ('attendant_garcia', 'Maria Garcia', airline2, 'Flight Attendant', '1988-07-25'),
        ('nav_kumar', 'Raj Kumar', airline1, 'Navigator', '1979-09-30'),
        ('loadmaster_anderson', 'Erik Anderson', airline2, 'Loadmaster', '1985-12-05'),
        ('pilot_zhang', 'Wei Zhang', airline1, 'Pilot', '1977-04-18'),
        ('stewardess_patel', 'Priya Patel', airline2, 'Stewardess', '1983-08-22'),
        ('copilot_brown', 'David Brown', airline1, 'Co-Pilot', '1976-01-14'),
        ('admin_kim', 'Min-ji Kim', airline2, 'admin', '1987-06-28')
    ]

    for username, name, airline, role, birth_date in employees_data:
        user = User.objects.create_user(username=username, password=password)
        Employee.objects.create(
            user=user,
            full_name=name,
            airline=airline,
            passport_data=f'P{random.randint(100000, 999999)}',
            role=role,
            birth_date=birth_date,
            education='Aviation Academy',
            experience=f'{random.randint(5, 25)} years'
        )

def create_crews():
    employees = list(Employee.objects.all())
    crew_roles = ["Pilot", "Co-Pilot", "Flight Engineer", "Flight Attendant", "Navigator", "Loadmaster", "Stewardess"]
    
    for i in range(5):
        crew = Crew.objects.create(is_approved=random.choice([True, False]))
        crew_members = random.sample(employees, 3)
        for member, role in zip(crew_members, random.sample(crew_roles, 3)):
            CrewMember.objects.create(crew=crew, employee=member, role=role)

def create_routes():
    airlines = Airline.objects.all()
    airports = Airport.objects.all()
    
    route_data = [
        ('London-Paris', 'LHR', 'CDG', 2),
        ('Singapore-Doha', 'SIN', 'DOH', 7),
        ('Frankfurt-Vienna', 'FRA', 'VIE', 3),
        ('Amsterdam-Zurich', 'AMS', 'ZRH', 2),
        ('Munich-London', 'MUC', 'LHR', 3)
    ]

    for name, dep_code, arr_code, duration in route_data:
        dep_airport = Airport.objects.get(code=dep_code)
        arr_airport = Airport.objects.get(code=arr_code)
        airline = random.choice(airlines)
        
        departure_time = timezone.make_aware(datetime.now() + timedelta(days=random.randint(1, 30)))
        arrival_time = departure_time + timedelta(hours=duration)
        
        Route.objects.create(
            name=name,
            departure_airport=dep_airport,
            arrival_airport=arr_airport,
            airline=airline,
            departure_time=departure_time,
            arrival_time=arrival_time,
            total_time=timedelta(hours=duration),
            periodicity=random.choice(['Daily', 'Weekly']),
            transit_id_sequence={}
        )

def create_transits():
    routes = Route.objects.all()
    airports = Airport.objects.all()
    
    for route in routes:
        if random.choice([True, False]):
            transit_airport = random.choice([a for a in airports 
                                          if a != route.departure_airport 
                                          and a != route.arrival_airport])
            
            transit_departure = route.departure_time + timedelta(hours=2)
            transit_arrival = transit_departure + timedelta(hours=1)
            
            transit = Transit.objects.create(
                route=route,
                departure_airport=transit_airport,
                arrival_airport=route.arrival_airport,
                departure_time=transit_departure,
                arrival_time=transit_arrival,
                transit_order=1
            )
            route.transit_id_sequence = {1: transit.id}
            route.save()

def create_flights():
    crews = Crew.objects.all()
    airplanes = Airplane.objects.filter(status='Active')
    routes = Route.objects.all()
    
    flight_statuses = ['Scheduled', 'Delayed', 'In Air', 'Landed', 'Cancelled']
    
    for i in range(10):
        Flight.objects.create(
            crew=random.choice(crews),
            airplane=random.choice(airplanes),
            route=random.choice(routes),
            flight_number=f'{random.choice(["QR", "LH", "SQ"])}{random.randint(100, 999)}',
            sold_tickets=random.randint(100, 400),
            flight_status=random.choice(flight_statuses)
        )

def create_maintenance():
    airplanes = Airplane.objects.all()
    maintenance_types = ['Regular Check', 'Engine Inspection', 'Avionics Update', 
                        'Interior Refurbishment', 'Emergency Systems Check']
    
    for airplane in airplanes:
        maintenance_date = timezone.now() - timedelta(days=random.randint(1, 90))
        AirplaneMaintenance.objects.create(
            airplane=airplane,
            maintenance_date=maintenance_date,
            is_completed=random.choice([True, False]),
            notes=f'{random.choice(maintenance_types)} for {airplane.serial_number}'
        )

def create_superuser(username, password):
    User = get_user_model()
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, password=password)
    else:
        print("Superuser with this username already exists")

if __name__ == '__main__':
    print('Creating test data...')
    create_superuser("admin", "admin")
    create_airlines()
    create_airports()
    create_airplane_models()
    create_airplanes()
    create_employees("defaultpassword")
    create_crews()
    create_routes()
    create_transits()
    create_flights()
    create_maintenance()
    print('Test data created successfully.')
