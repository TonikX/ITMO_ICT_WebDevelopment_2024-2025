from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import timedelta
from .models import *
from .serializers import *
from .permissions import IsAdminUser, IsCrewUser, IsAdminOrReadOnly, IsOwner


class CustomUserModelTest(TestCase):
    """Тестирование модели пользователя"""
    
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com',
            'is_admin': True
        }

    def test_create_user_sets_username_correctly(self):
        """Тест: создание пользователя устанавливает правильное имя пользователя"""
        user = get_user_model().objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'testuser')

    def test_create_user_sets_email_correctly(self):
        """Тест: создание пользователя устанавливает правильный email"""
        user = get_user_model().objects.create_user(**self.user_data)
        self.assertEqual(user.email, 'test@example.com')

    def test_create_user_sets_admin_flag_correctly(self):
        """Тест: создание пользователя устанавливает правильный флаг администратора"""
        user = get_user_model().objects.create_user(**self.user_data)
        self.assertTrue(user.is_admin)

    def test_create_user_has_correct_password(self):
        """Тест: создание пользователя устанавливает правильный пароль"""
        user = get_user_model().objects.create_user(**self.user_data)
        self.assertTrue(user.check_password('testpass123'))

    def test_create_user_sets_active_status(self):
        """Тест: создание пользователя устанавливает активный статус"""
        user = get_user_model().objects.create_user(**self.user_data)
        self.assertTrue(user.is_active)

    def test_create_superuser_sets_staff_flag(self):
        """Тест: создание суперпользователя устанавливает флаг staff"""
        admin_user = get_user_model().objects.create_superuser(
            username='admin',
            password='adminpass123'
        )
        self.assertTrue(admin_user.is_staff)

    def test_create_superuser_sets_superuser_flag(self):
        """Тест: создание суперпользователя устанавливает флаг superuser"""
        admin_user = get_user_model().objects.create_superuser(
            username='admin',
            password='adminpass123'
        )
        self.assertTrue(admin_user.is_superuser)


class EmployeeModelTest(TestCase):
    """Тестирование модели сотрудника"""
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='employee_user',
            password='testpass123'
        )
        self.airline = Airline.objects.create(
            name='Test Airlines',
            country='Test Country',
            type=1
        )
        self.employee_data = {
            'user': self.user,
            'airline': self.airline,
            'role': 'Pilot',
            'birth_date': '1990-01-01',
            'full_name': 'John Doe',
            'passport_data': 'AB123456'
        }

    def test_create_employee_sets_full_name(self):
        """Тест: создание сотрудника устанавливает полное имя"""
        employee = Employee.objects.create(**self.employee_data)
        self.assertEqual(employee.full_name, 'John Doe')

    def test_create_employee_sets_role(self):
        """Тест: создание сотрудника устанавливает роль"""
        employee = Employee.objects.create(**self.employee_data)
        self.assertEqual(employee.role, 'Pilot')

    def test_create_employee_links_to_airline(self):
        """Тест: создание сотрудника связывает с авиакомпанией"""
        employee = Employee.objects.create(**self.employee_data)
        self.assertEqual(employee.airline.name, 'Test Airlines')

    def test_employee_has_user_relation(self):
        """Тест: сотрудник имеет связь с пользователем"""
        employee = Employee.objects.create(**self.employee_data)
        self.assertTrue(hasattr(employee.user, 'employee'))


