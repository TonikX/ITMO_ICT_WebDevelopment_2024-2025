from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.http import JsonResponse


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Пользователь успешно зарегистрирован'})
        return Response(serializer.errors)


class SectionsListView(APIView):
    def get(self, request, *args, **kwargs):
        sections = SportSection.objects.all()
        sections_data = []

        for section in sections:
            section_data = {
                "id": section.id,
                "description": section.description,
                "title": section.title,
                "coach": f"{section.sportsectioncoaches_set.first().coach.last_name} {section.sportsectioncoaches_set.first().coach.first_name} {section.sportsectioncoaches_set.first().coach.middle_name}" if section.sportsectioncoaches_set.exists() else None,
                "sportsmen": [{"FIO": f"{sportsman.last_name} {sportsman.first_name} {sportsman.middle_name}"} for sportsman in section.sportsmen.all()],
                "free_places": section.capacity - section.sportsmen.count()
            }
            sections_data.append(section_data)

        return Response(sections_data)


class SportsmenListView(APIView):
    def get(self, request):
        students = Sportsman.objects.all()
        section = request.query_params.get('section')
        if section:
            students = students.filter(section__name=section)
        serializer = SportsmenSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SportsmenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class CoachesListView(APIView):
    def get(self, request):
        trainers = Coach.objects.all()
        serializer = CoachSerializer(trainers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CoachSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class SportHallsListView(APIView):
    def get(self, request):
        halls = SportHall.objects.all()
        serializer = SportHallsSerializer(halls, many=True)
        return Response(serializer.data)


class ScheduleListView(APIView):
    def get(self, request):
        trainings = Schedule.objects.all()
        serializer = ScheduleSerializer(trainings, many=True)
        return Response(serializer.data)


class UpdateSportsmanView(UpdateAPIView):
    queryset = Sportsman.objects.all()
    serializer_class = SportsmenSerializer

    def get(self, request, *args, **kwargs):
        sport_hall_equipment = self.get_object()
        serializer = self.get_serializer(sport_hall_equipment)
        return Response(serializer.data)


class SectionDetailsView(APIView):
    def get(self, request, pk):
        section = SportSection.objects.get(pk=pk)
        sportsmen = section.sportsmen.all()
        serializer = SportsmenSerializer(sportsmen, many=True)
        return Response({"title": section.title, "sportsmen": serializer.data})


class CoachesBySectionView(APIView):
    def get(self, request, section_id, *args, **kwargs):
        coaches = SportSectionCoaches.objects.filter(section_id=section_id, end__isnull=True)
        data = [{"id": coach.coach.id, "name": coach.coach.name} for coach in coaches]
        return Response(data)


class AddSportsmanToSection(APIView):
    def post(self, request, section_id):
        sportsman_id = request.data.get('sportsman_id')
        section = SportSection.objects.get(id=section_id)
        sportsman = Sportsman.objects.get(id=sportsman_id)
        section.sportsmen.add(sportsman)
        section.save()
        return Response({"message": "Спортсмен добавлен в секцию"})


def generate_report(request, coach_id):
    coach = Coach.objects.get(id=coach_id)
    coach_info = {
        "name": f'{coach.last_name} {coach.first_name} {coach.middle_name}',
        "qualification": coach.qualification,
        "experience": coach.experience,
    }
    sections = SportSectionCoaches.objects.filter(coach=coach)
    section_data = []
    for section_coach in sections:
        section = section_coach.section
        schedules = Schedule.objects.filter(sport_section=section)
        schedule_data = [
            {
                "sport_hall": schedule.sport_hall.name,
                "weekday": schedule.weekday,
                "start_time": schedule.start_time.strftime('%H:%M'),
                "end_time": schedule.end_time.strftime('%H:%M'),
            }
            for schedule in schedules
        ]
        sportsmen = section.sportsmen.all()
        sportsman_data = [{"name": f'{sportsman.last_name} {sportsman.first_name}'} for sportsman in sportsmen]
        section_data.append({
            "section_title": section.title,
            "schedule": schedule_data,
            "sportsmen": sportsman_data,
        })
    training_count = Schedule.objects.filter(sport_section__in=[section_coach.section for section_coach in sections])
    training_count = training_count.count()
    report = {
        "coach_info": coach_info,
        "sections": section_data,
        "training_count": training_count,
    }
    return JsonResponse(report)
