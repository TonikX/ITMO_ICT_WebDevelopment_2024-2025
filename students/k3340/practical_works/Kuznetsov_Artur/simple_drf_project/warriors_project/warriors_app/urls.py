from django.urls import path
from .views import *

app_name = "warriors_app"

urlpatterns = [
    path('warriors/', WarriorAPIView.as_view()),
    path('warriors/create/', WarriorCreateAPIView.as_view()),
    path('warriors/list/', WarriorListAPIView.as_view()),
    path('profession/create/', ProfessionCreateView.as_view()),
    path('profession/generic_create/', ProfessionCreateAPIView.as_view()),
    path('skills/', SkillListView.as_view()),
    path('skills/create/', SkillCreateView.as_view()),
    path('warriors/link_skills/', LinkSkillsToWarriorView.as_view()),
    path('warriors/with_professions/', WarriorWithProfessionListView.as_view()),
    path('warriors/with_skills/', WarriorWithSkillsListView.as_view()),
    path('warriors/<int:pk>/', WarriorDetailView.as_view()),
    path('warriors/delete/<int:pk>/', WarriorDeleteView.as_view()),
    path('warriors/update/<int:pk>/', WarriorUpdateView.as_view()),
]