class PermissionTest(TestCase):
    """Тестирование кастомных permissions"""
    
    def setUp(self):
        self.admin_user = get_user_model().objects.create_user(
            username='admin',
            password='pass123',
            is_admin=True
        )
        self.regular_user = get_user_model().objects.create_user(
            username='regular',
            password='pass123',
            is_admin=False
        )
        self.employee_user = get_user_model().objects.create_user(
            username='employee',
            password='pass123',
            is_admin=False
        )
        
        airline = Airline.objects.create(name='Test Airline', country='Test', type=1)
        Employee.objects.create(
            user=self.employee_user,
            airline=airline,
            role='Pilot',
            birth_date='1990-01-01',
            full_name='Test Employee',
            passport_data='TEST123'
        )

    def test_is_admin_user_grants_access_to_admin(self):
        """Тест: IsAdminUser предоставляет доступ администратору"""
        permission = IsAdminUser()
        request = self._create_mock_request(self.admin_user)
        self.assertTrue(permission.has_permission(request, None))

    def test_is_admin_user_denies_access_to_regular_user(self):
        """Тест: IsAdminUser запрещает доступ обычному пользователю"""
        permission = IsAdminUser()
        request = self._create_mock_request(self.regular_user)
        self.assertFalse(permission.has_permission(request, None))

    def test_is_crew_user_grants_access_to_employee(self):
        """Тест: IsCrewUser предоставляет доступ сотруднику"""
        permission = IsCrewUser()
        request = self._create_mock_request(self.employee_user)
        self.assertTrue(permission.has_permission(request, None))

    def test_is_crew_user_denies_access_to_regular_user(self):
        """Тест: IsCrewUser запрещает доступ обычному пользователю"""
        permission = IsCrewUser()
        request = self._create_mock_request(self.regular_user)
        self.assertFalse(permission.has_permission(request, None))

    def test_is_owner_grants_access_to_owner(self):
        """Тест: IsOwner предоставляет доступ владельцу объекта"""
        permission = IsOwner()
        request = self._create_mock_request(self.admin_user)
        self.assertTrue(permission.has_object_permission(request, None, self.admin_user))

    def test_is_owner_denies_access_to_non_owner(self):
        """Тест: IsOwner запрещает доступ не-владельцу объекта"""
        permission = IsOwner()
        request = self._create_mock_request(self.admin_user)
        self.assertFalse(permission.has_object_permission(request, None, self.regular_user))

    def _create_mock_request(self, user):
        """Вспомогательный метод для создания mock request"""
        class MockRequest:
            def __init__(self, user):
                self.user = user
        return MockRequest(user)


class SerializerTest(TestCase):
    """Тестирование сериализаторов"""

    def test_airline_serializer_validates_correct_data(self):
        """Тест: AirlineSerializer валидирует корректные данные"""
        data = {'name': 'Test Airlines', 'country': 'Test Country', 'type': 1}
        serializer = AirlineSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_airline_serializer_creates_object(self):
        """Тест: AirlineSerializer создает объект"""
        data = {'name': 'Test Airlines', 'country': 'Test Country', 'type': 1}
        serializer = AirlineSerializer(data=data)
        serializer.is_valid()
        airline = serializer.save()
        self.assertEqual(airline.name, 'Test Airlines')

    def test_login_serializer_validates_correct_data(self):
        """Тест: LoginSerializer валидирует корректные данные"""
        data = {'username': 'testuser', 'password': 'testpass'}
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_login_serializer_sets_correct_data(self):
        """Тест: LoginSerializer устанавливает правильные данные"""
        data = {'username': 'testuser', 'password': 'testpass'}
        serializer = LoginSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(serializer.validated_data['username'], 'testuser')
        self.assertEqual(serializer.validated_data['password'], 'testpass')


