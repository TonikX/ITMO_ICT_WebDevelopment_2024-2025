from django.urls import path
from .views import *


app_name = "warriors_app"


urlpatterns = [
    path('warriors/', WarriorAPIView.as_view()),
    path('profession/create/', ProfessionCreateView.as_view()),
    path('skill/', SkillView.as_view()),
    path('warriors/<int:pk>/', WarriorDetailView.as_view()),
    path('warriors/profession/', WarriorWithProfessionView.as_view()),
    path('warriors/skill/', WarriorWithSkillView.as_view()),
]