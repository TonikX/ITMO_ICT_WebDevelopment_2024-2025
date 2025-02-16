from django.urls import path
from .views import *

app_name = "warriors_app"

urlpatterns = [
    path('profession/create/', ProfessionCreateView.as_view()),
    path('skills/', SkillAPIView.as_view()),
    path('skills/create/', SkillCreateView.as_view()),
    path('warriors/', WarriorListAPIView.as_view()),
    path('warriors/<int:pk>/', WarriorRetrieveUpdateDestroyAPIView.as_view()),
    path('warriors/create/', WarriorCreateView.as_view()),
]
