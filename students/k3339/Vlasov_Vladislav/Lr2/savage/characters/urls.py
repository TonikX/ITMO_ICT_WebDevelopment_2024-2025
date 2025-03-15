from django.urls import path, include
from . import views
from .views import getSkills, updateSkill, createSkill, deleteSkill, deleteCharacter

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('user/registration/', views.createNewUser, name="user_registration"),
    path('logged_out/', views.my_logout, name='my_logout'),

    path('characters/list/', views.getAllCharacters, name='characters_list'),
    path('character/create/', views.createCharactersAttributes, name='character_create'),
    path('character/<int:pk>/update/', views.updateCharactersAttributes, name='character_update'),
    path('character/<int:pk>/', views.getCharacter, name='character'),
    path('character/<int:pk>/delete/', deleteCharacter.as_view(), name="character_delete"),

    path('skills/list/', getSkills.as_view(), name="skills_list"),
    path('skill/create/',createSkill.as_view(), name="skill_create"),
    path('skill/<int:pk>/update/', updateSkill.as_view(), name="skill_update"),
    path('skill/<int:pk>/delete/', deleteSkill.as_view(), name="skill_delete"),
]