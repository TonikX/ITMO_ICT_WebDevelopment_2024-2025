from django.urls import path
from .views import *

app_name = 'warrior_app'

urlpatterns = [
    # path('warrior/', WarriorAPIView.as_view()),
    path('profession/create/', ProfessionAPICreate.as_view()),
    path('skill/', SkillAPIView.as_view()),
    path('skill/create/', SkillAPICreate.as_view()),
    path('warrior/', WarriorListAPIView.as_view()),
    path('warrior/<int:pk>/', WarriorAPIView.as_view()),
]