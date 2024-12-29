from django.urls import path
from .views import *


app_name = "warriors_app"


urlpatterns = [
   path('warriors/', WarriorAPIView.as_view()),
   path('profession/create/', ProfessionCreateView.as_view()),
   path('skills/', SkillListAPIView.as_view(), name='skill_list'),
#----------------------
   # 1. Вывод полной информации о всех воинах и их профессиях
   path('warriors/professions/', WarriorProfessionListAPIView.as_view(), name='warriors_professions'),

    # 2. Вывод полной информации о всех воинах и их скиллах
   path('warriors/skills/', WarriorSkillListAPIView.as_view(), name='warriors_skills'),

    # 3. Вывод полной информации о воине (по id), его профессии и скиллах
   path('warriors/<int:pk>/', WarriorRetrieveAPIView.as_view(), name='warrior_detail'),

    # 4. Удаление воина по id
   path('warriors/<int:pk>/delete/', WarriorDestroyAPIView.as_view(), name='warrior_delete'),

    # 5. Редактирование информации о воине
   path('warriors/<int:pk>/update/', WarriorUpdateAPIView.as_view(), name='warrior_update'),

   path('warriors/create/', WarriorCreateAPIView.as_view(), name='warrior_create'),
]