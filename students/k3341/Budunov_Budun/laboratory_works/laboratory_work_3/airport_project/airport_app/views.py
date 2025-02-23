from rest_framework import viewsets, generics, mixins
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from .permissions import IsAdminUser, IsCrewUser, IsAdminOrReadOnly, IsOwner
from .models import *
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser

class UserAvatarUpdateView(generics.UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsOwner]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class RegisterUserView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer

class LoginUserView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# Простые ViewSets для CRUD операций
# GET /airline/ - Получить список авиакомпаний
# POST /airline/ - Создать авиакомпанию
# GET /airline/{id}/ - Получить авиакомпанию
# PUT /airline/{id}/ - Обновить авиакомпанию
# DELETE /airline/{id}/ - Удалить авиакомпанию
class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = [IsAdminOrReadOnly]


    # GET /airline/{id}/airplanes/ - Получить список самолетов данной авиакомпании
    @action(detail=True, methods=['get'], permission_classes = [IsAdminUser])
    def airplanes(self, request, pk=None):
        airline = self.get_object()
        airplanes = Airplane.objects.filter(airline=airline)
        serializer = AirplaneSerializer(airplanes, many=True)
        return Response(serializer.data)

    # GET /airline/{id}/employees/ - Получить список сотрудников данной авиакомпании
    @action(detail=True, methods=['get'], permission_classes = [IsAdminUser])
    def employees(self, request, pk=None):
        airline = self.get_object()
        employees = Employee.objects.filter(airline=airline)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

# GET /airport/ - Получить список аэропортов
# POST /airport/ - Создать аэропорт
# GET /airport/{id}/ - Получить аэропорт
# PUT /airport/{id}/ - Обновить аэропорт
# DELETE /airport/{id}/ - Удалить аэропорт
class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAdminOrReadOnly]


    # GET /airport/{id}/flights/ - Получить список рейсов, связанных с аэропортом
    @action(detail=True, methods=['get'], permission_classes = [IsAdminUser])
    def flights(self, request, pk=None):
        airport = self.get_object()
        routes = Route.objects.filter(departure_airport=airport) | Route.objects.filter(arrival_airport=airport)
        flights = Flight.objects.filter(route__in=routes)
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)

# GET /airplane/ - Получить список самолетов
# POST /airplane/ - Создать самолет
# GET /airplane/{id}/ - Получить самолет
# PUT /airplane/{id}/ - Обновить самолет
# DELETE /airplane/{id}/ - Удалить самолет
class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = [IsAdminOrReadOnly]


    # GET /airplane/{id}/maintenance/ - Получить историю технического обслуживания самолета
    @action(detail=True, methods=['get'], permission_classes = [IsAdminUser])
    def maintenance(self, request, pk=None):
        airplane = self.get_object()
        maintenance_records = AirplaneMaintenance.objects.filter(airplane=airplane)
        serializer = AirplaneMaintenanceSerializer(maintenance_records, many=True)
        return Response(serializer.data)

# GET /route/ - Получить список маршрутов
# POST /route/ - Создать маршрут
# GET /route/{id}/ - Получить маршрут
# PUT /route/{id}/ - Обновить маршрут
# DELETE /route/{id}/ - Удалить маршрут
class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAdminOrReadOnly]


    # GET /route/{id}/flights/ - Получить список рейсов по этому маршруту
    @action(detail=True, methods=['get'], permission_classes = [IsAdminUser])
    def flights(self, request, pk=None):
        route = self.get_object()
        flights = Flight.objects.filter(route=route)
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)

    # GET /route/by_airline/?airline_id={id} - Получить все маршруты авиакомпании
    @action(detail=False, methods=['get'], permission_classes = [IsAdminUser])
    def by_airline(self, request):
        airline_id = request.query_params.get('airline_id')
        routes = Route.objects.filter(airline_id=airline_id)
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)

