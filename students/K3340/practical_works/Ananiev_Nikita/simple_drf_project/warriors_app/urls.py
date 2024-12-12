from django.urls import path
from .views import *


app_name = "warriors_app"

urlpatterns = [
   path('warriors/<int:id>/', WarriorAPIView.as_view()),
   path('warriors/<int:id>/delete', WarriorDeleteAPIView.as_view()),
   path('warriors/<int:id>/update', WarriorUpdateAPIView.as_view()),
   path('warriors/list/', WarriorListAPIView.as_view()),
   path('warriors/create/', WarriorCreateView.as_view()),
   path('profession/create/', ProfessionCreateView.as_view()),
   path('skills/list/', SkillAPIView.as_view()),
   path('skills/create/', SkillCreateView.as_view()),
]