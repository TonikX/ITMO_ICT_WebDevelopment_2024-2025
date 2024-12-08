from datetime import time

from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


class SportsmenAPIView(APIView):
    def get(self, request):
        sportsmen = Sportsman.objects.all()
        serializer = SportsmenSerializer(sportsmen, many=True)
        return Response({"Sportsmen": serializer.data})


class SportsmanCreateView(APIView):
    def post(self, request):
        sportsman = request.data.get("sportsman")
        serializer = SportsmenSerializer(data=sportsman)
        if serializer.is_valid(raise_exception=True):
            sportsman_saved = serializer.save()
        return Response({"Success": "Sportsman '{}' created succesfully.".format(sportsman_saved.first_name)})


class SportAPIView(APIView):
    def get(self, request):
        sports = Sport.objects.all()
        serializer = SportSerializer(sports, many=True)
        return Response({"Sports": serializer.data})


class SportCreateView(APIView):
    def post(self, request):
        sport = request.data.get("sport")
        serializer = SportSerializer(data=sport)
        if serializer.is_valid(raise_exception=True):
            sport_saved = serializer.save()
        return Response({"Success": "Sport '{}' created succesfully.".format(sport_saved.name)})


class CoachAPIView(APIView):
    def get(self, request):
        coaches = Coach.objects.all()
        serializer = CoachSerializer(coaches, many=True)
        return Response({"Coaches": serializer.data})


class CoachCreateView(APIView):
    def post(self, request):
        coach = request.data.get("coach")
        serializer = CoachSerializer(data=coach)
        if serializer.is_valid(raise_exception=True):
            coach_saved = serializer.save()
        return Response({"Success": "Coach '{}' created succesfully.".format(coach_saved.first_name)})


class EquipmentAPIView(APIView):
    def get(self, request):
        equipment = Equipment.objects.all()
        serializer = EquipmentSerializer(equipment, many=True)
        return Response({"Equipment": serializer.data})


class EquipmentCreateView(APIView):
    def post(self, request):
        equipment = request.data.get("equipment")
        serializer = EquipmentSerializer(data=equipment)
        if serializer.is_valid(raise_exception=True):
            equipment_saved = serializer.save()
        return Response({"Success": "Equipment '{}' created succesfully.".format(equipment_saved.name)})


class SportHallAPIView(APIView):
    def get(self, request):
        sport_halls = SportHall.objects.all()
        serializer = SportHallSerializer(sport_halls, many=True)
        return Response({"Sport halls": serializer.data})


class SportHallCreateView(APIView):
    def post(self, request):
        sport_hall = request.data.get("sport_hall")
        serializer = SportHallSerializer(data=sport_hall)
        if serializer.is_valid(raise_exception=True):
            sport_hall_saved = serializer.save()
        return Response({"Success": "Sport hall '{}' created succesfully.".format(sport_hall_saved.name)})


class EquipmentOfSportHallAPIView(APIView):
    def get(self, request):
        sport_halls_equipment = EquipmentOfSportHall.objects.all()
        serializer = EquipmentOfSportHallSerializer(sport_halls_equipment, many=True)
        return Response({"Sport halls equipment": serializer.data})


class EquipmentOfSportHallCreateView(APIView):
    def post(self, request):
        sport_hall_equipment = request.data.get("sport_hall_equipment")
        serializer = EquipmentOfSportHallSerializer(data=sport_hall_equipment)
        if serializer.is_valid(raise_exception=True):
            sport_hall_equipment_saved = serializer.save()
        return Response({"Success": "Sport hall equipment '{}' created succesfully.".format(sport_hall_equipment_saved.equipment)})


class SportSectionAPIView(APIView):
    def get(self, request):
        sport_sections = SportSection.objects.all()
        serializer = SportSectionSerializer(sport_sections, many=True)
        return Response({"Sport sections": serializer.data})


