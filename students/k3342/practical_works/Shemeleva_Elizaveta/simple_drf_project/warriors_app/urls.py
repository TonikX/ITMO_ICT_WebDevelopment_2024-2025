from django.urls import path
from .views import (
    WarriorCreateAPIView, WarriorListAPIView, WarriorDetailAPIView, WarriorUpdateAPIView, WarriorDeleteAPIView,
    ProfessionCreateAPIView, ProfessionListAPIView, SkillListAPIView, SkillCreateAPIView, SkillOfWarriorListAPIView,
    SkillOfWarriorCreateAPIView, WarriorWithProfessionListAPIView, WarriorWithSkillsListAPIView
)

urlpatterns = [
   path('warrior/generic_create/', WarriorCreateAPIView.as_view()),
   path('warriors/list/', WarriorListAPIView.as_view()),
   path('profession/generic_create/', ProfessionCreateAPIView.as_view()),
   path('professions/list/', ProfessionListAPIView.as_view()),
   path('skills/list/', SkillListAPIView.as_view()),
   path('skill/generic_create/', SkillCreateAPIView.as_view()),
   path('warrior-skills/list/', SkillOfWarriorListAPIView.as_view()),
   path('warrior-skill/generic_create/', SkillOfWarriorCreateAPIView.as_view()),
   path('warriors-professions/', WarriorWithProfessionListAPIView.as_view(), name='warriors_professions'),
   path('warriors-skills/', WarriorWithSkillsListAPIView.as_view(), name='warriors_skills'),
   path('warrior/<int:pk>/', WarriorDetailAPIView.as_view(), name='warrior_detail'),
   path('warrior/<int:pk>/delete/', WarriorDeleteAPIView.as_view(), name='warrior_delete'),
   path('warrior/<int:pk>/update/', WarriorUpdateAPIView.as_view(), name='warrior_update'),
]
