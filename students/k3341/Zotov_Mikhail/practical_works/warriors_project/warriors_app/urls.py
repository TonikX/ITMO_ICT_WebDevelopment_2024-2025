from django.urls import path
from .views import *

app_name = "warriors_app"

urlpatterns = [
    path('warriors/', WarriorAPIView.as_view()),
    path('profession/create/', ProfessionCreateView.as_view()),
    path('skills/', SkillAPIView.as_view()),
    path('skills/create/', SkillCreateView.as_view()),
    path('warriors/list/', WarriorListAPIView.as_view()),
    path('profession/generic_create/', ProfessionCreateAPIView.as_view()),
    path('warriors/professions/', WarriorProfessionListAPIView.as_view()),
    path('warriors/skills/', WarriorSkillListAPIView.as_view()),
    path('warriors/<int:pk>/', WarriorDetailAPIView.as_view()),
    path('warriors/<int:pk>/delete', WarriorDeleteAPIView.as_view()),
    path('warriors/<int:pk>/update', WarriorUpdateAPIView.as_view()),
]