class APIIntegrationTest(APITestCase):
    """Интеграционные тесты API"""
    
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_user(
            username='admin',
            password='adminpass123',
            is_admin=True
        )
        
        self.airline = Airline.objects.create(
            name='Test Airlines',
            country='Test Country',
            type=1
        )

    def test_unauthenticated_access_to_airline_api_returns_401(self):
        """Тест: неаутентифицированный доступ к API авиакомпаний возвращает 401"""
        response = self.client.get('/api/airline/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_admin_access_to_airline_api_returns_200(self):
        """Тест: аутентифицированный доступ администратора к API авиакомпаний возвращает 200"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/airline/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_airline_creation_returns_201(self):
        """Тест: создание авиакомпании возвращает 201"""
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': 'New Airlines', 'country': 'New Country', 'type': 2}
        response = self.client.post('/api/airline/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_airline_creation_increases_count(self):
        """Тест: создание авиакомпании увеличивает счетчик"""
        self.client.force_authenticate(user=self.admin_user)
        initial_count = Airline.objects.count()
        data = {'name': 'New Airlines', 'country': 'New Country', 'type': 2}
        self.client.post('/api/airline/', data, format='json')
        self.assertEqual(Airline.objects.count(), initial_count + 1)


class EmployeeAPITest(APITestCase):
    """Тесты API сотрудников"""
    
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_user(
            username='admin',
            password='adminpass123',
            is_admin=True
        )
        
        self.airline = Airline.objects.create(
            name='Test Airlines',
            country='Test Country',
            type=1
        )

    def test_employee_creation_returns_200(self):
        """Тест: создание сотрудника возвращает 200"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'user': {
                'username': 'newemployee',
                'password': 'employeepass123',
                'email': 'employee@example.com',
                'is_admin': False
            },
            'airline': self.airline.id,
            'role': 'Pilot',
            'birth_date': '1990-01-01',
            'full_name': 'New Employee',
            'passport_data': 'NEW123456'
        }
        response = self.client.post('/api/employee/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_creation_creates_user(self):
        """Тест: создание сотрудника создает пользователя"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'user': {
                'username': 'newemployee',
                'password': 'employeepass123',
                'email': 'employee@example.com',
                'is_admin': False
            },
            'airline': self.airline.id,
            'role': 'Pilot',
            'birth_date': '1990-01-01',
            'full_name': 'New Employee',
            'passport_data': 'NEW123456'
        }
        self.client.post('/api/employee/', data, format='json')
        self.assertTrue(get_user_model().objects.filter(username='newemployee').exists())

    def test_employee_creation_creates_employee_record(self):
        """Тест: создание сотрудника создает запись сотрудника"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'user': {
                'username': 'newemployee',
                'password': 'employeepass123',
                'email': 'employee@example.com',
                'is_admin': False
            },
            'airline': self.airline.id,
            'role': 'Pilot',
            'birth_date': '1990-01-01',
            'full_name': 'New Employee',
            'passport_data': 'NEW123456'
        }
        self.client.post('/api/employee/', data, format='json')
        self.assertTrue(Employee.objects.filter(full_name='New Employee').exists())


class FlightBusinessLogicTest(TestCase):
    """Тестирование бизнес-логики рейсов"""
    
    def setUp(self):
        self.airline = Airline.objects.create(
            name='Flight Test Airlines',
            country='Test Country',
            type=1
        )
        
        self.departure_airport = Airport.objects.create(
            code='DEP',
            name='Departure Airport',
            city='Departure City',
            country='Test Country'
        )
        
        self.arrival_airport = Airport.objects.create(
            code='ARR',
            name='Arrival Airport',
            city='Arrival City',
            country='Test Country'
        )

    def test_route_creation_sets_name(self):
        """Тест: создание маршрута устанавливает имя"""
        route = self._create_test_route()
        self.assertEqual(route.name, 'TEST_ROUTE')

    def test_route_creation_links_departure_airport(self):
        """Тест: создание маршрута связывает аэропорт вылета"""
        route = self._create_test_route()
        self.assertEqual(route.departure_airport.code, 'DEP')

    def test_route_creation_links_arrival_airport(self):
        """Тест: создание маршрута связывает аэропорт прилета"""
        route = self._create_test_route()
        self.assertEqual(route.arrival_airport.code, 'ARR')

    def test_route_creation_sets_correct_duration(self):
        """Тест: создание маршрута устанавливает правильную продолжительность"""
        route = self._create_test_route()
        self.assertEqual(route.total_time, timedelta(hours=2))

    def test_transit_creation_sets_order(self):
        """Тест: создание транзита устанавливает порядок"""
        route = self._create_test_route()
        transit = self._create_test_transit(route)
        self.assertEqual(transit.transit_order, 1)

    def test_transit_creation_links_airport(self):
        """Тест: создание транзита связывает аэропорт"""
        route = self._create_test_route()
        transit = self._create_test_transit(route)
        self.assertEqual(transit.arrival_airport.code, 'TRN')

    def _create_test_route(self):
        """Вспомогательный метод для создания тестового маршрута"""
        return Route.objects.create(
            departure_airport=self.departure_airport,
            arrival_airport=self.arrival_airport,
            airline=self.airline,
            name='TEST_ROUTE',
            departure_time='2024-01-01T10:00:00Z',
            arrival_time='2024-01-01T12:00:00Z',
            total_time=timedelta(hours=2),
            periodicity='daily',
            transit_id_sequence=[]
        )

    def _create_test_transit(self, route):
        """Вспомогательный метод для создания тестового транзита"""
        transit_airport = Airport.objects.create(
            code='TRN',
            name='Transit Airport',
            city='Transit City',
            country='Test Country'
        )
        
        return Transit.objects.create(
            route=route,
            departure_airport=self.departure_airport,
            arrival_airport=transit_airport,
            arrival_time='2024-01-01T11:00:00Z',
            departure_time='2024-01-01T11:30:00Z',
            transit_order=1
        )


