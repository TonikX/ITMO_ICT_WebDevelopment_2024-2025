from rest_framework import viewsets
from .models import Teacher, Subject
from .serializers import TeacherSerializer, SubjectSerializer
from django.shortcuts import render

# DRF ViewSets
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

# Главная HTML-страница
def home(request):
    return render(request, "index.html")
