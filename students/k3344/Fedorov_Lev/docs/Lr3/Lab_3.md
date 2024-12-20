# Лабораторная работа 3

## Обзор

Эта лабораторная работа включает создание Django-приложения для управления страховыми данными. Приложение включает
модели, сериалайзеры, представления и конфигурации URL. Также интегрирован Swagger для документации API.

## Модели БД

### InsuranceAgency

Представляет страховое агентство с полями для имени, агента и информации об агентстве.

### Agent

Представляет агента с полями для имени, фамилии, паспортных данных и контактной информации.

### EmploymentContract

Представляет трудовой договор между агентом и страховым агентством с полями для даты начала, даты окончания и зарплаты.

### Organization

Представляет организацию с полями для кода, полного имени, короткого имени, адреса, банковских реквизитов и
специализации.

### Employee

Представляет сотрудника с полями для контракта, организации, имени, фамилии, возраста, категории риска, суммы выплаты,
должности и паспортных данных.

### Position

Представляет должность с полями для имени и является ли она штатной.

### Contract

Представляет контракт с полями для агента, организации, сотрудника, даты начала, даты окончания, общей суммы, типа
контракта и информации о контракте.

### InsuranceCase

Представляет страховой случай с полями для контракта, даты, причины, решения о выплате и суммы выплаты.

## Сериалайзеры

Сериалайзеры используются для преобразования экземпляров моделей в формат JSON и обратно. Каждая модель имеет
соответствующий сериалайзер.

## Представления

Viewsets используются для обработки CRUD операций для каждой модели. Они используют соответствующие сериалайзеры.

## Конфигурации URL

URL конфигурации определяют маршруты для каждого viewset. Они также включают путь к Swagger.

## Swagger

Использовал Swagger для документации API. Решил что так будет нагляднее и удобнее все продемонстрировать.

Запуск проекта:

```bash
cd students/k3344/Fedorov_Lev/Lr3  
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Чтобы проверить работу сваггера, перейдите на адрес /swagger/ в браузере после запуска сервера.

## Скрины полученных результатов:

Заходим в Swagger: и ищем нужный нам блок авторизации, возьмем авторизацию. Поскольку создаем нового пользователя, то
нужен нам ПОСТ запрос на /api/auth/users/:
![img.png](img.png) - создаем пользователя с Json-запросом:

```json
{
  "email": "user@example.com",
  "username": "user1",
  "password": "gu.8F7v7A8Vb+mSUx-BkZJq1feBC6VE5Cn+2oHMJiPT4crMzJmrIINj"
}
```

Получаем следующий респонс:
![img_1.png](img_1.png) - респонс на создание пользователя:

```json

{
  "email": "user@example.com",
  "username": "user1",
  "id": 4
}
```

Пользователь создан, теперь можно авторизоваться и получить токен. Для этого нужно сделать ПОСТ запрос на
/api/auth/token/login/:
![img_2.png](img_2.png) - авторизация пользователя:

```json
{
  "password": "gu.8F7v7A8Vb+mSUx-BkZJq1feBC6VE5Cn+2oHMJiPT4crMzJmrIINj",
  "username": "user1"
}
```

![img_3.png](img_3.png) - респонс на авторизацию:

```json
{
  "auth_token": "e0fc736994312fbc59cff5f9c75d744b66bca91b"
}
```

http://127.0.0.1:8000/api/agents/ - список всех агентов:
![img_12.png](img_12.png)

Вложенность контрактов в листе агентов - one to many (один агент может иметь много контрактов): получается при помощи
сериализатора где подгружаются по айди агента его контракты.
Класс вьюсета:
```
@permission_classes([AllowAny])
class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
```
И сериализатор:
```
class AgentSerializer(serializers.ModelSerializer):
    contracts = EmploymentContractSerializer(many=True, read_only=True, source='employment_contracts') - подгружаем контракты по айди агента

    class Meta:
        model = Agent
        fields = ['id', 'first_name', 'last_name', 'passport_data', 'contact_info', 'contracts']
```
Демонстрацию крудов реализую через питоновский скрипт, который будет делать запросы на сервер через токен авторизации.

``` 
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"
LOGIN_URL = "http://127.0.0.1:8000/auth/token/"

