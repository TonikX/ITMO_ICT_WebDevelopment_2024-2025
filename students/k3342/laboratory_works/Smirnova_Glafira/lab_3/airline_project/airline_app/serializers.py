from collections import defaultdict

from django.db.models import Count
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


class PlaneModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaneModel
        fields = '__all__'


class PlaneSerializer(serializers.ModelSerializer):
    airline = serializers.StringRelatedField()
    model = PlaneModelSerializer()

    class Meta:
        model = Plane
        fields = '__all__'


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

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ["employer"]


class EmployeeNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name']


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
        fields = ['employee', 'role']

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

        employee = data.get('employee', instance.employee if instance else None)
        role = data.get('role', instance.role if instance else None)

        if CrewMember.objects.filter(employee=employee, role=role).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("This crew member with the specified role already exists.")

        return data


class RouteSerializer(serializers.ModelSerializer):
    departure_airport = serializers.StringRelatedField()
    destination_airport = serializers.StringRelatedField()
    stops = serializers.StringRelatedField(many=True)

    class Meta:
        model = Route
        fields = '__all__'


class RouteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        exclude = ['id']

    def validate(self, data):
        """
        Custom validation for route creation:
        - Ensure no duplicate route exists with the same departure, destination, and stops.
        - Ensure departure, destination, and stops airports are all distinct.
        """
        instance = self.instance

        departure_airport = data.get('departure_airport', instance.departure_airport if instance else None)
        destination_airport = data.get('destination_airport', instance.destination_airport if instance else None)
        stops = data.get('stops', instance.stops.all() if instance else [])

        if not (departure_airport and destination_airport and stops):
            return data

        # Validate that departure, destination, and stops are distinct
        if departure_airport in stops:
            raise serializers.ValidationError(
                {"departure_airport": "Departure airport cannot be one of the stops."}
            )
        if destination_airport in stops:
            raise serializers.ValidationError(
                {"destination_airport": "Destination airport cannot be one of the stops."}
            )
        if departure_airport == destination_airport:
            raise serializers.ValidationError(
                {"departure_airport": "Departure and destination airports must be different."}
            )

        # Validate that the route does not already exist
        existing_routes = Route.objects.filter(
            departure_airport=departure_airport,
            destination_airport=destination_airport,
        ).exclude(id=instance.id if instance else None)

        # Check stops match existing routes
        for route in existing_routes:
            if set(route.stops.all()) == set(stops):
                raise serializers.ValidationError(
                    {"non_field_errors": "A route with the same departure, destination, and stops already exists."}
                )

        return data


class RouteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['number', 'distance_km']


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
        exclude = ["sold_tickets_number"]

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
        departure_datetime = data['departure_datetime']
        arrival_datetime = data['arrival_datetime']

        overlapping_maintenances = Maintenance.objects.filter(
            plane=plane,
            start_date__lt=arrival_datetime,
            end_date__gt=departure_datetime
        )
        if overlapping_maintenances.exists():
            maintenance = overlapping_maintenances.first()
            raise serializers.ValidationError(
                {"plane": f"Plane {plane.number} is under maintenance from {maintenance.start_date} "
                          f"to {maintenance.end_date or 'an unknown end date'}."}
            )

        overlapping_flights_plane = Flight.objects.filter(
            plane=plane,
            departure_datetime__lt=arrival_datetime,
            arrival_datetime__gt=departure_datetime
        )
        if overlapping_flights_plane.exists():
            flight = overlapping_flights_plane.first()
            raise serializers.ValidationError(
                {"plane": f"Plane {plane.number} is occupied by another flight ({flight.number}) "
                          f"from {flight.departure_datetime} to {flight.arrival_datetime}."}
            )

        overlapping_flights_crew = Flight.objects.filter(
            crew=crew,
            departure_datetime__lt=arrival_datetime,
            arrival_datetime__gt=departure_datetime
        )
        if overlapping_flights_crew.exists():
            flight = overlapping_flights_crew.first()
            raise serializers.ValidationError(
                {"crew": f"Crew {crew} is occupied by another flight ({flight.number}) "
                         f"from {flight.departure_datetime} to {flight.arrival_datetime}."}
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
        exclude = ["sold_tickets_number"]

    def validate(self, data):
        """
        Custom validation for plane, crew, and schedule conflicts in partial updates.
        """
        instance = self.instance

        plane = data.get('plane', instance.plane)
        crew = data.get('crew', instance.crew)
        departure_datetime = data.get('departure_datetime', instance.departure_datetime)
        arrival_datetime = data.get('arrival_datetime', instance.arrival_datetime)

        if not (plane and departure_datetime and arrival_datetime):
            return data

        overlapping_maintenances = Maintenance.objects.filter(
            plane=plane,
            start_date__lt=arrival_datetime,
            end_date__gt=departure_datetime
        )
        if overlapping_maintenances.exists():
            maintenance = overlapping_maintenances.first()
            raise serializers.ValidationError(
                {"plane": f"Plane {plane.number} is under maintenance from {maintenance.start_date} "
                          f"to {maintenance.end_date or 'an unknown end date'}."}
            )

        overlapping_flights_plane = Flight.objects.filter(
            plane=plane,
            departure_datetime__lt=arrival_datetime,
            arrival_datetime__gt=departure_datetime
        ).exclude(id=instance.id)
        if overlapping_flights_plane.exists():
            flight = overlapping_flights_plane.first()
            raise serializers.ValidationError(
                {"plane": f"Plane {plane.number} is occupied by another flight ({flight.number}) "
                          f"from {flight.departure_datetime} to {flight.arrival_datetime}."}
            )

        if crew:
            overlapping_flights_crew = Flight.objects.filter(
                crew=crew,
                departure_datetime__lt=arrival_datetime,
                arrival_datetime__gt=departure_datetime
            ).exclude(id=instance.id)
            if overlapping_flights_crew.exists():
                flight = overlapping_flights_crew.first()
                raise serializers.ValidationError(
                    {"crew": f"Crew {crew} is occupied by another flight ({flight.number}) "
                             f"from {flight.departure_datetime} to {flight.arrival_datetime}."}
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
                {"plane": f"Plane {plane.number} is under another maintenance from {maintenance.start_date} "
                          f"to {maintenance.end_date or 'an unknown end date'}."}
            )

        # Validate overlapping flights for the plane
        overlapping_flights_plane = Flight.objects.filter(
            plane=plane,
            departure_datetime__lt=end_date,
            arrival_datetime__gt=start_date
        )
        if overlapping_flights_plane.exists():
            flight = overlapping_flights_plane.first()
            raise serializers.ValidationError(
                {"plane": f"Plane {plane.number} is occupied by a flight ({flight.number}) "
                          f"from {flight.departure_datetime} to {flight.arrival_datetime}."}
            )

        return data


class TransitStopCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransitStop
        fields = ['airport', 'arrival_datetime', 'departure_datetime']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['airport_choices'] = [{"id": airport.id, "name": str(airport)} for airport in Airport.objects.all()]
        return rep

    def validate(self, data):
        flight = self.context.get('flight')

        route_stops = flight.route.stops.all()
        if data['airport'] not in route_stops:
            raise serializers.ValidationError("Selected airport is not a transit stop on this flight's route.")

        if TransitStop.objects.filter(flight=flight, airport=data['airport']).exists():
            raise serializers.ValidationError("Transit stop for this airport already exists.")

        if not (flight.departure_datetime <= data['arrival_datetime'] <= flight.arrival_datetime):
            raise serializers.ValidationError("Arrival datetime must be within the flight's schedule.")
        if not (flight.departure_datetime <= data['departure_datetime'] <= flight.arrival_datetime):
            raise serializers.ValidationError("Departure datetime must be within the flight's schedule.")

        if data['arrival_datetime'] >= data['departure_datetime']:
            raise serializers.ValidationError("Departure datetime must be after arrival datetime.")

        return data


# statistics serializers
class MostFrequentPlaneSerializer(serializers.Serializer):
    route_id = serializers.IntegerField()
    route = serializers.SerializerMethodField()
    most_frequent_plane = serializers.SerializerMethodField()

    def get_route(self, obj):
        route_id = obj['route_id']
        try:
            route = Route.objects.get(id=route_id)
            return str(route)
        except Route.DoesNotExist:
            return None

    def get_most_frequent_plane(self, obj):
        route_id = obj['route_id']

        planes = (
            Flight.objects.filter(route_id=route_id)
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

    class Meta:
        model = Route
        fields = ['id', 'departure_airport', 'destination_airport', 'under_filled_count', 'under_filled_percentage']

    def get_under_filled_count(self, obj):
        threshold = self.context.get('threshold', 50) / 100
        flights = obj.flights.all()
        under_filled_count = 0
        for flight in flights:
            fill_percentage = flight.sold_tickets_number / flight.plane.model.seats_capacity
            if fill_percentage < threshold:
                under_filled_count += 1
        return under_filled_count

    def get_under_filled_percentage(self, obj):
        flights = obj.flights.all()
        total_flights = flights.count()
        if total_flights == 0:
            return 0  # No flights to calculate percentage
        under_filled_count = self.get_under_filled_count(obj)
        return round((under_filled_count / total_flights) * 100, 2)


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
