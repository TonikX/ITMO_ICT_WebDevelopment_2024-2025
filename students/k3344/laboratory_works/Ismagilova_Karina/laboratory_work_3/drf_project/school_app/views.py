from django.db.models import Count
from requests import Response
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from .serializers import *

class StudentListCreateView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeacherListCreateView(ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class TeacherDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class GradeListCreateView(ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class LessonListCreateView(ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class RoomListCreateView(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class StudentScheduleListCreateView(ListCreateAPIView):
    queryset = StudentSchedule.objects.all()
    serializer_class = StudentScheduleSerializer

class StudentScheduleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = StudentSchedule.objects.all()
    serializer_class = StudentScheduleSerializer

class SubjectInRoomView(APIView):
    "Список предметов, которые проводятся в указанной комнате в указанный день недели."
    def get(self, request, room_number, day):
        lessons = Lesson.objects.filter(room__number=room_number, day=day)
        if lessons.exists():
            data = [
                {
                    "subject": lesson.subject,
                    "class": lesson.class_label,
                    "lesson_number": lesson.lesson_number
                } for lesson in lessons
            ]
            return Response(data)
        else:
            return Response({"error": "No lessons found for the specified room and day"}, status=404)

class TeachersPerSubjectView(APIView):
    "Количество учителей, преподающих каждый предмет, имена и фамилии."
    def get(self, request):
        subjects = Lesson.objects.values('subject').annotate(teacher_count=Count('teacher', distinct=True))
        result = []
        for subject in subjects:
            subject_name = subject['subject']
            teachers = Lesson.objects.filter(subject=subject_name).values(
                'teacher__name', 'teacher__surname'
            ).distinct()
            teacher_list = [
                {"name": teacher['teacher__name'], "surname": teacher['teacher__surname']}
                for teacher in teachers
            ]
            result.append({
                "subject": subject_name,
                "teacher_count": subject['teacher_count'],
                "teachers": teacher_list
            })
        return Response(result)

class GenderCountPerClassView(APIView):
    "Количество мальчиков и девочек в каждом классе."
    def get(self, request):
        gender_counts = (
            Student.objects.values('class_name', 'gender')
            .annotate(count=Count('id_student'))
        )
        result = {}
        for item in gender_counts:
            class_name = item['class_name']
            if class_name not in result:
                result[class_name] = {"boys": 0, "girls": 0}
            if item['gender'] == 'М':
                result[class_name]["boys"] = item['count']
            elif item['gender'] == 'Ж':
                result[class_name]["girls"] = item['count']
        return Response(result)

class RoomCountByStatusView(APIView):
    "Количество кабинетов в школе по классификации."
    def get(self, request):
        room_counts = (
            Room.objects.values('status')
            .annotate(count=Count('id_room'))
        )
        result = {item['status']: item['count'] for item in room_counts}
        return Response(result)

class TeachersWithSameSubjectsView(APIView):
    "Список учителей, которые преподают те же предметы, что и указанный учитель по id."
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id_teacher=teacher_id)
        subjects = teacher.lessons.values_list('subject', flat=True)
        teachers_with_same_subjects = Teacher.objects.filter(lessons__subject__in=subjects).exclude(id_teacher=teacher_id)
        teacher_list = [
            {"name": t.surname + " " + t.name} for t in teachers_with_same_subjects
        ]
        return Response(teacher_list)

class StudentScheduleView(APIView):
    "Расписание для ученика по id."
    def get(self, request, student_id):
        try:
            student_schedules = StudentSchedule.objects.filter(student_id=student_id)
            if not student_schedules.exists():
                return Response({"error": "Schedule not found for the given student"}, status=404)
            student = Student.objects.get(id_student=student_id)
            lessons = []
            for schedule in student_schedules:
                lessons.extend(schedule.lessons.all())
            schedule_data = {
                "student_name": f"{student.surname} {student.name}",
                "class_name": student.class_name,
                "lessons": [{"subject": lesson.subject, "day": lesson.day, "lesson_number": lesson.lesson_number} for
                            lesson in lessons]
            }
            return Response(schedule_data)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)


class GradeListView(APIView):
    "Оценки для ученика по id."
    def get(self, request, student_id):
        grades = Grade.objects.filter(student_id=student_id)
        student = Student.objects.get(id_student=student_id)
        if grades.exists():
            grade_data = [
                {
                    "student_name": f"{student.surname} {student.name}",
                    "subject": grade.subject,
                    "grade": grade.grade,
                    "quarter": grade.quarter
                }
                for grade in grades
            ]
            return Response(grade_data)
        else:
            return Response({"error": "Grades not found for the given student"}, status=404)
