import pytest
from datetime import date
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate

from AutorepairShop.models import (
    Client,
    Employee,
    CarWorkshop,
    JobPosition,
    Automobile,
    Model as CarModel,
    Contract,
)

@pytest.fixture
def auth_get():
    factory = APIRequestFactory()
    def get(user, path, view, params=None, **kwargs):
        request = factory.get(path, params or {})
        force_authenticate(request, user=user)
        return view(request, **kwargs)
    return get

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser', 
        password='testpass',
        email="test@example.com"
    )

@pytest.fixture
def mechanic_position():
    return JobPosition.objects.create(
        name="Mechanic", 
        specialisation="engine", 
        salary=55000
    )

@pytest.fixture
def manager_position():
    return JobPosition.objects.create(
        name="Manager", 
        specialisation="admin", 
        salary=75000
    )

@pytest.fixture
def workshop():
    return CarWorkshop.objects.create(
        address="123 Workshop St",
        city="Moscow"
    )

@pytest.fixture
def mechanic(user, mechanic_position, workshop):
    return Employee.objects.create(
        user=user,
        full_name="Иван Иванов",
        phone="79216666666",
        email="mech@example.com",
        job_position=mechanic_position,
        car_workshop=workshop,
        rank=1,        
    )

@pytest.fixture
def manager(manager_position, workshop):
    user = User.objects.create_user(
        username='testmanager',
        password='testpass',
    )
    return Employee.objects.create(
        user=user,
        full_name="Петр Петров",
        phone="79216666667",
        email="manager@example.com",
        job_position=manager_position,
        car_workshop=workshop,
        rank=1,
    )

@pytest.fixture
def client(user):
    return Client.objects.create(
        user=user,
        full_name="Иван Иванов",
        phone="79216666668",
        email="client@example.com"
    )

@pytest.fixture
def car_model():
    return CarModel.objects.create(
        car_brand="BMW",
        country_of_production="Germany",
        model="X5",
        car_power=249,
    )

@pytest.fixture
def automobile(client, car_model):
    return Automobile.objects.create(
        engine_number="EN1",
        year_of_vehicle=2020,
        colour="black",
        state_number="A111AA",
        client=client,
        auto_model=car_model,
    )

@pytest.fixture
def make_contract():
    def create_contract(**kwargs):
        defaults = dict(
            order_date = date.today(),
            order_status = "open",
            payment_status = "paid",
            date_of_acceptance_for_repair = date.today(),
            scheduled_date_end_of_repair = None,
            actual_date_end_of_repair = None,
            total_payment = 10000,
        )
        defaults.update(kwargs)
        return Contract.objects.create(**defaults)
    return create_contract