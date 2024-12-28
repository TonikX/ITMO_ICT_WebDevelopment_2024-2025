from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.db.models import Avg

from .models import Teacher, Student, Subject, Mark, Lesson, Grade
from .serializers import TeacherSerializer, StudentSerializer, SubjectSerializer, MarkSerializer, LessonSerializer, GradeSerializer

class TeacherViewSet(viewsets.ModelViewSet):
  queryset = Teacher.objects.all()
  serializer_class = TeacherSerializer
  # permission_classes = (IsAdminUser,)

class StudentViewSet(viewsets.ModelViewSet):
  queryset = Student.objects.all()
  serializer_class = StudentSerializer
  # permission_classes = (IsAdminUser,)

class SubjectViewSet(viewsets.ModelViewSet):
  queryset = Subject.objects.all()
  serializer_class = SubjectSerializer
  # permission_classes = (IsAdminUser,)

class MarkViewSet(viewsets.ModelViewSet):
  queryset = Mark.objects.all()
  serializer_class = MarkSerializer
  # permission_classes = (IsAdminUser,)

class LessonViewSet(viewsets.ModelViewSet):
  queryset = Lesson.objects.all()
  serializer_class = LessonSerializer
  # permission_classes = (IsAdminUser,)

class GradeViewSet(viewsets.ModelViewSet):
  queryset = Grade.objects.all()
  serializer_class = GradeSerializer
  # permission_classes = (IsAdminUser,)

  @action(detail=True, methods=['get'])
  def report(self, request, pk):
    grade = self.get_object()
    students = Student.objects.filter(grade=grade)
    data = {
      'average_marks': {},
      'total_students': students.count(),
      'teacher': grade.teacher.first_name + ' ' + grade.teacher.last_name,
    }
    for subject in Subject.objects.all():
      marks = Mark.objects.filter(student__grade=grade, subject=subject)
      if marks.exists():
        data['average_marks'][subject.name] = marks.aggregate(Avg('mark'))['mark__avg']
    return Response(data)