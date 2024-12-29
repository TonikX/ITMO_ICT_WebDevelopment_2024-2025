from django.db.models import Count, F
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Airline, AircraftType, Airplane, Route, Flight, TransitStop,
    Employee, Crew, CrewEmployee, FlightInstance
)
from .serializers import (
    AirlineSerializer, AircraftTypeSerializer, AirplaneSerializer, RouteSerializer,
    FlightSerializer, TransitStopSerializer, EmployeeSerializer, CrewSerializer,
    CrewEmployeeSerializer, FlightInstanceSerializer
)


class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer


class AircraftTypeViewSet(viewsets.ModelViewSet):
    queryset = AircraftType.objects.all()
    serializer_class = AircraftTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class TransitStopViewSet(viewsets.ModelViewSet):
    queryset = TransitStop.objects.all()
    serializer_class = TransitStopSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class CrewEmployeeViewSet(viewsets.ModelViewSet):
    queryset = CrewEmployee.objects.all()
    serializer_class = CrewEmployeeSerializer


class FlightInstanceViewSet(viewsets.ModelViewSet):
    queryset = FlightInstance.objects.all()
    serializer_class = FlightInstanceSerializer


class MostCommonAircraftByRouteView(APIView):
    def get(self, request, *args, **kwargs):
        airplane_counts = Airplane.objects.annotate(flight_count=Count('flights')).order_by('-flight_count')

        if airplane_counts:
            most_common_aircraft = airplane_counts[0]
            return Response(AirplaneSerializer(most_common_aircraft).data)
        return Response({"detail": "No data found."})


class LowCapacityFlightsView(APIView):
    def get(self, request, *args, **kwargs):
        threshold_percentage = int(request.query_params.get('threshold', 50))
        low_capacity_flights = FlightInstance.objects.filter(
            seats_sold__lt=(threshold_percentage / 100) * F('flight__airplane__seats')
        )

        flights = Flight.objects.filter(id__in=low_capacity_flights.values('flight_id'))
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)

class AvailableSeatsView(APIView):
    def get(self, request, *args, **kwargs):
        flight_instance_id = request.GET.get('flight_instance_id')
        if not flight_instance_id:
            return Response({"detail": "Flight instance ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        flight_instance = get_object_or_404(FlightInstance, id=flight_instance_id)
        total_seats = flight_instance.flight.airplane.seats
        seats_sold = flight_instance.seats_sold
        available_seats = total_seats - seats_sold

        return Response(
            {
                "flight_number": flight_instance.flight.flight_number,
                "total_seats": total_seats,
                "seats_sold": seats_sold,
                "available_seats": available_seats
            },
            status=status.HTTP_200_OK
        )


class AircraftInRepairView(APIView):
    def get(self, request, *args, **kwargs):
        airplanes_in_repair = Airplane.objects.filter(is_in_repair=True).count()
        return Response({"airplanes_in_repair": airplanes_in_repair})


class EmployeesCountView(APIView):
    def get(self, request, *args, **kwargs):
        airline_id = request.query_params.get('airline_id')
        if airline_id:
            employees_count = Employee.objects.filter(airline_id=airline_id).count()
            return Response({"employees_count": employees_count})
        return Response({"detail": "Airline ID is required."}, status=400)