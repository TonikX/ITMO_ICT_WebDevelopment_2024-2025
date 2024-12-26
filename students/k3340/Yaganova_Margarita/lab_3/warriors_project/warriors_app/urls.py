from django.urls import path
from .views import *

app_name = "warriors_app"

urlpatterns = [
    path('warriors/profession/', WarriorProfessionListAPIView.as_view()),
    path('warriors/skills/', WarriorSkillsListAPIView.as_view()),
    path('skills/', SkillAPIView.as_view()),
    path('warriors/<int:id>/', WarriorDetailAPIView.as_view()),
    path('warriors/<int:id>/delete/', WarriorDeleteAPIView.as_view()),
    path('warriors/<int:id>/update/', WarriorUpdateAPIView.as_view())
]
