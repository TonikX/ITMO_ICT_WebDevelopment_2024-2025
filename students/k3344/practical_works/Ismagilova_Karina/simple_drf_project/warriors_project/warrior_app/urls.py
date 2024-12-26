from django.urls import path
from .views import *


app_name = "warrior_app"


urlpatterns = [
    path('warriors/list/', WarriorListAPIView.as_view()),
    path('skill/', SkillListView.as_view(), name='skill-list'),
    path('skill/create/', SkillCreateView.as_view(), name='create-skill'),
    path('profession/generic_create/', ProfessionCreateAPIView.as_view()),
    path('warriors/create/', WarriorCreateAPIView.as_view(), name='warrior-create'),
    path('warriors/skills/', WarriorWithSkillListAPIView.as_view(), name='warrior-list-with-skills'),
    path('warriors/professions/', WarriorWithProfessionListAPIView.as_view(), name='warrior-list-with-professions'),
    path('warriors/<int:id>/', WarriorDetailAPIView.as_view(), name='warrior-detail'),
    path('warriors/<int:id>/delete/', WarriorDeleteAPIView.as_view(), name='warrior-delete'),
    path('warriors/<int:id>/update/', WarriorUpdateAPIView.as_view(), name='warrior-update')
]