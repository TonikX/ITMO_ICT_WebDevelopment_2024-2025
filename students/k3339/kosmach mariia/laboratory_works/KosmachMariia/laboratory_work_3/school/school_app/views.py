from django.db.models import Min, Max
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status, permissions, authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *


class TeacherListView(generics.ListAPIView):
    queryset = Teachers.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class TeacherRetrieveView(generics.RetrieveAPIView):
    queryset = Teachers.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class TeacherCreateView(generics.CreateAPIView):
    queryset = Teachers.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class TeacherUpdateView(generics.UpdateAPIView):
    queryset = Teachers.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class TeacherDeleteView(generics.DestroyAPIView):
    queryset = Teachers.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class CabinetListView(generics.ListAPIView):
    queryset = Cabinets.objects.all()
    serializer_class = CabinetSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class CabinetRetrieveView(generics.RetrieveAPIView):
    queryset = Cabinets.objects.all()
    serializer_class = CabinetSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class CabinetCreateView(generics.CreateAPIView):
    queryset = Cabinets.objects.all()
    serializer_class = CabinetSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class CabinetUpdateView(generics.UpdateAPIView):
    queryset = Cabinets.objects.all()
    serializer_class = CabinetSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class CabinetDeleteView(generics.DestroyAPIView):
    queryset = Cabinets.objects.all()
    serializer_class = CabinetSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class ClassListView(generics.ListAPIView):
    queryset = Classes.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class ClassRetrieveView(generics.RetrieveAPIView):
    queryset = Classes.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class ClassCreateView(generics.CreateAPIView):
    queryset = Classes.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class ClassUpdateView(generics.UpdateAPIView):
    queryset = Classes.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class ClassDeleteView(generics.DestroyAPIView):
    queryset = Classes.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class StudentListView(generics.ListAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class StudentRetrieveView(generics.RetrieveAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class StudentCreateView(generics.CreateAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentAddSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class StudentUpdateView(generics.UpdateAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentAddSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class StudentDeleteView(generics.DestroyAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class ScheduleListView(generics.ListAPIView):
    queryset = Schedules.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class ScheduleRetrieveView(generics.RetrieveAPIView):
    queryset = Schedules.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class ScheduleCreateView(generics.CreateAPIView):
    queryset = Schedules.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class ScheduleUpdateView(generics.UpdateAPIView):
    queryset = Schedules.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class ScheduleDeleteView(generics.DestroyAPIView):
    queryset = Schedules.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class TeachingListView(generics.ListAPIView):
    queryset = Teachings.objects.all()
    serializer_class = TeachingSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class TeachingRetrieveView(generics.RetrieveAPIView):
    queryset = Teachings.objects.all()
    serializer_class = TeachingSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class TeachingCreateView(generics.CreateAPIView):
    queryset = Teachings.objects.all()
    serializer_class = TeachingSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class TeachingUpdateView(generics.UpdateAPIView):
    queryset = Teachings.objects.all()
    serializer_class = TeachingSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class TeachingDeleteView(generics.DestroyAPIView):
    queryset = Teachings.objects.all()
    serializer_class = TeachingSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class SubjectListView(generics.ListAPIView):
    queryset = Subjects.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class SubjectRetrieveView(generics.RetrieveAPIView):
    queryset = Subjects.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class SubjectCreateView(generics.CreateAPIView):
    queryset = Subjects.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class SubjectUpdateView(generics.UpdateAPIView):
    queryset = Subjects.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class SubjectDeleteView(generics.DestroyAPIView):
    queryset = Subjects.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class SpecialStudentListView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)

    def get_queryset(self):
        grade = self.kwargs['grade']
        studs = Students.objects.filter(grades__grade__contains=grade)
        return studs


class GradeListView(generics.ListAPIView):
    queryset = Grades.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class GradeRetrieveView(generics.RetrieveAPIView):
    queryset = Grades.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class GradeCreateView(generics.CreateAPIView):
    queryset = Grades.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class GradeUpdateView(generics.UpdateAPIView):
    queryset = Grades.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class GradeDeleteView(generics.DestroyAPIView):
    queryset = Grades.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (authentication.TokenAuthentication,)


class LogOut(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