# GET /flight/ - Получить список рейсов
# POST /flight/ - Создать рейс
# GET /flight/{id}/ - Получить рейс
# PUT /flight/{id}/ - Обновить рейс
# DELETE /flight/{id}/ - Удалить рейс
class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAdminOrReadOnly]


    # GET /flight/by_airport/?departure={id}&arrival={id} - Поиск рейсов по аэропорту
    @action(detail=False, methods=['get'], permission_classes = [IsAdminUser])
    def by_airport(self, request):
        departure_id = request.query_params.get('departure')
        arrival_id = request.query_params.get('arrival')
        flights = Flight.objects.all()
        if departure_id:
            flights = flights.filter(route__departure_airport_id=departure_id)
        if arrival_id:
            flights = flights.filter(route__arrival_airport_id=arrival_id)
        serializer = self.get_serializer(flights, many=True)
        return Response(serializer.data)

    # GET /flight/by_date/?date=YYYY-MM-DD - Получить список рейсов по дате
    @action(detail=False, methods=['get'], permission_classes = [IsAdminUser])
    def by_date(self, request):
        date = request.query_params.get('date')
        flights = Flight.objects.filter(departure_time__date=date)
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)

    # GET /flight/by_airline/?airline_id={id} - Получить список рейсов по авиакомпании
    @action(detail=False, methods=['get'], permission_classes = [IsAdminUser])
    def by_airline(self, request):
        airline_id = request.query_params.get('airline_id')
        flights = Flight.objects.filter(route__airline_id=airline_id)
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)

    # GET /flight/{id}/crews/ - Получить список экипажей для рейса
    @action(detail=True, methods=['get'], permission_classes = [IsAdminUser])
    def crews(self, request, pk=None):
        flight = self.get_object()
        crews = Crew.objects.filter(flight=flight)
        serializer = CrewSerializer(crews, many=True)
        return Response(serializer.data)
    
    # GET /flight/{id}/full_info/ - Получить полную информацию о рейсе, включая транзиты
    @action(detail=True, methods=['get'], permission_classes = [IsAdminUser])
    def full_info(self, request, pk=None):
        flight = self.get_object()
        route = flight.route
        transits = Transit.objects.filter(route=route)
        serializer = TransitSerializer(transits, many=True)
        return Response({'flight': FlightSerializer(flight).data, 'transits': serializer.data})


# GET /employee/ - Получить список сотрудников
# POST /employee/ - Создать сотрудника
# GET /employee/{id}/ - Получить сотрудника
# PUT /employee/{id}/ - Обновить сотрудника
# DELETE /employee/{id}/ - Удалить сотрудника
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrReadOnly]


    # GET /employee/by_position/?position={name} - Получить список сотрудников по должности
    @action(detail=False, methods=['get'], permission_classes = [IsAdminUser])
    def by_position(self, request):
        position = request.query_params.get('position')
        employees = Employee.objects.filter(position=position)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

# GET /crew/ - Получить список экипажей
# POST /crew/ - Создать экипаж
# GET /crew/{id}/ - Получить экипаж
# PUT /crew/{id}/ - Обновить экипаж
# DELETE /crew/{id}/ - Удалить экипаж
class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = [IsAdminOrReadOnly]


# GET /crew_member/ - Получить список членов экипажей
# POST /crew_member/ - Создать члена экипажа
# GET /crew_member/{id}/ - Получить члена экипажа
# PUT /crew_member/{id}/ - Обновить члена экипажа
# DELETE /crew_member/{id}/ - Удалить члена экипажа
class CrewMemberViewSet(viewsets.ModelViewSet):
    queryset = CrewMember.objects.all()
    serializer_class = CrewMemberSerializer
    permission_classes = [IsAdminOrReadOnly]

# GET /airplane_maintenance/ - Получить список записей о ТО самолетов
# POST /airplane_maintenance/ - Добавить запись о ТО
# GET /airplane_maintenance/{id}/ - Получить запись о ТО
# PUT /airplane_maintenance/{id}/ - Обновить запись о ТО
# DELETE /airplane_maintenance/{id}/ - Удалить запись о ТО
class AirplaneMaintenanceViewSet(viewsets.ModelViewSet):
    queryset = AirplaneMaintenance.objects.all()
    serializer_class = AirplaneMaintenanceSerializer
    permission_classes = [IsAdminOrReadOnly]


    # GET /airplane_maintenance/by_date/?start={YYYY-MM-DD}&end={YYYY-MM-DD} - Получить историю ТО самолетов по диапазону дат
    @action(detail=False, methods=['get'], permission_classes = [IsAdminUser])
    def by_date(self, request):
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')
        maintenance_records = AirplaneMaintenance.objects.filter(date__range=[start_date, end_date])
        serializer = AirplaneMaintenanceSerializer(maintenance_records, many=True)
        return Response(serializer.data)
    
    # GET /airplane_maintenance/history/?airplane_id={id} - Получить историю ТО самолета
    @action(detail=False, methods=['get'], permission_classes = [IsAdminUser])
    def history(self, request):
        airplane_id = request.query_params.get('airplane_id')
        maintenance_records = AirplaneMaintenance.objects.filter(airplane_id=airplane_id)
        serializer = AirplaneMaintenanceSerializer(maintenance_records, many=True)
        return Response(serializer.data)

# GET /airplane_model/ - Получить список всех моделей и информации о них
# POST /airplane_model/ 
# GET /airplane_model/{id}/
# PUT /airplane_model/{id}/
# DELETE /airplane_model/{id}/
class AirplaneModelViewSet(viewsets.ModelViewSet):
    queryset = AirplaneModel.objects.all()
    serializer_class = AirplaneModelSerializer
    permission_classes = [IsAdminOrReadOnly]

# GET /transit/ - Получить список транзитов и полную инфу о каждом
# POST /transit/
# GET /transit/{id}/
# PUT /transit/{id}/
# DELETE /transit/{id}/
class TransitViewSet(viewsets.ModelViewSet):
    queryset = Transit.objects.all()
    serializer_class = TransitSerializer
    permission_classes = [IsAdminOrReadOnly]
