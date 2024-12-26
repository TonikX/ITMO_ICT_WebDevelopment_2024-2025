from django.urls import path
from warriors_app import views


urlpatterns = [
    path("warriors/", views.WarriorAPIView.as_view()),
    path("warriors/<int:pk>/", views.WarriorDetailView.as_view()),
    path("warriors/profession/", views.WarriorWithProfessionView.as_view()),
    path("warriors/skill/", views.WarriorWithSkillView.as_view()),
    path("professions/", views.ProfessionCreateView.as_view()),
    path("skills/", views.SkillView.as_view()),
]
