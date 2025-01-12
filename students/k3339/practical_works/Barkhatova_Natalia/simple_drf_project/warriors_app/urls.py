from django.urls import path
from .views import *


app_name = "warriors_app"


urlpatterns = [
   path('warriors/', WarriorAPIView.as_view()),
   path('profession/create/',  ProfessionCreateView.as_view()),
   path('skills/', SkillAPIView.as_view()),
   path('skills/create/', SkillCreateView.as_view()),
   path('warriors/with_professions/', WarriorWithProfessionListView.as_view()),
   path('warriors/with_skills/', WarriorWithSkillsListView.as_view()),
   path('warriors/<int:id>/', WarriorDetailView.as_view()),
   path('warriors/delete/<int:pk>/', WarriorDeleteView.as_view()),
   path('warriors/update/<int:pk>/', WarriorUpdateView.as_view()),
]