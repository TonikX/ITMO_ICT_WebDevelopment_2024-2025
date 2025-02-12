from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.db.models import Count
from rest_framework.decorators import api_view


class TeacherAPIView(APIView):
    """
    Просмотр списка учителей
    """
    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response({"Teachers": serializer.data})


class StudentAPIView(APIView):
    """
    Просмотр списка учащихся
    """
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


class ClassAPIView(APIView):
    """
    Просмотр списка учителей
    """
    def get(self, request):
        classes = Class.objects.all()
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data)


class AddTeacherView(APIView):
    """
    Добавление нового учителя
    """
    def post(self, request):
        serializer = TecherAdd(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class SubjectsAPIView(APIView):
    """
    Просмотр списка учителей
    """
    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


class ClassroomsAPIView(APIView):
    """
    Просмотр списка учителей
    """
    def get(self, request):
        classrooms = Classroom.objects.all()
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data)


class AddStudentView(APIView):
    """
    Класс для добавления нового ученика
    """
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        

class AddGradesView(APIView):
    """
    Внесение четвертных оценок
    """
    def post(self, request):
        serializer = AddGradeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class DeleteTeacherView(APIView):
    """
    Удаление данных об уволившемся учителе
    """
    def delete(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
            teacher.delete()
            return Response({"message": f"Учитель с ID {pk} успешно удалён."})
        except Teacher.DoesNotExist:
            return Response({"error": f"Учитель с ID {pk} не найден."})


class DeleteStudentView(APIView):
    """
    Удаление данных об отчисленном ученике
    """
    def delete(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            student.delete()
            return Response({"message": f"Ученик с ID {pk} успешно удалён."})
        except Student.DoesNotExist:
            return Response({"error": f"Ученик с ID {pk} не найден."})


class UpdateTeacherView(APIView):
    """
    Внесение изменений в данные об учителе
    """
    def put(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({'error': 'Warrior not found'}, status=404)
            
        serializer = TeacherUpdateSerializer(teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class UpdateStudentView(APIView):
    """
    Внесение изменений в данные об ученике
    """
    def put(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Student.DoesNotExist:
            return Response({"error": f"Ученик с ID {pk} не найден."})



class UpdateGradeView(APIView):
    """
    Внесение изменений в оценку ученика по предмету
    """
    def put(self, request, pk):
        try:
            grade = Grade.objects.get(pk=pk)
        except Grade.DoesNotExist:
            return Response({'error': 'Warrior not found'}, status=404)
        
        serializer = GradeUpdateSerializer(grade, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ScheduleManagementView(APIView):
    """
    Управления расписанием занятий.
    """

    def get(self, request):
        """
        Получить список всех записей в расписании
        """
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Добавить новую запись в расписание
        """
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self, request, pk):
        """
        Обновить существующую запись в расписании
        """
        try:
            schedule = Schedule.objects.get(pk=pk)
            serializer = ScheduleSerializer(schedule, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Schedule.DoesNotExist:
            return Response({"detail": "Запись расписания не найдена."})

    def delete(self, request, pk):
        """
        Удалить запись в расписании
        """
        try:
            schedule = Schedule.objects.get(pk=pk)
            schedule.delete()
            return Response({"detail": "Запись в расписании успешно удалена."})
        except Schedule.DoesNotExist:
            return Response({"detail": "Запись расписания не найдена."})


class ClassReportView(APIView):
    """
    Отчет по успеваемости класса
    """
    def get(self, request, class_id, format=None):
        try:
            school_class = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return Response({'error': 'Class not found'})
        
        serializer = ClassReportSerializer(school_class)
        
        return Response(serializer.data)


class TeachersPerSubject(APIView):
    """
    Количество учителей по каждому предмету
    """
    def get(self, request):
        subjects = Subject.objects.annotate(num_teachers=Count('teacher')).values('title', 'num_teachers')
        return Response(subjects)


class StudentsPerClassGender(APIView):
    """
    Количество учеников в каждому классе (ж/м)
    """
    def get(self, request, class_name, gender):
    
        school_class = Class.objects.filter(name=class_name).first()

        if not school_class:
            return Response({"error": "Класс не найден"})

        gender_types = {
            'm': 'Мужской',
            'f': 'Женский'
        }
        
        if gender not in gender_types:
            return Response({"error": "Пол должен быть 'm' или 'f'"})

        students_count = Student.objects.filter(school_classes=school_class, gender=gender).count()
        return Response({
            'class': class_name,
            'gender': gender_types[gender],
            'students_count': students_count
        })


class ClassroomTypeCount(APIView):
    """
    Количество проф/непроф классов
    """
    def get(self, request, is_profile):
        
        if is_profile not in ["profile", "basic"]:
            return Response(
                {"error": "Тип кабинета должен быть 'profile' (профильный) или 'basic' (непрофильный)"}
            )

        is_profile_flag = True if is_profile == "profile" else False
        classrooms_count = Classroom.objects.filter(is_profile=is_profile_flag).count()

        profile_status = "Профильные" if is_profile_flag else "Непрофильные"

        return Response({
            "classroom_type": profile_status,
            "count": classrooms_count
        })


class ClassScheduleAPIView(APIView):
    """
    Какой предмет будет в заданном классе, в заданный день недели на заданном уроке
    """
    def get(self, request, class_name, day, lesson_time):
        
        schedule = Schedule.objects.filter(
            class_group__name=class_name,
            day_of_week=day,
            time=lesson_time
        )

        if not schedule.exists():
            return Response(
                {"message": "Предмет не найден для заданных параметров."}
            )

        serializer = ScheduleSerializer(schedule, many=True)
        return Response(serializer.data)


class TeacherSubjectView(APIView):
    """
    Представление для работы с данными TeacherSubject.
    """
    def get(self, request):
        teacher_subjects = TeacherSubject.objects.all()
        serializer = TeacherSubjectSerializer(teacher_subjects, many=True)
        return Response(serializer.data)
    

class GradeListView(APIView):
    """
    Вывод всех оценок
    """
    def get(self, request):
        grades = Grade.objects.all()
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)


class StudentClassManagementView(APIView):
    """
    Управление ассоциацией учеников с классами.
    """

    def get(self, request):
        """
        Получить список всех ассоциаций учеников с классами.
        """
        student_classes = StudentClass.objects.all()
        serializer = StudentClassSerializer(student_classes, many=True)
        return Response(serializer.data)


class StudentClassAddView(APIView):
    def post(self, request):
        serializer = StudentClassAdd(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class StudentFullListView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentFullSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateStudentClassView(APIView):
    def put(self, request, pk):
        try:
            student_classes = StudentClass.objects.get(pk=pk)
        except StudentClass.DoesNotExist:
            return Response({'error': 'Warrior not found'}, status=404)
            
        serializer = StudentClassUpdateSerializer(student_classes, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class DeleteStudentClassView(APIView):
    """
    Удаление данных об отчисленном ученике
    """
    def delete(self, request, pk):
        try:
            student_classes = StudentClass.objects.get(pk=pk)
            student_classes.delete()
            return Response({"message": f"Ученик с ID {pk} успешно удалён."})
        except Student.DoesNotExist:
            return Response({"error": f"Ученик с ID {pk} не найден."})


class TeacherSubjectAddView(APIView):
    def post(self, request):
        serializer = TeacherSubjectAdd(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class UpdateTeacherSubjectView(APIView):
    def put(self, request, pk):
        try:
            teacher_subjects = TeacherSubject.objects.get(pk=pk)
        except TeacherSubject.DoesNotExist:
            return Response({'error': 'Warrior not found'}, status=404)
            
        serializer = TeacherSubjectUpdateSerializer(teacher_subjects, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class DeleteTeacherSubjectView(APIView):
    def delete(self, request, pk):
        try:
            teacher_subjects = TeacherSubject.objects.get(pk=pk)
            teacher_subjects.delete()
            return Response({"message": f"Учитель с ID {pk} успешно удалён."})
        except TeacherSubject.DoesNotExist:
            return Response({"error": f"Учитель с ID {pk} не найден."})


class TeacherFullListView(APIView):
    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherFullSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteGradeView(APIView):
    def delete(self, request, pk):
        try:
            grades = Grade.objects.get(pk=pk)
            grades.delete()
            return Response({"message": f"Оценка с ID {pk} успешно удалён."})
        except Grade.DoesNotExist:
            return Response({"error": f"Оценка с ID {pk} не найден."})