class SportSectionCreateView(APIView):
    def post(self, request):
        sport_section = request.data.get("sport_section")
        serializer = SportSectionSerializer(data=sport_section)
        if serializer.is_valid(raise_exception=True):
            sport_section_saved = serializer.save()
        return Response({"Success": "Sport section '{}' created succesfully.".format(sport_section_saved.title)})


class SportSectionCoachesView(APIView):
    def get(self, request):
        section_coaches = SportSectionCoaches.objects.all()
        serializer = SportSectionCoachesSerializer(section_coaches, many=True)
        return Response({"Sport sections coaches": serializer.data})


class SportSectionCoachesCreateView(APIView):
    def post(self, request):
        section_coaches = request.data.get("section_coaches")
        serializer = SportSectionCoachesSerializer(data=section_coaches)
        if serializer.is_valid(raise_exception=True):
            section_coaches_saved = serializer.save()
        return Response({"Success": "Coach for '{}' created succesfully.".format(section_coaches_saved.section)})


class ScheduleAPIView(APIView):
    def get(self, request):
        schedule = Schedule.objects.all()
        serializer = ScheduleSerializer(schedule, many=True)
        return Response({"Schedule": serializer.data})


class ScheduleCreateView(APIView):
    def post(self, request):
        schedule = request.data.get("schedule")
        serializer = ScheduleSerializer(data=schedule)
        if serializer.is_valid(raise_exception=True):
            schedule_saved = serializer.save()
        return Response({"Success": "Schedule for '{}' created succesfully.".format(schedule_saved.sport_section)})


class SportsmenUpdateView(UpdateAPIView):
    queryset = Sportsman.objects.all()
    serializer_class = SportsmenSerializer

    def get(self, request, *args, **kwargs):
        sportsmen = self.get_object()
        serializer = self.get_serializer(sportsmen)
        return Response(serializer.data)


