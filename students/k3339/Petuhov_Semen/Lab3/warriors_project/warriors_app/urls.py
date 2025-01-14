from django.urls import path
from .views import *


app_name = "warriors_app"


urlpatterns = [
   path('warriors/', WarriorAPIView.as_view()),
   path('profession/create/', ProfessionCreateView.as_view()),
   path('skills/', SkillAPIView.as_view()),
   path('skills/create/', SkillCreateView.as_view()),
   path('warriors2/', WarriorListView.as_view(), name='warrior-list'),
   path('warriors/skills/', WarriorSkillsListView.as_view(), name='warrior-skills-list'),
   path('warriors/<int:pk>/', WarriorDetailView.as_view(), name='warrior-detail'),
   path('warriors/<int:pk>/delete/', WarriorDeleteView.as_view(), name='warrior-delete'),
   path('warriors/<int:pk>/update/', WarriorUpdateView.as_view(), name='warrior-update'),
]