USERNAME = "admin"
PASSWORD = "admin"

def get_token():
    response = requests.post(LOGIN_URL, data={"username": USERNAME, "password": PASSWORD})
    print("Response Status Code:", response.status_code)
    print("Response Content:", json.dumps(response.json(), indent=4))
    return response.json().get("access")

def pretty_print_response(response):
    if response.status_code in [200, 201]:
        print(json.dumps(response.json(), indent=4))
    else:
        print("Failed to retrieve data:", response.status_code, response.content)

def create_agent(token):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "first_name": "New",
        "last_name": "Agent",
        "passport_data": "Passport data for New Agent",
        "contact_info": "Contact info for New Agent"
    }
    response = requests.post(f"{BASE_URL}/agents/", headers=headers, data=json.dumps(data))
    pretty_print_response(response)
    return response.json().get("id")

def get_agent(token, agent_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/agents/{agent_id}/", headers=headers)
    pretty_print_response(response)

def update_agent(token, agent_id):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "first_name": "Updated",
        "last_name": "Agent",
        "passport_data": "Passport data for Updated Agent",
        "contact_info": "Contact info for Updated Agent"
    }
    response = requests.put(f"{BASE_URL}/agents/{agent_id}/", headers=headers, data=json.dumps(data))
    pretty_print_response(response)

def delete_agent(token, agent_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/agents/{agent_id}/", headers=headers)
    if response.status_code == 204:
        print(f"Agent with ID {agent_id} deleted successfully.")
    else:
        print("Failed to delete agent:", response.status_code, response.content)

if __name__ == "__main__":
    token = get_token()
    if token:
        agent_id = create_agent(token)
        if agent_id:
            get_agent(token, agent_id)
            update_agent(token, agent_id)
            get_agent(token, agent_id)
            delete_agent(token, agent_id)
            get_agent(token, agent_id)  # здесь 404 будет
    else:
        print("Failed to obtain token")
```

Результат работы скрипта:
```
Response Status Code: 200
Response Content: {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNDc3NjE1NSwiaWF0IjoxNzM0Njg5NzU1LCJqdGkiOiI0ZWVjODM4ZGM3OGY0NzE5YWE1OTE0MThkNDM4Mjk1NiIsInVzZXJfaWQiOjF9.nn8Cp1IH7eAGrrZ-L1BchLPFtsUkRqp1gGVkkGQAHBU",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM0NjkzMzU1LCJpYXQiOjE3MzQ2ODk3NTUsImp0aSI6IjBhOGMyOWI2NGYyZjQ4ZmY4ZjVmZmZkMDg4ZjQ1ZjllIiwidXNlcl9pZCI6MX0.CVQSHEJYfXaizLxN2Df2QXtIDYOowA8nSLD3fqAR88k"
}
{
    "id": 10,
    "first_name": "New",
    "last_name": "Agent",
    "passport_data": "Passport data for New Agent",
    "contact_info": "Contact info for New Agent",
    "contracts": []
}
{
    "id": 10,
    "first_name": "New",
    "last_name": "Agent",
    "passport_data": "Passport data for New Agent",
    "contact_info": "Contact info for New Agent",
    "contracts": []
}
{
    "id": 10,
    "first_name": "Updated",
    "last_name": "Agent",
    "passport_data": "Passport data for Updated Agent",
    "contact_info": "Contact info for Updated Agent",
    "contracts": []
}
{
    "id": 10,
    "first_name": "Updated",
    "last_name": "Agent",
    "passport_data": "Passport data for Updated Agent",
    "contact_info": "Contact info for Updated Agent",
    "contracts": []
}
Agent with ID 10 deleted successfully.
Failed to retrieve data: 404 b'{"detail":"No Agent matches the given query."}'

```
Как можем видеть, скрипт работает корректно и выполняет все действия.

### End-point-ы

# Swagger UI:

GET /swagger/
GET /swagger/?format=openapi

# User Authentication:

POST /api/auth/users/
GET /api/auth/users/

# Django Admin:

GET /admin/
ну а дальше в админке все как обычно.