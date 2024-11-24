from django.urls import path
from .views import *


app_name = "warriors_app"


urlpatterns = [
   path('skills/', SkillsGetView.as_view()),
   path('skills/create', SkillCreateView.as_view()),
   path('warriors/professions/', WarriorListWithProfessionAPIView.as_view(), name='warriors-with-professions'),
   path('warriors/skills/', WarriorListWithSkillsAPIView.as_view(), name='warriors-with-skills'),
   path('warriors/<int:pk>/', WarriorDetailAPIView.as_view(), name='warrior-detail'),
]