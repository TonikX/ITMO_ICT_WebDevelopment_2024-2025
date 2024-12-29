from django.urls import path
from .views import *


app_name = "warriors_app"
urlpatterns = [
    path('warriors/', WarriorAPIView.as_view()),
    path('warrior/create', WarriorCreateView.as_view()),
    path('profession/create/', ProfessionCreateView.as_view()),
    path('skills/', SkillAPIView.as_view()),
    path('skills/create/', SkillCreateView.as_view()),
    path('skills_of_warrior/create/', SkillOfWarriorCreateView.as_view()),
    path('warriors_and_professions/', WarriorWithProfessionAPIView.as_view()),
    path('warriors_and_skills/', WarriorWithSkillAPIView.as_view()),
    path('warrior/<int:pk>/', WarriorDetailAPIView.as_view()),
    path('warrior/delete/<int:pk>/', WarriorDeleteView.as_view()),
    path('warrior/update/<int:pk>/', WarriorUpdateView.as_view()),
]