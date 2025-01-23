from django.urls import path

from .views import WarriorProfessionListAPIView, WarriorSkillListAPIView, WarriorDetailAPIView, WarriorDeleteAPIView, \
    WarriorUpdateAPIView, SkillCreateView, SkillListView, WarriorsListView

urlpatterns = [
    path('warriors/', WarriorsListView.as_view(), name='warriors-list'),

    path('skill/create/', SkillCreateView.as_view(), name='skill-create'),

    path('skills/', SkillListView.as_view(), name='skill-list'),

    path('warriors/professions/', WarriorProfessionListAPIView.as_view(), name='warrior-professions'),

    path('warriors/skills/', WarriorSkillListAPIView.as_view(), name='warrior-skills'),

    path('warriors/<int:pk>/', WarriorDetailAPIView.as_view(), name='warrior-detail'),

    path('warriors/delete/<int:pk>/', WarriorDeleteAPIView.as_view(), name='warrior-delete'),

    path('warriors/update/<int:pk>/', WarriorUpdateAPIView.as_view(), name='warrior-update'),
]
