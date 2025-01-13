from django.urls import path
from .views import *


app_name = "warriors_app"


urlpatterns = [
   path('warriors/', WarriorAPIView.as_view()), 
   path('warriors/<int:pk>/', WarriorDetailAPIView.as_view(), name='warrior-detail'),
   path('warriors/<int:pk>/delete/', WarriorDeleteAPIView.as_view(), name='warrior-delete'),
   path('warriors/<int:pk>/update/', WarriorUpdateAPIView.as_view(), name='warrior-update'),
   path('warriors/create', WarriorCreateAPIView.as_view(), name='warrior-create'), 
   path('warriors/professions', WarriorProfessionListAPIView.as_view(), name='warrior-profession-list'),
   path('warriors/skills', WarriorSkillsListAPIView.as_view(), name='warrior-skills-list'),
   path('skills/', SkillAPIView.as_view()), 
   path('profession/create/', ProfessionCreateView.as_view()),
   path('profession/create/', ProfessionCreateView.as_view()),
   path('skills/create/', SkillCreateView.as_view()),
   ]