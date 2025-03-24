from django.urls import path
from .views import WarriorAPIView, SkillAPIView, WarriorsWithProfessionsView, WarriorsWithSkillsView, WarriorDetailView

urlpatterns = [
    path('warriors/', WarriorAPIView.as_view(), name='warriors-list'),
    path('skills/', SkillAPIView.as_view(), name='skills-list'),
    path('warriors/professions/', WarriorsWithProfessionsView.as_view(), name='warriors-with-professions'),
    path('warriors/skills/', WarriorsWithSkillsView.as_view(), name='warriors-with-skills'),
    path('warriors/<int:pk>/', WarriorDetailView.as_view(), name='warrior-detail'),
]
