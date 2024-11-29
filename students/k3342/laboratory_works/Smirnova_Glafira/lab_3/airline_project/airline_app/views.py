from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


class AirlinesAPIView(APIView):
    """
    Handles listing all airlines and creating a new airline.
    """

    serializer_class = AirlineCreateSerializer

    def get(self, request):
        airlines = Airline.objects.all()
        serializer = AirlineSerializer(airlines, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        serializer_for_writing = self.serializer_class(data=request.data)
        serializer_for_writing.is_valid(raise_exception=True)
        serializer_for_writing.save()
        return Response(data=serializer_for_writing.data, status=status.HTTP_201_CREATED)


class AirlineAPIView(APIView):
    """
    Handles retrieving, updating, and deleting a specific airline.
    """

    def get(self, request, pk=None):
        airline = Airline.objects.get(pk=pk)
        serializer = AirlineSerializer(airline)
        return Response(serializer.data)

    def delete(self, request, pk):
        airline = Airline.objects.get(pk=pk)
        airline.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(request_body=AirlineCreateSerializer)
    def patch(self, request, pk):
        try:
            airline = Airline.objects.get(pk=pk)
        except Airline.DoesNotExist:
            return Response({"error": "Airline not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AirlineCreateSerializer(airline, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlanesAPIView(APIView):
    """
    Handles listing all planes or planes associated with a specific airline, and creating a new plane for a specific airline.
    """

    serializer_class = PlaneCreateSerializer

    def get(self, request, airline_pk=None):
        if airline_pk:
            planes = Plane.objects.filter(airline_id=airline_pk)
            serializer = PlaneSerializer(planes, many=True)
            return Response(serializer.data)
        planes = Plane.objects.all()
        serializer = PlaneSerializer(planes, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, airline_pk=None):
        if not airline_pk:
            return Response(
                {"error": "to add a new plane please go to airlines/<int:airline_pk>/planes."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            airline = Airline.objects.get(pk=airline_pk)
        except Airline.DoesNotExist:
            return Response(
                {"error": "Airline not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        plane = serializer.save(airline=airline)
        return Response(PlaneSerializer(plane).data, status=status.HTTP_201_CREATED)


class PlaneAPIView(APIView):
    """
    Handles retrieving, updating, and deleting a specific plane.
    """

    def get(self, request, airline_pk=None, pk=None):
        plane = Plane.objects.get(pk=pk)
        serializer = PlaneSerializer(plane)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PlaneCreateSerializer)
    def patch(self, request, airline_pk=None, pk=None):
        try:
            plane = Plane.objects.get(pk=pk)
        except Plane.DoesNotExist:
            return Response({"error": "Plane not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlaneCreateSerializer(plane, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, airline_pk=None, pk=None):
        plane = Plane.objects.get(pk=pk)
        plane.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeesAPIView(APIView):
    """
    Handles listing all employees or employees associated with a specific airline, and creating a new employee for a specific airline.
    """

    serializer_class = EmployeeCreateSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, airline_pk=None):
        if airline_pk:
            employees = Employee.objects.filter(employer_id=airline_pk)
            serializer = EmployeeSerializer(employees, many=True)
            return Response(serializer.data)
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, airline_pk):
        if not airline_pk:
            return Response(
                {"error": "to add a new employee please go to airlines/<int:airline_pk>/employees."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            airline = Airline.objects.get(pk=airline_pk)
        except Airline.DoesNotExist:
            return Response(
                {"error": "Airline not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        employee = serializer.save(employer=airline)
        return Response(EmployeeSerializer(employee).data, status=status.HTTP_201_CREATED)


class EmployeeAPIView(APIView):
    """
    Handles retrieving, updating, and deleting a specific employee.
    """

    def get(self, request, airline_pk=None, pk=None):
        employee = Employee.objects.get(pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=EmployeeCreateSerializer)
    def patch(self, request, airline_pk=None, pk=None):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeCreateSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, airline_pk=None, pk=None):
        employee = Employee.objects.get(pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FlightsAPIView(APIView):
    """
    Handles listing all flights or flights associated with a specific airline, and creating a new flight.
    """

    serializer_class = FlightCreateSerializer

    def get(self, request, airline_pk=None):
        if airline_pk:
            flights = Flight.objects.filter(plane__airline_id=airline_pk)
            serializer = FlightSerializer(flights, many=True)
            return Response(serializer.data)
        flights = Flight.objects.all()
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, airline_pk=None):
        if airline_pk:
            try:
                airline = Airline.objects.get(pk=airline_pk)
            except Airline.DoesNotExist:
                return Response(
                    {"error": "Airline not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FlightAPIView(APIView):
    """
    Handles retrieving, updating, and deleting a specific flight.
    """

    def get(self, request, airline_pk=None, pk=None):
        flight = Flight.objects.get(pk=pk)
        serializer = FlightSerializer(flight)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=FlightCreateSerializer)
    def patch(self, request, airline_pk=None, pk=None):
        try:
            flight = Flight.objects.get(pk=pk)
        except Flight.DoesNotExist:
            return Response({"error": "Flight not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FlightCreateSerializer(flight, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, airline_pk=None, pk=None):
        flight = Flight.objects.get(pk=pk)
        flight.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MaintenancesAPIView(APIView):
    """
    Handles listing all maintenances and creating a new maintenance.
    """

    serializer_class = MaintenanceCreateSerializer

    def get(self, request):
        maintenances = Maintenance.objects.all()
        serializer = MaintenanceSerializer(maintenances, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MaintenanceAPIView(APIView):
    """
    Handles retrieving, updating, and deleting a specific maintenance.
    """

    def get(self, request, pk):
        maintenance = get_object_or_404(Maintenance, pk=pk)
        serializer = MaintenanceSerializer(maintenance)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=MaintenanceCreateSerializer)
    def patch(self, request, pk):
        maintenance = get_object_or_404(Maintenance, pk=pk)
        serializer = MaintenanceCreateSerializer(maintenance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        maintenance = get_object_or_404(Maintenance, pk=pk)
        maintenance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SeatsAPIView(APIView):
    """
    Handles listing all seats for a specific flight.
    """

    serializer_class = SeatSellSerializer

    def get(self, request, flight_pk):
        try:
            flight = Flight.objects.get(pk=flight_pk)
        except Flight.DoesNotExist:
            return Response({"error": "Flight not found."}, status=status.HTTP_404_NOT_FOUND)

        seats = Seat.objects.filter(flight=flight)
        serializer = SeatListSerializer(seats, many=True)
        return Response(serializer.data)


class FlightSeatAvailabilityAPIView(APIView):
    """
    Handles retrieving seat availability for a specific flight.
    """

    def get(self, request, flight_id):
        flight = Flight.objects.get(id=flight_id)
        serializer = FlightSeatAvailabilitySerializer(flight)
        return Response(serializer.data)


class SeatSellAPIView(APIView):
    """
    Handles selling a seat for a specific flight.
    """

    serializer_class = SeatSellSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, flight_pk):
        try:
            flight = Flight.objects.get(pk=flight_pk)
        except Flight.DoesNotExist:
            return Response({"error": "Flight not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data, context={'flight': flight})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": f"Seat {serializer.validated_data['number']} has been sold."},
            status=status.HTTP_200_OK
        )


class RoutesAPIView(APIView):
    """
    Handles listing all routes and creating a new route.
    """

    def get(self, request):
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=RouteCreateSerializer)
    def post(self, request):
        serializer = RouteCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RouteAPIView(APIView):
    """
    Handles retrieving, updating, and deleting a specific route.
    """

    def get(self, request, pk):
        route = Route.objects.get(pk=pk)
        serializer = RouteSerializer(route)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=RouteCreateSerializer)
    def patch(self, request, pk=None):
        try:
            route = Route.objects.get(pk=pk)
        except Route.DoesNotExist:
            return Response({"error": "Route not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = RouteCreateSerializer(route, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        route = Route.objects.get(pk=pk)
        route.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FlightTransitStopsAPIView(APIView):
    """
    Handles listing transit stops for a specific flight and adding new transit stop details.
    """

    serializer_class = TransitStopCreateSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, pk):
        try:
            flight = Flight.objects.get(pk=pk)
        except Flight.DoesNotExist:
            return Response({"error": "Flight not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data, context={'flight': flight})
        serializer.is_valid(raise_exception=True)
        transit_stop = serializer.save(flight=flight)
        return Response(TransitStopCreateSerializer(transit_stop).data, status=status.HTTP_201_CREATED)

    def get(self, request, pk):
        try:
            flight = Flight.objects.get(pk=pk)
        except Flight.DoesNotExist:
            return Response({"error": "Flight not found."}, status=status.HTTP_404_NOT_FOUND)

        route_stops = flight.route.stops.all()

        if not route_stops:
            return Response({"message": "This route has no transit stops."})

        stops_data = []
        for stop in route_stops:
            transit_stop = TransitStop.objects.filter(flight=flight, airport=stop).first()
            if transit_stop:
                stops_data.append({
                    "airport": str(stop),
                    "arrival_datetime": transit_stop.arrival_datetime,
                    "departure_datetime": transit_stop.departure_datetime
                })
            else:
                stops_data.append({
                    "airport": str(stop),
                    "message": f"For the stop {stop.city}, no details were provided."
                })

        return Response(stops_data)


class CrewMembersAPIView(APIView):
    """
    Handles listing all crew members and creating a new crew member.
    """

    serializer_class = CrewMemberCreateSerializer

    def get(self, request):
        crew_members = CrewMember.objects.all()
        serializer = CrewMemberFullSerializer(crew_members, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CrewsAPIView(APIView):
    """
    Handles listing all crews and creating a new crew.
    """

    serializer_class = CrewCreateSerializer

    def get(self, request):
        crews = Crew.objects.all()
        serializer = CrewSerializer(crews, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# statistics api views
class MostFrequentPlaneAPIView(APIView):
    """
    Handles retrieving the most frequently used plane for a specific route.
    """

    def get(self, request, route_id):
        data = {'route_id': route_id}
        serializer = MostFrequentPlaneSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class UnderFilledRoutesAPIView(APIView):
    """
    Handles retrieving routes with passenger occupancy below a given threshold.
    """

    def get(self, request):
        threshold = float(request.query_params.get('threshold', 50))
        routes = Route.objects.all()
        serializer = UnderFilledRouteSerializer(routes, many=True, context={'threshold': threshold})
        return Response(serializer.data)


class PlanesInMaintenanceAPIView(APIView):
    """
    Handles listing all planes currently under maintenance.
    """

    def get(self, request):
        serializer = PlanesInMaintenanceSerializer({})
        return Response(serializer.data)


class AirlineEmployeesCountAPIView(APIView):
    """
    Handles retrieving the number of employees working for a specific airline.
    """

    def get(self, request, airline_id):
        airline = Airline.objects.get(id=airline_id)
        serializer = AirlineEmployeesCountSerializer(airline)
        return Response(serializer.data)


# additional views
class AvailableSeatsAPIView(APIView):
    """
    Handles retrieving all available seats for a specific flight.
    """

    def get(self, request, pk):
        flight = Flight.objects.get(pk=pk)
        available_seats = flight.seats.filter(is_sold=False)
        seat_numbers = [seat.number for seat in available_seats]
        return Response({"available_seats": seat_numbers, "count": available_seats.count()})


class FlightsByAirlineAPIView(APIView):
    """
    Handles retrieving all flights operated by a specific airline.
    """

    def get(self, request, airline_id):
        flights = Flight.objects.filter(plane__airline_id=airline_id)
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)


class FlightsByAirportAPIView(APIView):
    """
    Handles retrieving all flights departing from or arriving at a specific airport.
    """

    def get(self, request, airport_code):
        routes = Route.objects.filter(
            departure_airport__code=airport_code
        ) | Route.objects.filter(destination_airport__code=airport_code)
        flights = Flight.objects.filter(route__in=routes)
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)


class EmployeesByAirlineAPIView(APIView):
    """
    Handles retrieving the number of employees for a specific airline.
    """

    def get(self, request, airline_id):
        employees = Employee.objects.filter(employer_id=airline_id).count()
        return Response({"employees_count": employees})


class FlightsWithTransitStopsAPIView(APIView):
    """
    Handles retrieving all flights that have transit stops.
    """

    def get(self, request):
        flights = Flight.objects.filter(transitstop__isnull=False).distinct()
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)


class PlaneStatisticsAPIView(APIView):
    """
    Handles retrieving statistical information about planes for a specific airline.
    """

    def get(self, request, pk):
        try:
            airline = Airline.objects.get(pk=pk)
        except Airline.DoesNotExist:
            return Response({"error": "Airline not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlaneStatisticsSerializer(airline)
        return Response(serializer.data)
