from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<int:racer_id>/', views.other_profile, name='other_profile'),
    path('races/<str:race_type>/', views.race_list, name='race_list'),
    path('race/<int:race_id>/', views.race_detail, name='race_detail'),
    path('race/<int:race_id>/register/', views.register_for_race, name='register_for_race'),
    path('race/<int:race_id>/cancel_register/', views.cancel_register_for_race, name='cancel_register_for_race'),
    path('race/<int:race_id>/comment/', views.add_comment, name='add_comment'),

]
