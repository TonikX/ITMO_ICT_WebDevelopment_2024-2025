from django.db.models import Count, Avg
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from school_app.models import Teacher, HomeTeacher, Student, Schedule, Group, Subject, Room, QuarterGrades
from school_app.serializers import TeacherSerializer, TeacherCreateSerializer, HomeTeacherSerializer, \
    HomeTeacherCreateSerializer, StudentCreateSerializer, StudentSerializer, ScheduleSerializer, \
    ScheduleCreateSerializer, SubjectSerializer, SubjectTeacherCountSerializer, RoomSerializer, GroupSerializer, \
    QuarterGradesSerializer, QuarterGradesCreateSerializer, QuarterGradesUpdateSerializer


def get_group_by_group_full_name(group_name: str) -> Group:
    if len(group_name) == 2:
        group_grade = int(group_name[0])
        group_id = group_name[1]
    else:
        group_grade = int(group_name[0:1])
        group_id = group_name[2]
    return Group.objects.get(group_grade=group_grade, group_name=group_id)


class TeacherAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherCreateSerializer

    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeacherCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Teacher created successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = 'id'


class GroupAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer

    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Teacher created successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeTeacherAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = HomeTeacherSerializer

    def get(self, request):
        home_teachers = HomeTeacher.objects.all()
        serializer = HomeTeacherSerializer(home_teachers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HomeTeacherCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Home Teacher created successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentCreateSerializer

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Student created successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'


class ScheduleAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScheduleCreateSerializer

    def get(self, request):
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ScheduleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Schedule created successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    lookup_field = 'id'


class SubjectAPIVIew(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectSerializer

    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


class QuarterGradesAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuarterGradesCreateSerializer

    def get(self, request, id):
        quarter_grades = QuarterGrades.objects.filter(student_id=id)
        serializer = QuarterGradesSerializer(quarter_grades, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuarterGradesCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Quarter Grades created successfully"})


class QuarterGradesUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = QuarterGrades.objects.all()
    serializer_class = QuarterGradesUpdateSerializer


class SubjectViewByDayAndLessonNumber(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectSerializer

    @swagger_auto_schema(
        operation_description="Получить предмет, который будет преподаваться в определённом классе, в определённый день недели, на определённом уроке.",
        manual_parameters=[
            openapi.Parameter(
                'group_name',
                openapi.IN_QUERY,
                description="Класс",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'day_of_week',
                openapi.IN_QUERY,
                description="День недели",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'lesson_number',
                openapi.IN_QUERY,
                description="Номер урока",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="Successful retrieval", schema=SubjectSerializer),
        }
    )
    def get(self, request):
        day_of_week = request.query_params.get('day_of_week', None)
        lesson_number = request.query_params.get('lesson_number', None)
        group = get_group_by_group_full_name(request.query_params.get('group_name', None))
        try:
            schedule = Schedule.objects.get(group=group, day_of_week=day_of_week, number_of_lesson=lesson_number)
            serializer = SubjectSerializer(schedule.subject)
            return Response(serializer.data)
        except Schedule.DoesNotExist:
            return Response({"Ошибка": "Урока в расписании по таким параметрам найти не удалось"})


class TeacherOfSubjectsCountView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subjects = Subject.objects.annotate(teacher_count=Count('schedule__teacher', distinct=True))

        serializer = SubjectTeacherCountSerializer(subjects, many=True)
        return Response(serializer.data)


class RoomsApiView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer
    queryset = Room.objects.all()


class TeachersByTeacherInClass(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherSerializer

    @swagger_auto_schema(
        operation_description="Получить список учителей, преподающих те же предметы, что и учитель, ведущий информатику в заданном классе.",
        manual_parameters=[
            openapi.Parameter(
                'group_name',
                openapi.IN_QUERY,
                description="Класс",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="Successful retrieval", schema=SubjectSerializer),
        }
    )
    def get(self, request):
        group = get_group_by_group_full_name(request.query_params.get('group_name', None))
        informatics_teacher = Teacher.objects.filter(
            id__in=Schedule.objects.filter(
                group=group,
                subject__subject_name='Информатика'
            ).values('teacher_id')
        ).first()
        if not informatics_teacher:
            return Response({"Ошибка": "Не было найдено учителя информатики у этой группы"}, status=404)

        subjects_of_informatics_teacher = Schedule.objects.filter(
            teacher=informatics_teacher
        ).values_list('subject', flat=True)

        teachers_with_same_subjects = Teacher.objects.filter(
            id__in=Schedule.objects.filter(
                subject__in=subjects_of_informatics_teacher
            ).exclude(teacher=informatics_teacher).values('teacher_id')
        ).distinct()

        serializer = TeacherSerializer(teachers_with_same_subjects, many=True)
        return Response(serializer.data)


class BoysAndGirlsInGroupsView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        groups = Group.objects.all()
        gender_counts = []

        for group in groups:
            boys_count = Student.objects.filter(group=group, gender='m').count()
            girls_count = Student.objects.filter(group=group, gender='f').count()

            gender_counts.append({
                'group_name': f"{group.group_grade}{group.group_name}",
                'boys_count': boys_count,
                'girls_count': girls_count
            })

        return Response(gender_counts)


class CountOfSpecializedAndNonSpecializerRoomsView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        base_rooms_count = Room.objects.filter(subject_id__isnull=True).count()
        profile_rooms = Room.objects.filter(subject_id__isnull=False).count()

        return Response({
            'base_rooms': base_rooms_count,
            'profile_rooms': profile_rooms
        })


class ReportView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Отчёт по заданному классу.",
        manual_parameters=[
            openapi.Parameter(
                'group_name',
                openapi.IN_QUERY,
                description="Класс",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="Successful retrieval", schema=SubjectSerializer),
        }
    )
    def get(self, request):
        group = get_group_by_group_full_name(request.query_params.get('group_name', None))

        home_teacher = HomeTeacher.objects.get(group=group)
        class_teacher = home_teacher.teacher

        students_in_group = Student.objects.filter(group=group)

        total_students = students_in_group.count()

        subjects_report = []
        for subject in Subject.objects.all():
            grades = QuarterGrades.objects.filter(student__in=students_in_group, subject=subject)

            if grades.exists():
                average_grade = grades.aggregate(Avg('grade'))['grade__avg']
            else:
                average_grade = None

            subjects_report.append({
                'subject_name': subject.subject_name,
                'average_grade': average_grade
            })

        report = {
            'class_name': f'{group.group_grade}{group.group_name}',
            'class_teacher': f'{class_teacher.first_name} {class_teacher.second_name} {class_teacher.patronymic}',
            'total_students': total_students,
            'subjects': subjects_report
        }

        return Response(report)
