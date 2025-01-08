from collections import defaultdict
from datetime import datetime

from django.db.models import Count
from django.utils import timezone
from rest_framework import serializers
from .models import *
from django.utils.timezone import now


class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__'


class AirlineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = ["name", "country", "contact_info"]


class UserSerializer(serializers.ModelSerializer):
    airline = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'airline']


class PlaneModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaneModel
        fields = '__all__'


class PlaneSerializer(serializers.ModelSerializer):
    airline = serializers.StringRelatedField()
    model = PlaneModelSerializer()
    plane_str = serializers.SerializerMethodField()

    class Meta:
        model = Plane
        fields = '__all__'

    def get_plane_str(self, obj):
        return str(obj)


class PlaneCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = ["number", "model"]


class PlaneUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = ["number"]


class EmployeeSerializer(serializers.ModelSerializer):
    employer = serializers.StringRelatedField()
    crew_roles = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = '__all__'

    def get_crew_roles(self, obj):
        roles = obj.crew_roles.all()
        roles = [role.role for role in roles]
        return roles


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ["employer"]


class EmployeeNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'work_experience_years']


class CrewMemberSerializer(serializers.ModelSerializer):
    employee = EmployeeNestedSerializer()

    class Meta:
        model = CrewMember
        fields = ['employee']


class CrewMemberFullSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()

    class Meta:
        model = CrewMember
        fields = '__all__'


class CrewMemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewMember
        fields = ['employees', 'role']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Dropdown list for employees
        rep['employee_choices'] = [
            {"id": emp.id, "name": str(emp)} for emp in Employee.objects.all()
        ]
        # Dropdown list for roles
        rep['role_choices'] = [
            {"value": role[0], "display_name": role[1]} for role in CrewMember._meta.get_field('role').choices
        ]
        return rep

    def validate(self, data):
        instance = self.instance

        employee = data.get('employees', instance.employee if instance else None)
        role = data.get('role', instance.role if instance else None)

        if CrewMember.objects.filter(employee=employee, role=role).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("This crew member with the specified role already exists.")

        return data


class TransitStopSerializer(serializers.ModelSerializer):
    airport = serializers.StringRelatedField()

    class Meta:
        model = TransitStop
        exclude = ['route']


class RouteSerializer(serializers.ModelSerializer):
    departure_airport = serializers.StringRelatedField()
    destination_airport = serializers.StringRelatedField()
    stops = serializers.SerializerMethodField()
    route_str = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = '__all__'

    def get_stops(self, obj):
        """
        Dynamically include all transit stops for the route, using TransitStopSerializer.
        """
        stops = obj.transit_stops.all().order_by('arrival_day', 'arrival_time')
        return TransitStopSerializer(stops, many=True).data

    def get_route_str(self, obj):
        """
        Dynamically include all transit stops for the route, using TransitStopSerializer.
        """
        return str(obj)


class RouteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        exclude = ['id']

    def validate(self, data):

        instance = self.instance

        departure_airport = data.get('departure_airport', instance.departure_airport if instance else None)
        destination_airport = data.get('destination_airport', instance.destination_airport if instance else None)
        departure_time = data.get('departure_time', instance.departure_time if instance else None)
        arrival_time = data.get('arrival_time', instance.arrival_time if instance else None)
        arrival_day = data.get('arrival_day', instance.arrival_day if instance else None)
        regularity = data.get('regularity', instance.regularity if instance else None)

        if departure_airport == destination_airport:
            raise serializers.ValidationError("Departure and destination airports must be different.")

        if arrival_day == 0 and departure_time and arrival_time and departure_time >= arrival_time:
            raise serializers.ValidationError(
                "Departure time must be earlier than arrival time when arrival day is the same.")

        query = Route.objects.filter(
            departure_airport=departure_airport,
            destination_airport=destination_airport,
            departure_time=departure_time,
            arrival_time=arrival_time,
            arrival_day=arrival_day,
            regularity=regularity,
        )
        if instance:
            query = query.exclude(id=instance.id)

        if query.exists():
            raise serializers.ValidationError("A route with the same details already exists.")

        return data


class RouteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['number', 'distance_km', 'regularity', 'departure_time', 'arrival_time']

    def validate(self, data):
        instance = self.instance

        departure_time = data.get('departure_time', instance.departure_time if instance else None)
        arrival_time = data.get('arrival_time', instance.arrival_time if instance else None)
        arrival_day = instance.arrival_day

        if arrival_day == 0 and departure_time and arrival_time and departure_time >= arrival_time:
            raise serializers.ValidationError("Departure time must be earlier than arrival time when arrival day is "
                                              "the same.")

        query = Route.objects.filter(
            number=data.get('number', instance.number),
            departure_time=departure_time,
            arrival_time=arrival_time,
            regularity=data.get('regularity', instance.regularity),
        )
        if instance:
            query = query.exclude(id=instance.id)

        if query.exists():
            raise serializers.ValidationError("A route with the same details already exists.")

        return data


class CrewSerializer(serializers.ModelSerializer):
    captain = CrewMemberSerializer()
    co_pilot = CrewMemberSerializer()
    navigator = CrewMemberSerializer()
    attendants = CrewMemberSerializer(many=True)

    class Meta:
        model = Crew
        fields = '__all__'


class CrewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ['captain', 'co_pilot', 'navigator', 'attendants']

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        # Dropdown lists for crew roles, correctly filtering by role
        rep['captain_choices'] = [
            {"id": member.id, "name": f"{member.employee} ({member.role})"}
            for member in CrewMember.objects.filter(role='Captain')
        ]
        rep['co_pilot_choices'] = [
            {"id": member.id, "name": f"{member.employee} ({member.role})"}
            for member in CrewMember.objects.filter(role='Co-Pilot')
        ]
        rep['navigator_choices'] = [
            {"id": member.id, "name": f"{member.employee} ({member.role})"}
            for member in CrewMember.objects.filter(role='Navigator')
        ]
        rep['attendant_choices'] = [
            {"id": member.id, "name": f"{member.employee} ({member.role})"}
            for member in CrewMember.objects.filter(role='Attendant')
        ]

        return rep

    def validate(self, data):
        instance = self.instance

        captain = data.get('captain', instance.captain if instance else None)
        co_pilot = data.get('co_pilot', instance.co_pilot if instance else None)
        navigator = data.get('navigator', instance.navigator if instance else None)
        attendants = data.get('attendants', instance.attendants.all() if instance else None)

        if captain and captain.role != 'Captain':
            raise serializers.ValidationError("Selected captain must have the 'Captain' role.")
        if co_pilot and co_pilot.role != 'Co-Pilot':
            raise serializers.ValidationError("Selected co-pilot must have the 'Co-Pilot' role.")
        if navigator and navigator.role != 'Navigator':
            raise serializers.ValidationError("Selected navigator must have the 'Navigator' role.")
        if attendants:
            for attendant in attendants:
                if attendant.role != 'Attendant':
                    raise serializers.ValidationError(f"{attendant.employee} does not have the 'Attendant' role.")

        # Check for existing crew with identical members
        existing_crew = Crew.objects.filter(
            captain=captain,
            co_pilot=co_pilot,
            navigator=navigator
        ).exclude(pk=instance.pk if instance else None)

        if existing_crew.exists():
            for crew in existing_crew:
                existing_attendants = set(crew.attendants.all())
                new_attendants = set(attendants)
                if existing_attendants == new_attendants:
                    raise serializers.ValidationError("A crew with identical members already exists.")

        return data


class FlightShortSerializer(serializers.ModelSerializer):
    crew = serializers.StringRelatedField()
    route = serializers.StringRelatedField()
    stops = serializers.SerializerMethodField()
    plane = serializers.StringRelatedField()
    departure_time = serializers.SerializerMethodField()
    arrival_time = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = '__all__'

    def get_stops(self, obj):
        stops = obj.route.transit_stops.all().order_by('arrival_day', 'arrival_time')
        stops = [str(stop.airport) for stop in stops]
        return stops

    def get_departure_time(self, obj):
        return obj.route.departure_time

    def get_arrival_time(self, obj):
        return obj.route.arrival_time


class FlightSerializer(serializers.ModelSerializer):
    crew = serializers.StringRelatedField()
    route = RouteSerializer()
    plane = PlaneSerializer()

    class Meta:
        model = Flight
        fields = '__all__'


class FlightCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        exclude = ["arrival_date", "sold_tickets_number"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['crew_choices'] = [{"id": crew.id, "name": str(crew)} for crew in Crew.objects.all()]
        rep['route_choices'] = [{"id": route.id, "name": str(route)} for route in Route.objects.all()]
        rep['plane_choices'] = [{"id": plane.id, "name": str(plane)} for plane in Plane.objects.all()]
        return rep

    def validate(self, data):
        """
        Custom validation for plane, crew, and schedule conflicts.
        """
        plane = data['plane']
        crew = data['crew']
        departure_date = data['departure_date']
        arrival_date = departure_date + timedelta(days=data['route'].arrival_day or 0)

        arrival_datetime = datetime.combine(arrival_date, datetime.min.time())
        departure_datetime = datetime.combine(departure_date, datetime.min.time())
        arrival_datetime = timezone.make_aware(arrival_datetime)
        departure_datetime = timezone.make_aware(departure_datetime)

        overlapping_maintenances = Maintenance.objects.filter(
            plane=plane,
            start_date__lte=arrival_datetime,
            end_date__gte=departure_datetime
        )
        if overlapping_maintenances.exists():
            maintenance = overlapping_maintenances.first()
            raise serializers.ValidationError(
                {"plane": f"Plane {plane.number} is under maintenance from {maintenance.start_date} "
                          f"to {maintenance.end_date or 'an unknown end date'}."}
            )

        overlapping_flights_plane = Flight.objects.filter(
            plane=plane,
            departure_date__lte=arrival_date,
            arrival_date__gte=departure_date
        )
        if overlapping_flights_plane.exists():
            flight = overlapping_flights_plane.first()
            raise serializers.ValidationError(
                {"plane": f"Plane {plane.number} is occupied by another flight ({flight.number}) "
                          f"from {flight.departure_date} to {flight.arrival_date}."}
            )

        overlapping_flights_crew = Flight.objects.filter(
            crew=crew,
            departure_date__lte=arrival_date,
            arrival_date__gte=departure_date
        )
        if overlapping_flights_crew.exists():
            flight = overlapping_flights_crew.first()
            raise serializers.ValidationError(
                {"crew": f"Crew {crew} is occupied by another flight ({flight.number}) "
                         f"from {flight.departure_date} to {flight.arrival_date}."}
            )

        return data

    def create(self, validated_data):
        """
        Create a flight and generate seats based on the plane's seat capacity.
        """
        flight = Flight.objects.create(**validated_data)
        plane = flight.plane

        rows = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        capacity = plane.model.seats_capacity
        row_count = (capacity // 3) + (1 if capacity % 3 != 0 else 0)
        seat_count = 0

        for row in rows[:row_count]:
            for col in range(1, 4):
                if seat_count >= capacity:
                    break
                seat_number = f"{row}{col}"
                Seat.objects.create(number=seat_number, flight=flight)
                seat_count += 1

        return flight


class FlightPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        exclude = ["route", "arrival_date", "sold_tickets_number"]

    def validate(self, data):
        """
        Custom validation for plane, crew, and schedule conflicts in partial updates.
        """

        instance = self.instance

        plane = data.get('plane', instance.plane)
        crew = data.get('crew', instance.crew)
        departure_date = data.get('departure_date', instance.departure_date)
        arrival_date = departure_date + timedelta(days=instance.route.arrival_day or 0)

        arrival_datetime = datetime.combine(arrival_date, datetime.min.time())
        departure_datetime = datetime.combine(departure_date, datetime.min.time())
        arrival_datetime = timezone.make_aware(arrival_datetime)
        departure_datetime = timezone.make_aware(departure_datetime)

        overlapping_maintenances = Maintenance.objects.filter(
            plane=plane,
            start_date__lte=arrival_datetime,
            end_date__gte=departure_datetime
        )
        if overlapping_maintenances.exists():
            maintenance = overlapping_maintenances.first()
            raise serializers.ValidationError(
                {"departure_date": f"Plane {plane.number} is under maintenance from {maintenance.start_date} "
                          f"to {maintenance.end_date or 'an unknown end date'}."}
            )

        overlapping_flights_plane = Flight.objects.filter(
            plane=plane,
            departure_date__lte=arrival_date,
            arrival_date__gte=departure_date
        ).exclude(id=instance.id)
        if overlapping_flights_plane.exists():
            flight = overlapping_flights_plane.first()
            raise serializers.ValidationError(
                {"departure_date": f"Plane {plane.number} is occupied by another flight ({flight.number}) "
                          f"from {flight.departure_date} to {flight.arrival_date}."}
            )

        if crew:
            overlapping_flights_crew = Flight.objects.filter(
                crew=crew,
                departure_date__lte=arrival_date,
                arrival_date__gte=departure_date
            ).exclude(id=instance.id)
            if overlapping_flights_crew.exists():
                flight = overlapping_flights_crew.first()
                raise serializers.ValidationError(
                    {"departure_date": f"Crew {crew} is occupied by another flight ({flight.number}) "
                             f"from {flight.departure_date} to {flight.arrival_date}."}
                )

        return data


class SeatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['number', 'is_sold']


class SeatSellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['number']

    def validate(self, data):
        flight = self.context.get('flight')
        seat_number = data['number']
        seat = Seat.objects.filter(flight=flight, number=seat_number).first()
        if not seat:
            raise serializers.ValidationError("Seat not found.")
        if seat.is_sold:
            raise serializers.ValidationError("Seat is already sold.")
        return data

    def save(self, **kwargs):
        flight = self.context.get('flight')
        seat_number = self.validated_data['number']
        seat = Seat.objects.get(flight=flight, number=seat_number)
        seat.is_sold = True
        seat.save()
        flight.sold_tickets_number += 1
        flight.save()
        return seat


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'


class MaintenanceSerializer(serializers.ModelSerializer):
    plane = serializers.StringRelatedField()

    class Meta:
        model = Maintenance
        fields = '__all__'


class MaintenanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['plane_choices'] = [{"id": plane.id, "name": str(plane)} for plane in Plane.objects.all()]
        rep['status_choices'] = [
            {"value": choice[0], "display_name": choice[1]}
            for choice in Maintenance._meta.get_field('status').choices
        ]
        return rep

    def validate(self, data):
        """
        Custom validation for plane and schedule conflicts in partial updates.
        """
        instance = self.instance

        plane = data.get('plane', instance.plane if instance else None)
        start_date = data.get('start_date', instance.start_date if instance else None)
        end_date = data.get('end_date', instance.end_date if instance else None)

        if not (plane and start_date and end_date):
            return data

        overlapping_maintenances = Maintenance.objects.filter(
            plane=plane,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exclude(id=instance.id if instance else None)
        if overlapping_maintenances.exists():
            maintenance = overlapping_maintenances.first()
            raise serializers.ValidationError(
                {"start_date": f"Plane {plane.number} is under another maintenance from {maintenance.start_date} "
                          f"to {maintenance.end_date or 'an unknown end date'}."}
            )

            # Check if end_date is later than start_date
        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError(
                {"end_date": "End date must be later than the start date."}
            )

        # Validate overlapping flights for the plane
        overlapping_flights_plane = Flight.objects.filter(
            plane=plane,
            departure_date__lt=end_date,
            arrival_date__gt=start_date
        )
        if overlapping_flights_plane.exists():
            flight = overlapping_flights_plane.first()
            raise serializers.ValidationError(
                {"plane": f"Plane {plane.number} is occupied by a flight ({flight.number}) "
                          f"from {flight.departure_date} to {flight.arrival_date}."}
            )

        return data


class TransitStopCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransitStop
        fields = ['airport', 'arrival_time', 'arrival_day', 'departure_time', 'departure_day']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['airport_choices'] = [{"id": airport.id, "name": str(airport)} for airport in Airport.objects.all()]
        return rep

    def validate(self, data):
        route = self.context.get('route')

        # Retrieve route details
        dep_airport, dest_airport = route.departure_airport, route.destination_airport
        dep_time, arr_time, arr_day = route.departure_time, route.arrival_time, route.arrival_day

        if TransitStop.objects.filter(route=route, airport=data['airport']).exists():
            raise serializers.ValidationError("Transit stop for this airport already exists.")

        if data['airport'] == dep_airport or data['airport'] == dest_airport:
            raise serializers.ValidationError(
                "Transit stop airport must be different from both departure and destination airports of the route.")

        if data['arrival_day'] > data['departure_day']:
            raise serializers.ValidationError("Arrival day cannot be later than departure day.")

        if data['arrival_day'] == data['departure_day'] and data['arrival_time'] >= data['departure_time']:
            raise serializers.ValidationError("Arrival time must be earlier than departure time on the same day.")

        if not (arr_day <= data['arrival_day'] <= data['departure_day'] <= arr_day):
            raise serializers.ValidationError("Transit times must be within the route's schedule.")

        if not ((arr_day < data['arrival_day'] or
                 (arr_day == data['arrival_day'] and arr_time <= data['arrival_time'])) and
                (arr_day < data['departure_day'] or
                 (arr_day == data['departure_day'] and arr_time >= data['departure_time']))):
            raise serializers.ValidationError("Arrival and departure times must fit within the route's timing.")

        return data


# statistics serializers
class MostFrequentPlaneSerializer(serializers.Serializer):
    route_id = serializers.IntegerField()
    route = serializers.SerializerMethodField()
    most_frequent_plane = serializers.SerializerMethodField()
    airline = serializers.IntegerField()

    def get_route(self, obj):
        route_id = obj['route_id']
        try:
            route = Route.objects.get(id=route_id)
            return str(route)
        except Route.DoesNotExist:
            return None

    def get_most_frequent_plane(self, obj):
        route_id = obj['route_id']
        airline = self.validated_data.get('airline')
        planes = (
            Flight.objects.filter(route_id=route_id, plane__airline_id=airline)
            .values('plane__model')
            .annotate(flight_count=Count('id'))
            .order_by('-flight_count')
        )

        if planes:
            plane_model_id = planes[0]['plane__model']
            try:
                plane_model = PlaneModel.objects.get(id=plane_model_id)
                serialized_plane = PlaneModelSerializer(plane_model).data
                return {
                    'plane_model': serialized_plane,
                    'flight_count': planes[0]['flight_count']
                }
            except PlaneModel.DoesNotExist:
                return None

        return None


class UnderFilledRouteSerializer(serializers.ModelSerializer):
    departure_airport = serializers.StringRelatedField()
    destination_airport = serializers.StringRelatedField()
    under_filled_count = serializers.SerializerMethodField()
    under_filled_percentage = serializers.SerializerMethodField()
    route = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = ['route', 'id', 'departure_airport', 'destination_airport', 'under_filled_count', 'under_filled_percentage']

    def get_under_filled_count(self, obj):
        threshold = self.context.get('threshold', 50) / 100
        airline = self.context.get('airline')
        flights = obj.flights.filter(plane__airline = airline)
        under_filled_count = 0
        for flight in flights:
            fill_percentage = flight.sold_tickets_number / flight.plane.model.seats_capacity
            if fill_percentage < threshold:
                under_filled_count += 1
        return under_filled_count

    def get_under_filled_percentage(self, obj):
        airline = self.context.get('airline')
        flights = obj.flights.filter(plane__airline = airline)
        total_flights = flights.count()
        if total_flights == 0:
            return 0  # No flights to calculate percentage
        under_filled_count = self.get_under_filled_count(obj)
        return round((under_filled_count / total_flights) * 100, 2)

    def get_route(self, obj):
        return RouteSerializer(obj).data


class FlightSeatAvailabilitySerializer(serializers.ModelSerializer):
    available_seats = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = ['id', 'number', 'available_seats', 'is_available']

    def get_available_seats(self, obj):
        return obj.seats.filter(is_sold=False).count()

    def get_is_available(self, obj):
        return obj.seats.filter(is_sold=False).exists()


class PlanesInMaintenanceSerializer(serializers.Serializer):
    planes_in_maintenance_count = serializers.SerializerMethodField()
    maintenances_details = serializers.SerializerMethodField()

    def get_planes_in_maintenance_count(self, obj):
        current_time = now()
        return Maintenance.objects.filter(
            start_date__lte=current_time,
            end_date__gte=current_time
        ).count()

    def get_maintenances_details(self, obj):
        current_time = now()
        maintenances = Maintenance.objects.filter(
            start_date__lte=current_time,
            end_date__gte=current_time
        )

        return MaintenanceSerializer(maintenances, many=True).data


class AirlineEmployeesCountSerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Airline
        fields = ['id', 'name', 'employee_count']

    def get_employee_count(self, obj):
        return obj.employees.count()


class PlaneStatisticsSerializer(serializers.Serializer):
    total_planes = serializers.SerializerMethodField()
    models_statistics = serializers.SerializerMethodField()

    def get_total_planes(self, obj):
        return obj.planes.count()

    def get_models_statistics(self, obj):
        planes = obj.planes.select_related('model').all()
        model_stats = defaultdict(lambda: {
            'plane_numbers': []
        })

        for plane in planes:
            model = plane.model
            model_stats[model]['plane_numbers'].append(plane.number)

        formatted_stats = []
        for model, data in model_stats.items():
            formatted_stats.append({
                'model': model.name,
                'plane_amount': len(data['plane_numbers']),
                'seat_capacity': model.seats_capacity,
                'speed': model.speed,
                'plane_numbers': data['plane_numbers']
            })

        return formatted_stats