class AirportModelTest(TestCase):
    """Тестирование модели аэропорта"""

    def test_airport_creation_sets_code(self):
        """Тест: создание аэропорта устанавливает код"""
        airport = Airport.objects.create(
            code='TEST',
            name='Test Airport',
            city='Test City',
            country='Test Country'
        )
        self.assertEqual(airport.code, 'TEST')

    def test_airport_creation_sets_name(self):
        """Тест: создание аэропорта устанавливает имя"""
        airport = Airport.objects.create(
            code='TEST',
            name='Test Airport',
            city='Test City',
            country='Test Country'
        )
        self.assertEqual(airport.name, 'Test Airport')

    def test_airport_string_representation(self):
        """Тест: строковое представление аэропорта"""
        airport = Airport.objects.create(
            code='TEST',
            name='Test Airport',
            city='Test City',
            country='Test Country'
        )
        self.assertEqual(str(airport), 'Test Airport (TEST)')


class AirplaneModelTest(TestCase):
    """Тестирование модели самолета"""
    
    def setUp(self):
        self.airline = Airline.objects.create(
            name='Test Airlines',
            country='Test Country',
            type=1
        )
        
        self.airplane_model = AirplaneModel.objects.create(
            speed=800,
            seats=150,
            name='Boeing 737',
            year_of_manufacture='2020-01-01T00:00:00Z',
            manufacture_name='Boeing'
        )

    def test_airplane_creation_sets_serial_number(self):
        """Тест: создание самолета устанавливает серийный номер"""
        airplane = Airplane.objects.create(
            airline=self.airline,
            serial_number='SN123456',
            airplane_model=self.airplane_model,
            status='Active'
        )
        self.assertEqual(airplane.serial_number, 'SN123456')

    def test_airplane_creation_links_model(self):
        """Тест: создание самолета связывает модель"""
        airplane = Airplane.objects.create(
            airline=self.airline,
            serial_number='SN123456',
            airplane_model=self.airplane_model,
            status='Active'
        )
        self.assertEqual(airplane.airplane_model.name, 'Boeing 737')

    def test_airplane_creation_sets_status(self):
        """Тест: создание самолета устанавливает статус"""
        airplane = Airplane.objects.create(
            airline=self.airline,
            serial_number='SN123456',
            airplane_model=self.airplane_model,
            status='Active'
        )
        self.assertEqual(airplane.status, 'Active')

    def test_airplane_string_representation(self):
        """Тест: строковое представление самолета"""
        airplane = Airplane.objects.create(
            airline=self.airline,
            serial_number='SN123456',
            airplane_model=self.airplane_model,
            status='Active'
        )
        self.assertEqual(str(airplane), 'SN123456 (Boeing 737)')