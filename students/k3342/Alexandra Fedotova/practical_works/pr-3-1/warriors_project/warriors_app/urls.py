from django.urls import path
from .views import *

app_name = "warriors_app"

urlpatterns = [
    path('warriors/', WarriorAPIView.as_view(), name="warriors-list"),
    path('warriors/create/', WarriorCreateView.as_view(), name='create-warrior'),
    path('warriorslist/', WarriorListAPIView.as_view(), name='warrior-list'),
    path('warriors/<int:pk>/delete/', WarriorDeleteView.as_view(), name='warrior-delete'),
    path('warriors/<int:pk>/update/', WarriorUpdateView.as_view(), name='warrior-update'),
    path('warriors/<int:pk>/', WarriorDetailView.as_view(), name='warrior-detail'),
    path('warriors/professions/', WarriorAndProfessionAPIView.as_view()),
    path('warriors/skills/', WarriorAndSkillsAPIView.as_view()),
    path('profession/create/', ProfessionCreateView.as_view()),
    path('skill/', SkillAPIView.as_view(), name='skill-list'),
    path('skill/create/', SkillCreateView.as_view(), name='skill-create'),
]
