from django.urls import path
from .views import *

app_name = "warriors_app"

urlpatterns = [
    path('warriors/', WarriorAPIView.as_view(), name='warriors_list'),
    path('skills/', SkillListView.as_view(), name='skill-list'),
    path('skills/create/', SkillCreateView.as_view(), name='skill-create'),
    path('warriors/professions/', WarriorWithProfessionAPIView.as_view(), name='warrior_with_profession'),
    path('warriors/skills/', WarriorWithSkillsAPIView.as_view(), name='warrior_with_profession'),
    path('warrior/<int:pk>/', WarriorDetailAPIView.as_view(), name='warrior_full'),
    path('warrior/<int:pk>/delete/', WarriorDeleteAPIView.as_view(), name='warrior_delete'),
    path('warrior/<int:pk>/update/', WarriorUpdateAPIView.as_view(), name='warrior_update'),
]
