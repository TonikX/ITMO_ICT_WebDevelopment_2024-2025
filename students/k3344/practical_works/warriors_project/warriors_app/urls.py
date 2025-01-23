from django.urls import path
from .views import *

app_name = "warriors_app"

urlpatterns = [
    path('warriors/', WarriorAPIView.as_view()),
    path("warriors/skill/", WarriorSkillListApiView.as_view()),
    path('warriors/<int:pk>/', ShowWarriorAPIView.as_view()),
    path("warriors/delete/<int:pk>/", DeleteWarriorAPIView.as_view()),
    path("warriors/update/<int:pk>/", UpdateWarriorAPIView.as_view()),
    path('warriors/list/', WarriorListAPIView.as_view()),
    path('profession/create/', ProfessionCreateView.as_view()),
    path("warriors/profession/", WarriorProfessionListAPIView.as_view()),
    path('profession/generic_create/', ProfessionCreateAPIView.as_view()),
    path('skills/', SkillAPIView.as_view()),
    path('skill/create/', SkillCreateView.as_view()),
]