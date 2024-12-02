from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *


class SubjectScheduleView(APIView):
    def get(self, request, class_id, day_of_week, lesson_number):
        schedule = Schedule.objects.filter(
            class_instance=class_id,
            day_of_week=day_of_week,
            lesson_number=lesson_number
        ).select_related('subject').first()
        if schedule:
            return Response({'subject_name': schedule.subject.name})
        return Response({'error': 'No schedule found'}, status=404)


class TeacherCountPerSubjectView(APIView):
    def get(self, request):
        subject_counts = Schedule.objects.values('subject') \
            .annotate(teacher_count=Count('teacher', distinct=True))
        return Response(subject_counts)


# Получить учителей, преподающих те же предметы, что и учитель, ведущий информатику в классе
class InformaticsTeacherPeersView(APIView):
    def get(self, request, class_id):
        informatics_subject = Subject.objects.get(name='Informatics')
        informatics_teachers = Schedule.objects.filter(
            subject=informatics_subject,
            class_instance=class_id
        ).values('teacher').distinct()

        teachers = Teacher.objects.filter(id__in=[t['teacher'] for t in informatics_teachers])
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)


# Получить отчет по успеваемости класса
class ClassReportView(generics.GenericAPIView):
    serializer_class = ClassReportSerializer

    def get(self, request, class_id):
        report_data = get_class_report(class_id)  # Ваши функции для получения отчета
        return Response(report_data)

