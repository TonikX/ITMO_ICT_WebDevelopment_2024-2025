from django.urls import path
from .views import WarriorAPIView, SkillAPIView, WarriorListAPIView, WarriorDetailAPIView, WarriorUpdateDeleteAPIView

urlpatterns = [
    path('warriors/', WarriorAPIView.as_view()),
    path('skills/', SkillAPIView.as_view(), name='skill-list'),
    path('warriors/', WarriorListAPIView.as_view(), name='warrior-list'),
    path('warriors/<int:pk>/', WarriorDetailAPIView.as_view(), name='warrior-detail'),
    path('warriors/<int:pk>/edit/', WarriorUpdateDeleteAPIView.as_view(), name='warrior-edit'),
]
