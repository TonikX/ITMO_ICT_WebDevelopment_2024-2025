import pytest
from django.utils.timezone import now

from AutorepairShop.serializers import (
    AutomobileSerializer,
    ContractSerializer,
)

@pytest.mark.django_db
def test_automobile_serializer_write_via_id_and_read_nested_properties(client, car_model):
    # Проверяем, что автомобиль можно создать через client_id, auto_model_id поля.
    # При чтении возвращаем вложенные client и auto_model с нужными данными.
    payload = {
        "engine_number": "EN-NEW-42",
        "year_of_vehicle": 2021,
        "colour": "green",
        "state_number": "O123OO198",
        "client_id": client.id,
        "auto_model_id": car_model.id,        
    }

    ser = AutomobileSerializer(data=payload)
    assert ser.is_valid(), ser.errors
    instance = ser.save()
    out = AutomobileSerializer(instance).data

    assert out["client"]["full_name"] == client.full_name
    assert out["auto_model"]["car_brand"] == car_model.car_brand

@pytest.mark.django_db
def test_contract_serializer_write_via_id_and_read_nested_properties(client, automobile, mechanic):
    # Проверяем, что сериализатор принимает *_id и успешно создает контракт.
    # При чтении возвращаем вложенные client/auto/employee с нужными данными.

    payload = {
        "order_date": str(now().date()),
        "order_status": "open",
        "payment_status": "paid",
        "date_of_acceptance_for_repair": str(now().date()),
        "client_id": client.id,
        "auto_id": automobile.id,
        "employee_id": mechanic.id,
    }

    ser = ContractSerializer(data=payload)
    assert ser.is_valid(), ser.errors
    instance = ser.save()
    out = ContractSerializer(instance).data

    assert out["client"]["full_name"] == client.full_name
    assert out["auto"]["state_number"] == automobile.state_number
    assert out["employee"]["full_name"] == mechanic.full_name

@pytest.mark.django_db
def test_contract_serializer_employee_is_null(client, automobile):
    # Проверка случая, когда сотрудник не передается в контракт.
    # Проверяем, что контракт создается без сотрудника и сериализация возвращает None.
    payload ={
        "order_date": str(now().date()),
        "order_status": "open",
        "payment_status": "paid",
        "date_of_acceptance_for_repair": str(now().date()),
        "client_id": client.id,
        "auto_id": automobile.id,
        "employee_id": None,        
    }

    ser = ContractSerializer(data=payload)
    assert ser.is_valid(), ser.errors
    instance = ser.save()
    out = ContractSerializer(instance).data

    assert out["employee"] is None