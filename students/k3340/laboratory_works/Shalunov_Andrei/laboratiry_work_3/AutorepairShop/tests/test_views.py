from datetime import date, timedelta

import pytest
from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework import status

from AutorepairShop.views import ClientViewSet, EmployeeViewSet
from AutorepairShop.models import Client, Automobile, Employee

@pytest.mark.django_db
def test_action_yearly_visits_counts_last_365(auth_get, user, client, automobile, mechanic, make_contract):
    # Проверяем, что yearly_visits считает обращения клиента только за последний год
    make_contract(
        client=client, 
        auto=automobile, 
        employee=mechanic, 
        order_date = now().date() - timedelta(days=10)
    )
    make_contract(
        client=client, 
        auto=automobile, 
        employee=mechanic, 
        order_date = now().date() - timedelta(days=370)
    )
    view = ClientViewSet.as_view({"get": "yearly_visits"})

    response = auth_get(user, f"/clients/{client.id}/yearly_visits/", view, None, pk=client.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["client"] == client.full_name
    assert response.data["visits"] == 1

@pytest.mark.django_db
def test_action_repeat_clients_returns_only_multi_visit(auth_get, user, client, automobile, mechanic, make_contract):
    # Проверяем, что repeat_clients возвращает только клиентов с числом обращений > 1
    make_contract(client=client, auto=automobile, employee=mechanic)
    make_contract(client=client, auto=automobile, employee=mechanic)

    user_2 = User.objects.create(username="testuser2")
    client_2 = Client.objects.create(user=user_2, full_name="Клиент №2", phone="89211234567")
    auto_2 = Automobile.objects.create(
        engine_number="EN2",
        year_of_vehicle=2025,
        colour="gold",
        state_number="O222OO98",
        client=client_2, 
        auto_model=automobile.auto_model,
    )
    make_contract(client=client_2, auto=auto_2, employee=mechanic)
    view = ClientViewSet.as_view({"get": "repeat_clients"})
    
    response = auth_get(user, "/clients/repeat_clients/", view)

    assert response.status_code == status.HTTP_200_OK
    names = [row["full_name"] for row in response.data]
    assert client.full_name in names
    assert client_2.full_name not in names

@pytest.mark.django_db
def test_action_top_mechanic_by_brand_requires_query(auth_get, user):
    # Проверяем случай - если не передать ?brand= в top_mechanic_by_brand, то возвращается 400 с сообщением об ошибке
    view = EmployeeViewSet.as_view({"get": "top_mechanic_by_brand"})

    response = auth_get(user, "/employees/top_mechanic_by_brand/", view)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "brand" in response.data.get("error")

@pytest.mark.django_db
def test_action_top_mechanic_by_brand_selects_max(auth_get, user, mechanic, workshop, automobile, make_contract):
    # Проверяем, что top_mechanic_by_brand возвращает механика с максимальным количеством работ по заданному бренду
    car_brand = automobile.auto_model.car_brand
    client = automobile.client
    user_2 = User.objects.create(username="testuser2")
    mechanic_2 = Employee.objects.create(
        user=user_2, 
        full_name="Петр Петров", 
        phone="89212345678", 
        email="mechanic_2@example.com",
        job_position=mechanic.job_position, 
        car_workshop=workshop, 
        rank=1,
    )
    make_contract(client=client, auto=automobile, employee=mechanic)
    make_contract(client=client, auto=automobile, employee=mechanic_2)
    make_contract(client=client, auto=automobile, employee=mechanic_2)
    view = EmployeeViewSet.as_view({"get": "top_mechanic_by_brand"})

    response = auth_get(user, f"/employees/top_mechanic_by_brand/?brand={car_brand}", view, {"brand": car_brand})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["car_brand"] == car_brand
    assert response.data["mechanic_name"] == "Петр Петров"
    assert response.data["job_counts"] == 2

@pytest.mark.django_db
def test_action_loyal_clients_with_incorrect_job_position(user, manager, auth_get):
    # Проверяем случай - если сотрудник не механик, то action loyal_clients возвращает 400 с сообщением об ошибке
    view = EmployeeViewSet.as_view({"get": "loyal_clients"})

    response = auth_get(user, f"/employees/{manager.id}/loyal_clients/", view, None, pk=manager.id)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Этот сотрудник не является механиком" in response.data.get("error")

@pytest.mark.django_db
def test_action_delayed_days_returns_correct_number_of_days_for_client(auth_get, user, client, mechanic, automobile, workshop, make_contract):
    # Проверяем, что delayed_days корректно считает количество дней просрочки
    make_contract(
        client=client, 
        auto=automobile, 
        employee=mechanic,
        scheduled_date_end_of_repair=date.today() - timedelta(days=10),
        actual_date_end_of_repair=date.today(),
    )
    view = EmployeeViewSet.as_view({"get": "delayed_days"})

    response = auth_get(user, f"/employees/{mechanic.id}/delayed_days/", view, None, pk=mechanic.id)

    assert response.status_code == status.HTTP_200_OK
    rows = response.data
    assert rows[0]["client_name"] == client.full_name
    assert rows[0]["days_late"] == 10

@pytest.mark.django_db
def test_action_fines_calculation(user, mechanic, client, automobile, make_contract, auth_get):
    # Проверяем, что fines считает штраф корректно: 5% от total_payment за каждый день просрочки
    days_late = 3
    fine_amount = 10_000 * 0.05 * days_late
    make_contract(
        client=client, 
        auto=automobile, 
        employee=mechanic,
        date_of_acceptance_for_repair=now().date() - timedelta(days=10),
        scheduled_date_end_of_repair=now().date() - timedelta(days=5),
        actual_date_end_of_repair=now().date() - timedelta(days=2),
        total_payment=10000,
    )
    view = EmployeeViewSet.as_view({"get": "fines"})

    response = auth_get(user, f"/employees/{mechanic.id}/fines/", view, None, pk=mechanic.id)

    assert response.status_code == status.HTTP_200_OK
    fine_data = response.data[0]
    assert fine_data["client_name"] == client.full_name
    assert fine_data["days_late"] == days_late
    assert fine_data["fine"] == fine_amount