class CoachUpdateView(UpdateAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer

    def get(self, request, *args, **kwargs):
        coach = self.get_object()
        serializer = self.get_serializer(coach)
        return Response(serializer.data)


class EquipmentOfSportHallUpdateView(UpdateAPIView):
    queryset = EquipmentOfSportHall.objects.all()
    serializer_class = EquipmentOfSportHallSerializer

    def get(self, request, *args, **kwargs):
        sport_hall_equipment = self.get_object()
        serializer = self.get_serializer(sport_hall_equipment)
        return Response(serializer.data)


class SportSectionUpdateView(UpdateAPIView):
    queryset = SportSection.objects.all()
    serializer_class = SportSectionSerializer

    def get(self, request, *args, **kwargs):
        sport_section = self.get_object()
        serializer = self.get_serializer(sport_section)
        return Response(serializer.data)


class ScheduleUpdateView(UpdateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get(self, request, *args, **kwargs):
        schedule = self.get_object()
        serializer = self.get_serializer(schedule)
        return Response(serializer.data)


class SportSectionCoachesUpdateView(UpdateAPIView):
    queryset = SportSectionCoaches.objects.all()
    serializer_class = SportSectionCoachesSerializer

    def get(self, request, *args, **kwargs):
        section_coaches = self.get_object()
        serializer = self.get_serializer(section_coaches)
        return Response(serializer.data)


class SportsmenDeleteView(DestroyAPIView):
    queryset = Sportsman.objects.all()
    serializer_class = SportsmenSerializer


class ScheduleDeleteView(DestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class CoachDeleteView(DestroyAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer


class SportSectionDeleteView(DestroyAPIView):
    queryset = SportSection.objects.all()
    serializer_class = SportSectionSerializer


class SportSectionCoachesDeleteView(DestroyAPIView):
    queryset = SportSectionCoaches.objects.all()
    serializer_class = SportSectionCoachesSerializer


class EquipmentOfSportHallDeleteView(DestroyAPIView):
    queryset = EquipmentOfSportHall.objects.all()
    serializer_class = EquipmentOfSportHallSerializer


class SportSectionSearchAPIView(APIView):
    # Какая секция будет в заданном зале, в заданный день недели на заданное время?
    def post(self, request):
        sport_hall_id = request.data.get("sport_hall_id")
        weekday = request.data.get("weekday")
        start_time = request.data.get("start_time")

        if sport_hall_id and weekday and start_time:
            schedule = Schedule.objects.filter(sport_hall=sport_hall_id, weekday=weekday, start_time=start_time).select_related("sport_section", "sport_hall")
            if schedule.exists():
                result = []
                for info in schedule:
                    necessary_coach = SportSectionCoaches.objects.filter(section=info.sport_section).select_related("coach").first()
                    result.append({
                        "sport_section": info.sport_section.title,
                        "sport_hall": info.sport_hall.name,
                        "coach": f"{necessary_coach.coach.last_name} {necessary_coach.coach.first_name} {necessary_coach.coach.middle_name}" if necessary_coach else "No current coach",
                        "start_time": info.start_time,
                        "end_time": info.end_time,
                    })
                return Response({"Sport sections": result})
        return Response({"message": "No sections found"})


class SportSectionSportsmenSearchAPIView(APIView):
    # Сколько спортсменов занимаются в секции и какое количество свободных мест?
    def get(self, request):
        section_id = request.query_params.get("section_id")
        sport_section = SportSection.objects.get(id=section_id)
        sportsmen_count = sport_section.sportsmen.count()
        free_places = sport_section.capacity - sportsmen_count
        sportsmen = list(sport_section.sportsmen.values_list("last_name", "first_name", "middle_name"))

        result = {
            "id": sport_section.id,
            "title": sport_section.title,
            "sportsmen": sportsmen,
            "capacity": sport_section.capacity,
            "sportsmen_count": sportsmen_count,
            "free_slots": free_places
        }
        return Response(result)


class CoachScheduleSearchAPIView(APIView):
    # Какое расписание тренировок у конкретного тренера?
    def get(self, request):
        coach_id = request.query_params.get("coach_id")
        coach = Coach.objects.get(id=coach_id)
        sport_section_coaches = SportSectionCoaches.objects.filter(coach=coach_id)
        coach_schedule = []
        for coach_section in sport_section_coaches:
            schedules = Schedule.objects.filter(sport_section=coach_section.section)
            for schedule in schedules:
                coach_schedule.append({
                    "section": schedule.sport_section.title,
                    "start_time": schedule.start_time,
                    "end_time": schedule.end_time,
                })

        result = {
            "id": coach_id,
            "last_name": coach.last_name,
            "first_name": coach.first_name,
            "middle_name": coach.middle_name,
            "coach_schedule": coach_schedule
        }
        return Response(result)


class SportHallEquipmentSearchAPIView(APIView):
    # Какое оборудование имеется в наличии в определенном зале?
    def get(self, request):
        hall_id = request.query_params.get("hall_id")
        hall = SportHall.objects.get(id=hall_id)
        equipment_of_sport_halls = EquipmentOfSportHall.objects.filter(sport_hall=hall_id)
        all_equipment = []
        for equipment in equipment_of_sport_halls:
            all_equipment.append({
                "name": equipment.equipment.name,
                "sport": equipment.equipment.sport.name,
                "amount": equipment.amount
            })
        result = {
            "id": hall_id,
            "sport_hall": hall.name,
            "address": hall.address,
            "equipment": all_equipment
        }
        return Response(result)


class SectionsBySportSearchAPIView(APIView):
    # Список доступных секций по конкретному виду спорта
    def get(self, request):
        sport_id = request.query_params.get("sport_id")
        sport = Sport.objects.get(id=sport_id)
        sport_sections = SportSection.objects.filter(sport=sport_id)
        all_sections = []
        for section in sport_sections:
            all_sections.append({
                "title": section.title,
                "description": section.description
            })
        result = {
            "id": sport_id,
            "name": sport.name,
            "all_sections": all_sections
        }
        return Response(result)
