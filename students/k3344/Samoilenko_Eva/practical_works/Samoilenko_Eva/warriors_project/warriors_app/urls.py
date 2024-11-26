from django.urls import path
from .views import *


app_name = "warriors_app"

urlpatterns = [
    path('warriors/', WarriorAPIView.as_view()),
    # path('profession/create/', ProfessionCreateView.as_view()),
    path('skills/', SkillGetAPIView.as_view()),
    path('skills/create/', SkillCreateAPIView.as_view()),
    path('warriors/professions/', WarriorWithProfessionAPIView.as_view()),
    path('warriors/skills/', WarriorWithSkillsAPIView.as_view()),
    path('warriors/<int:pk>/', WarriorDetailAPIView.as_view()),

]
