from django.urls import path
from warriors import views


urlpatterns = [
    path("warriors/", views.WarriorListView.as_view()),
    path("warriors/<int:pk>/", views.WarriorDetailView.as_view()),
    path("professions/create/", views.ProfessionCreateView.as_view()),
    path("skills/", views.SkillListView.as_view()),
    path("skills/create/", views.SkillCreateView.as_view()),
]
