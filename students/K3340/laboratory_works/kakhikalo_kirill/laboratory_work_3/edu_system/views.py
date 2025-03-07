from rest_framework import viewsets
from edu_system.models import (
    EducationProgram,
    AcademicDiscipline,
    ProgramElement,
    Group,
    Student,
    Classroom,
    Teacher,
    ClassSession,
    TeachingPermit,
    Result
)
from edu_system.serializers import (
    EducationProgramSerializer,
    AcademicDisciplineSerializer,
    ProgramElementSerializer,
    GroupSerializer,
    StudentSerializer,
    ClassroomSerializer,
    TeacherSerializer,
    ClassSessionSerializer,
    TeachingPermitSerializer,
    ResultSerializer
)

class EducationProgramViewSet(viewsets.ModelViewSet):
    queryset = EducationProgram.objects.all()
    serializer_class = EducationProgramSerializer


class AcademicDisciplineViewSet(viewsets.ModelViewSet):
    queryset = AcademicDiscipline.objects.all()
    serializer_class = AcademicDisciplineSerializer


class ProgramElementViewSet(viewsets.ModelViewSet):
    queryset = ProgramElement.objects.all()
    serializer_class = ProgramElementSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class ClassSessionViewSet(viewsets.ModelViewSet):
    queryset = ClassSession.objects.all()
    serializer_class = ClassSessionSerializer


class TeachingPermitViewSet(viewsets.ModelViewSet):
    queryset = TeachingPermit.objects.all()
    serializer_class = TeachingPermitSerializer


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
