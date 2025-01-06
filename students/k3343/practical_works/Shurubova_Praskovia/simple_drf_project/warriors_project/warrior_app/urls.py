from django.urls import path
from .views import *


app_name = "warrior_app"


urlpatterns = [
   path('warriors/', WarriorAPIView.as_view()),
   path('skills/create/', SkillCreateAPIView.as_view()),
   path('skills/', SkillListAPIView.as_view()),
   path('warriors/profession/', WarriorWithProfessionListView.as_view()),
   path('warriors/skills/', WarriorWithSkillsListView.as_view()),
   path('warriors/create/', WarriorCreateAPIView.as_view()),
   path('warrior/<int:pk>/', WarriorDetailAPIView.as_view()),
   path('warrior/<int:pk>/delete/', WarriorDeleteAPIView.as_view()),
   path('warrior/<int:pk>/update/', WarriorUpdateAPIView.as_view()),
   path('profession/create/', ProfessionCreateAPIView.as_view()),
]