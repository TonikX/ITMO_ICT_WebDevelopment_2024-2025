from django.urls import path
from .views import *


app_name = "warriors_app"


urlpatterns = [
   path('warriors/', WarriorAPIView.as_view()),
   path('profession/create/', ProfessionCreateView.as_view()),
   path('skills/', SkillAPIView.as_view()),
   path('skill/create/', SkillCreateView.as_view()),
   path('warriors_and_professions', WarriorProfessionAPIView.as_view()),

   path('warriors_and_skills', WarriorSkillAPIView.as_view()),

   path('warriors_and_skills_and_professions', WarriorSkillProfessionAPIView.as_view()),

   path('warrior/delete/<int:pk>/', WarriorDeleteView.as_view()),

   path('warrior/update/<int:pk>/', WarriorUpdateView.as_view()),
   ]